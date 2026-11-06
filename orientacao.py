class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self, confianca, pontos):
        documentos_formatados = "\n".join(f"  - {doc}" for doc in self.documentos)

        print("=" * 60)
        print(f"{self.titulo}")
        print(f"Categoria: {self.categoria}")
        print("=" * 60)
        print(f"Confiança: {confianca} ({pontos} pontos)")
        print()
        print(f"Resposta: {self.resposta}")
        print()
        print("Documentos necessários:")
        print(documentos_formatados)
        print()
        print(f"Onde ir: {self.onde}")
        print(f"Fonte: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print()
        print("Aviso: este assistente NÃO é um canal oficial.")
        print("=" * 60)
