"""Testes (apenas biblioteca padrão).

Rodar da raiz do repositório:  python -m unittest discover -s tests -t .
"""
import copy
import unittest

from src.energia import alternativas as alt
from src.energia import assistente, calculos as c
from src.energia.formatacao import falar, fmt_anos, fmt_num, fmt_rs


class TestCalculos(unittest.TestCase):
    def test_energia_kwh(self):
        self.assertAlmostEqual(c.energia_kwh(1000, 1), 1.0)
        self.assertAlmostEqual(c.energia_kwh(20, 10), 0.2)

    def test_energia_rejeita_negativos(self):
        with self.assertRaises(ValueError):
            c.energia_kwh(-1, 5)
        with self.assertRaises(ValueError):
            c.energia_kwh(10, -5)

    def test_custo_respeita_custo_de_disponibilidade(self):
        # geração maior que o consumo: ainda se paga o mínimo
        custo = c.custo_mensal(300, 1.0, geracao_kwh=500, disponibilidade_kwh=100)
        self.assertAlmostEqual(custo, 100.0)

    def test_custo_sem_geracao(self):
        self.assertAlmostEqual(c.custo_mensal(200, 0.9), 180.0)

    def test_custo_com_desconto_de_compensacao(self):
        # compensa 200 kWh, paga 100 kWh mínimo + 15% da tarifa sobre os 200 compensados
        custo = c.custo_mensal(300, 1.0, geracao_kwh=200, disponibilidade_kwh=100, desconto_compensacao=0.15)
        self.assertAlmostEqual(custo, 100 + 200 * 0.15)

    def test_consumo_abaixo_do_minimo_paga_minimo(self):
        self.assertAlmostEqual(c.custo_mensal(40, 1.0, disponibilidade_kwh=100), 100.0)

    def test_dimensionamento_solar(self):
        kwp = c.dimensionar_fv_kwp(500, 100, hsp=5.0, pr=0.8)
        # alvo 400 kWh / (5 x 0,8 x 30) = 3,33 kWp -> arredonda para cima em 0,1
        self.assertAlmostEqual(kwp, 3.4)
        self.assertGreaterEqual(c.geracao_mensal_kwh(kwp, 5.0, 0.8), 400)

    def test_dimensionamento_sem_consumo_acima_do_minimo(self):
        self.assertEqual(c.dimensionar_fv_kwp(80, 100, 4.6, 0.78), 0.0)

    def test_parametros_solares_invalidos(self):
        with self.assertRaises(ValueError):
            c.dimensionar_fv_kwp(500, 100, hsp=0, pr=0.8)
        with self.assertRaises(ValueError):
            c.geracao_mensal_kwh(3, 4.6, 1.5)

    def test_payback_interpolado(self):
        self.assertAlmostEqual(c.payback_anos(1000, [500, 500, 500]), 2.0)
        self.assertAlmostEqual(c.payback_anos(750, [500, 500]), 1.5)

    def test_payback_nao_recupera(self):
        self.assertIsNone(c.payback_anos(10000, [100, 100]))

    def test_fluxo_com_reajuste_e_degradacao(self):
        fluxo = c.fluxo_anual(1000, 3, reajuste_tarifa=0.10, degradacao=0.0)
        self.assertAlmostEqual(fluxo[0], 1000)
        self.assertAlmostEqual(fluxo[1], 1100)
        self.assertAlmostEqual(fluxo[2], 1210)

    def test_validacao_de_equipamento(self):
        eq = c.Equipamento("x", "x", "x", 1, 10, 25, 20, 0, (), "", True)
        with self.assertRaises(ValueError):
            c.validar_equipamento(eq)


class TestDados(unittest.TestCase):
    def test_arquivos_de_dados_carregam(self):
        p = c.carregar_premissas()
        eqs = c.carregar_equipamentos()
        self.assertGreater(len(eqs), 0)
        self.assertTrue(all(e.estimado for e in eqs), "dados estimados devem estar marcados")
        self.assertIn("tarifa", p)

    def test_todo_bloco_de_premissas_tem_origem(self):
        p = c.carregar_premissas()
        for nome, bloco in p.items():
            self.assertIn("_origem", bloco, f"bloco '{nome}' sem origem")


