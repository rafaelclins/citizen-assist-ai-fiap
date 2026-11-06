import json

from orientacao import Orientacao


class BaseConhecimento:
    ACENTOS = {
        "á": "a", "à": "a", "ã": "a", "â": "a", "ä": "a",
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i", "ï": "i",
        "ó": "o", "ò": "o", "õ": "o", "ô": "o", "ö": "o",
        "ú": "u", "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
        "Á": "a", "À": "a", "Ã": "a", "Â": "a", "Ä": "a",
        "É": "e", "È": "e", "Ê": "e", "Ë": "e",
        "Í": "i", "Ì": "i", "Î": "i", "Ï": "i",
        "Ó": "o", "Ò": "o", "Õ": "o", "Ô": "o", "Ö": "o",
        "Ú": "u", "Ù": "u", "Û": "u", "Ü": "u",
        "Ç": "c",
    }

    PONTUACAO = "?!.,;:()"

    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def normalizar(self, texto):
        texto = texto.lower()

        texto = "".join(self.ACENTOS.get(char, char) for char in texto)

        for char in self.PONTUACAO:
            texto = texto.replace(char, " ")

        return " ".join(texto.split())

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Aviso: arquivo '{self.caminho}' não encontrado. Iniciando base vazia.")
            dados = []
        except json.JSONDecodeError:
            print(f"Aviso: arquivo '{self.caminho}' inválido. Iniciando base vazia.")
            dados = []

        for item in dados:
            orientacao = Orientacao(
                id=item["id"],
                categoria=item["categoria"],
                titulo=item["titulo"],
                palavras_chave=item["palavras_chave"],
                resposta=item["resposta"],
                documentos=item["documentos"],
                onde=item["onde"],
                fonte=item["fonte"],
                verificado_em=item["verificado_em"],
            )
            self.orientacoes.append(orientacao)

        return self.orientacoes

    def categorias(self):
        return list({orientacao.categoria for orientacao in self.orientacoes})

    def buscar(self, pergunta):
        pergunta_normalizada = self.normalizar(pergunta)
        palavras_pergunta = pergunta_normalizada.split()

        resultados = []

        for orientacao in self.orientacoes:
            pontos = 0

            for palavra_chave in orientacao.palavras_chave:
                palavra_chave_normalizada = self.normalizar(palavra_chave)
                if palavra_chave_normalizada in pergunta_normalizada:
                    pontos += 3

            titulo_normalizado = self.normalizar(orientacao.titulo)
            for palavra in palavras_pergunta:
                if len(palavra) >= 4 and palavra in titulo_normalizado:
                    pontos += 1

            resultados.append((pontos, orientacao))

        resultados.sort(key=lambda item: item[0], reverse=True)

        return resultados
