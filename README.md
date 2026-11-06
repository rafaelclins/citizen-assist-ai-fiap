# Citizen Assist AI - Transporte Gratuito

Assistente em linha de comando para orientar cidadãos sobre direitos de **transporte gratuito** (estudantes, idosos, PCD e assistência social), com base em uma base de conhecimento curada e verificada.

---

## Equipe

| Nome | RM |
| --- | --- |
| Eric dos Santos Mendes da Silva | 569528 |
| Rafael Côrtes Lins | 570588 |
| Tom Stringasci Albuquerque Coelho Morais | 568844 |

**Sala:** 1CCPI

---

## Público e Problema

**Público-alvo:** cidadãos que buscam informações sobre gratuidade no transporte — estudantes, idosos, pessoas com deficiência (PCD) e beneficiários de programas de assistência social.

**Problema:** a informação sobre esses direitos costuma estar **espalhada em diversos sites e escrita em linguagem técnica**, o que dificulta o acesso de quem mais precisa. O Citizen Assist AI centraliza esse conteúdo em respostas objetivas, com documentos necessários, local de atendimento e fonte oficial.

---

## ODS Relacionadas

- **ODS 10 — Redução das Desigualdades:** facilita o acesso a direitos de mobilidade para grupos vulneráveis.
- **ODS 11 — Cidades e Comunidades Sustentáveis:** incentiva o uso do transporte público ao simplificar o acesso à gratuidade.

---

## Como Executar

Pré-requisitos: **Python 3.8+** (sem dependências externas).

```bash
python main.py
```

O programa abre um menu com as opções:

1. Fazer uma pergunta
2. Navegar por categorias
3. Ver indicadores e sair

Na opção 3, o sistema exibe os indicadores, exporta o histórico e solicita uma nota de facilidade de 1 a 5.

---

## Regra de Pontuação

Ao fazer uma pergunta, o sistema normaliza o texto (minúsculas, sem acentos e sem pontuação) e calcula uma pontuação para cada orientação:

- **+3 pontos** para cada **palavra-chave** da orientação presente na pergunta.
- **+1 ponto** para cada palavra da pergunta (com **4 letras ou mais**) presente no **título** da orientação.

A pontuação total define o nível de confiança da resposta:

| Pontuação | Confiança |
| --- | --- |
| **>= 6** | ALTA |
| **3 a 5** | MÉDIA |
| **< 3** | NÃO ENCONTREI |

A orientação com maior pontuação é exibida ao usuário. Quando a confiança é "NÃO ENCONTREI", o assistente sugere navegar pelo menu de categorias.

---

## Estrutura de Arquivos

```
.
├── main.py                 # Ponto de entrada e menu principal
├── assistente.py           # Classe Assistente (perguntas, navegação, indicadores, exportação)
├── base_conhecimento.py    # Classe BaseConhecimento (carrega o JSON, normaliza e busca)
├── orientacao.py           # Classe Orientacao (modelo de dados e exibição formatada)
├── README.md
└── data/
    ├── base_conhecimento.json   # Base de conhecimento (10 orientações, 4 categorias)
    ├── atendimentos.csv         # Gerado ao sair (histórico tabular)
    └── historico.json           # Gerado ao sair (histórico completo em JSON)
```

---

## Teste com Usuários

> **Placeholder — preencher com os resultados dos testes reais com 3 pessoas.**

### Teste 1

- **Perfil do participante:** _(ex.: estudante, 19 anos)_
- **Dúvida testada:** _(ex.: como tirar o passe livre estudantil)_
- **Resultado:** _(encontrou a resposta? a nota de facilidade foi X/5?)_
- **Observações:** _(comentários do participante)_

### Teste 2

- **Perfil do participante:** _(ex.: aposentado, 68 anos)_
- **Dúvida testada:** _(ex.: gratuidade para idosos)_
- **Resultado:** _(...)_
- **Observações:** _(...)_

### Teste 3

- **Perfil do participante:** _(ex.: pessoa com deficiência)_
- **Dúvida testada:** _(ex.: passe livre federal para PCD)_
- **Resultado:** _(...)_
- **Observações:** _(...)_

### Melhoria feita a partir do teste

> _Descreva aqui uma melhoria implementada com base no feedback dos usuários._ _(ex.: após um usuário escrever a dúvida com acentos e pontuação variados, reforçamos a normalização de texto para tornar a busca mais tolerante.)_

---

## Limitações

- O assistente depende **estritamente do arquivo `data/base_conhecimento.json`**. Se a base não for atualizada, as respostas ficam desatualizadas.
- **Não utiliza IA generativa real.** A busca é feita por **correspondência de palavras-chave** e regras simples de pontuação, conforme exigido na disciplina de **PCP (Pensamento Computacional / Projeto de Computação)**.
- As respostas são orientativas e **não substituem os canais oficiais** dos órgãos públicos.
- A base atual cobre 4 categorias e 10 orientações, podendo ser expandida manualmente.

> **Aviso:** este assistente NÃO é um canal oficial.
