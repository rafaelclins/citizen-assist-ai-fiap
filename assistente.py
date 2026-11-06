import csv
import json
import os
import re
import time
from datetime import datetime

from base_conhecimento import BaseConhecimento


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []

    def _verificar_dados_pessoais(self, texto):
        if "@" in texto:
            return True
        if re.search(r"\d{8,}", texto):
            return True
        return False

    def navegar(self):
        categorias = self.base.categorias()

        if not categorias:
            print("Nenhuma categoria disponível.")
            return

        print("\nCategorias disponíveis:")
        for indice, categoria in enumerate(categorias, start=1):
            print(f"  {indice}. {categoria}")
        print("  0. Voltar")

        escolha = input("Escolha uma categoria: ").strip()

        if escolha == "0":
            return

        if not escolha.isdigit() or not (1 <= int(escolha) <= len(categorias)):
            print("Opção inválida.")
            return

        categoria_escolhida = categorias[int(escolha) - 1]
        orientacoes = [o for o in self.base.orientacoes if o.categoria == categoria_escolhida]

        print(f"\nOrientações em '{categoria_escolhida}':")
        for indice, orientacao in enumerate(orientacoes, start=1):
            print(f"  {indice}. {orientacao.titulo}")
        print("  0. Voltar")

        escolha = input("Escolha uma orientação: ").strip()

        if escolha == "0":
            return

        if not escolha.isdigit() or not (1 <= int(escolha) <= len(orientacoes)):
            print("Opção inválida.")
            return

        orientacao_escolhida = orientacoes[int(escolha) - 1]
        orientacao_escolhida.exibir("MÉDIA", 3)

    def perguntar(self):
        pergunta = input("\nDigite sua dúvida (ou '0' para sair): ").strip()

        if pergunta == "0":
            return False

        while self._verificar_dados_pessoais(pergunta):
            print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
            pergunta = input("Digite sua dúvida (ou '0' para sair): ").strip()
            if pergunta == "0":
                return False

        inicio = time.time()
        resultados = self.base.buscar(pergunta)
        tempo_segundos = round(time.time() - inicio, 1)

        if resultados:
            pontos, melhor = resultados[0]
        else:
            pontos, melhor = 0, None

        if pontos >= 6:
            confianca = "ALTA"
        elif pontos >= 3:
            confianca = "MÉDIA"
        else:
            confianca = "NÃO ENCONTREI"

        if confianca == "NÃO ENCONTREI" or melhor is None:
            print("\nNão encontrei uma resposta para a sua dúvida.")
            print("Sugestão: use o menu de categorias para navegar pelas opções disponíveis.")
            id_orientacao = None
            encontrou = False
            ajudou = False
        else:
            melhor.exibir(confianca, pontos)
            id_orientacao = melhor.id
            encontrou = True

            resposta = input("Essa informação resolveu sua dúvida? (s/n): ").strip().lower()
            while resposta not in ("s", "n"):
                resposta = input("Resposta inválida. Digite 's' ou 'n': ").strip().lower()
            ajudou = resposta == "s"

        registro = {
            "data": datetime.now().isoformat(),
            "origem": "pergunta",
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": 1,
            "tempo_segundos": tempo_segundos,
        }
        self.historico.append(registro)

        return True

    def indicadores(self):
        total = len(self.historico)

        print("\n=== Indicadores ===")
        if total == 0:
            print("Nenhum atendimento registrado ainda.")
            return

        encontrados = sum(1 for r in self.historico if r["encontrou"])
        ajudaram = sum(1 for r in self.historico if r["ajudou"])
        tempo_medio = sum(r["tempo_segundos"] for r in self.historico) / total

        parte_encontrada = (encontrados / total) * 100
        parte_ajudou = (ajudaram / total) * 100

        print(f"Respostas encontradas: {parte_encontrada:.1f}%")
        print(f"Taxa de acerto (ajudou): {parte_ajudou:.1f}%")
        print(f"Tempo médio: {tempo_medio:.1f} segundos")

        sem_solucao = [r["pergunta"] for r in self.historico if not r["ajudou"]]
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("  (nenhuma)")

    def exportar_csv(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou", "ajudou", "tentativas", "tempo_segundos"]
        for registro in self.historico:
            for chave in registro:
                if chave not in campos:
                    campos.append(chave)

        with open(os.path.join("data", "atendimentos.csv"), "w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos, extrasaction="ignore")
            escritor.writeheader()
            for registro in self.historico:
                escritor.writerow(registro)

        with open(os.path.join("data", "historico.json"), "w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)

        print("Histórico exportado para data/atendimentos.csv e data/historico.json.")