class TestAlternativas(unittest.TestCase):
    def setUp(self):
        self.p = c.carregar_premissas()
        self.eqs = c.carregar_equipamentos()

    def test_tres_alternativas_com_mesmo_horizonte(self):
        ctx = alt.comparar(self.p, self.eqs)
        self.assertEqual(len(ctx["resultados"]), 3)
        for r in ctx["resultados"]:
            self.assertEqual(len(r.fluxo), self.p["economia"]["horizonte_anos"])

    def test_alguma_alternativa_usa_fonte_renovavel(self):
        ctx = alt.comparar(self.p, self.eqs)
        self.assertTrue(any(r.potencia_fv_kwp > 0 for r in ctx["resultados"]))

    def test_economia_nao_negativa_e_custo_depois_menor(self):
        for r in alt.comparar(self.p, self.eqs)["resultados"]:
            self.assertGreaterEqual(r.economia_rs_mes, 0)
            self.assertLessEqual(r.custo_depois_rs_mes, r.custo_antes_rs_mes)

    def test_c_usa_sistema_solar_menor_que_b(self):
        _, b, cc = alt.comparar(self.p, self.eqs)["resultados"]
        self.assertLess(cc.potencia_fv_kwp, b.potencia_fv_kwp)

    def test_tarifa_maior_melhora_o_retorno(self):
        base = alt.comparar(self.p, self.eqs)["resultados"]
        p2 = copy.deepcopy(self.p)
        p2["tarifa"]["valor_rs_kwh"] *= 1.5
        caro = alt.comparar(p2, self.eqs)["resultados"]
        for r0, r1 in zip(base, caro):
            self.assertLess(r1.payback_anos, r0.payback_anos)

    def test_solar_sozinho_tem_efeito_climatico_pequeno(self):
        _, b, _ = alt.comparar(self.p, self.eqs)["resultados"]
        self.assertLess(abs(b.emissoes_evitadas_kg_ano), 50)

    def test_toda_alternativa_declara_limitacoes(self):
        for r in alt.comparar(self.p, self.eqs)["resultados"]:
            self.assertTrue(r.limitacoes)


class TestAssistente(unittest.TestCase):
    PERGUNTAS = [
        "quanto o espaço consome por mês?",
        "quanto gasta o computador?",
        "quanto gasta a lupa eletrônica?",
        "vale a pena trocar para LED?",
        "tomada inteligente compensa?",
        "vale a pena instalar energia solar?",
        "qual alternativa é a melhor?",
        "como entender minha conta de luz?",
        "quais são as fontes?",
        "ajuda",
    ]

    def test_toda_resposta_tem_estrutura_e_limitacoes(self):
        for pergunta in self.PERGUNTAS:
            texto = assistente.responder_energia(pergunta)
            for rotulo in ("Resposta:", "Como calculei:", "Limitações:", "Fontes:"):
                if pergunta == "ajuda":
                    continue
                self.assertIn(rotulo, texto, f"'{pergunta}' sem '{rotulo}'")
            self.assertIn("estimad", texto.lower(), f"'{pergunta}' não avisa que é estimativa")

    def test_perguntas_vazias_ou_invalidas_nao_quebram(self):
        for entrada in ["", "   ", None, 123, "asdfgh qwerty"]:
            self.assertIsInstance(assistente.responder_energia(entrada), str)

    def test_modo_acessivel_nao_usa_simbolos(self):
        texto = assistente.responder_energia("vale a pena instalar solar?", acessivel=True)
        self.assertNotIn("R$", texto)
        self.assertNotIn("kWh", texto)
        self.assertNotIn("kWp", texto)
        self.assertNotIn("%", texto)

    def test_modo_abreviado_mantem_siglas(self):
        texto = assistente.responder_energia("vale a pena instalar solar?", acessivel=False)
        self.assertIn("R$", texto)

    def test_resposta_coerente_com_a_analise(self):
        ctx = assistente.contexto()
        b = ctx["resultados"][1]
        texto = assistente.responder_energia("vale a pena instalar solar?", acessivel=False)
        self.assertIn(fmt_rs(b.investimento_rs), texto)
        self.assertIn(fmt_num(b.potencia_fv_kwp, 1), texto)

    def test_conta_de_luz_nao_confunde_com_lampada(self):
        texto = assistente.responder_energia("não entendo minha conta de luz")
        self.assertIn("disponibilidade", texto)

    def test_acentos_sao_ignorados(self):
        a = assistente.responder_energia("lampada led")
        b = assistente.responder_energia("lâmpada LED")
        self.assertEqual(a, b)


class TestFormatacao(unittest.TestCase):
    def test_numeros_brasileiros(self):
        self.assertEqual(fmt_num(1234.5, 1), "1.234,5")
        self.assertEqual(fmt_rs(1234.5), "R$ 1.234,50")
        self.assertEqual(fmt_num(-0.0001, 1), "0,0")

    def test_anos(self):
        self.assertEqual(fmt_anos(None), "não se paga no horizonte analisado")
        self.assertEqual(fmt_anos(1.5), "1 ano e 6 meses")
        self.assertEqual(fmt_anos(0.5), "6 meses")

    def test_falar(self):
        self.assertEqual(falar("R$ 12,50 por mês"), "12,50 reais por mês")
        self.assertIn("quilowatts-hora", falar("100 kWh"))
        self.assertIn("por cento", falar("5%"))


if __name__ == "__main__":
    unittest.main()
