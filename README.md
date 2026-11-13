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

Foram realizados testes com 3 pessoas de fora da equipe, totalizando 12 atendimentos no terminal. Abaixo estão os destaques de cada perfil:

### Teste 1
- **Perfil do participante:** Maria, 68 anos, aposentada.
- **Dúvida testada:** "Tenho 68 anos, preciso pagar passagem no domingo?"
- **Resultado:** Encontrou a resposta com confiança ALTA (7 pontos). O sistema identificou corretamente os termos "anos" (idade) e "domingo".
- **Observações:** A usuária ficou surpresa com a resposta, pois achava que a gratuidade valia para todos os dias. Ela elogiou o aviso claro sobre a Portaria 047/2025 e a formatação legível no terminal.

### Teste 2
- **Perfil do participante:** João, 19 anos, estudante universitário.
- **Dúvida testada:** "Como consigo gratuidade no transporte sendo estudante?"
- **Resultado:** Encontrou a resposta com confiança MÉDIA (4 pontos). O sistema identificou "estudante" e "gratuidade", mas não "passe livre" nesta formulação específica.
- **Observações:** O usuário achou a lista de documentos necessária muito clara. Porém, comentou que a palavra "gratuidade" é mais natural para ele do que "passe livre", e que o sistema demorou um pouco para dar a nota máxima de confiança nessa pergunta.

### Teste 3
- **Perfil do participante:** Carlos, 35 anos, pessoa com deficiência (usuário de cadeira de rodas).
- **Dúvida testada:** "Meu acompanhante paga passagem se eu for cadeirante?"
- **Resultado:** Encontrou a resposta com confiança ALTA (6 pontos). O sistema identificou "acompanhante" e fez a ligação com a categoria PCD.
- **Observações:** O participante achou a resposta precisa. No entanto, notou que ao digitar apenas "cadeirante" em um primeiro momento, o sistema não deu uma boa pontuação, exigindo que ele usasse o termo "pcd" ou "deficiência" para obter a resposta ideal.

---

### Melhoria feita a partir do teste

Com base no feedback dos testes 2 e 3, foi realizada uma **expansão das palavras-chave** no arquivo `data/base_conhecimento.json` para tornar a busca por pontuação mais tolerante a variações da linguagem natural:

1. Na orientação de **Estudantes (ID 1)**, adicionamos `"gratuidade"` e `"desconto"` ao array de `palavras_chave`.
2. Na orientação de **PCD (ID 6 e 7)**, adicionamos `"cadeirante"` e `"mobilidade reduzida"` ao array de `palavras_chave`.

**Resultado da melhoria:** Após a atualização, a pergunta *"Como consigo gratuidade no transporte sendo estudante?"* passou a atingir **confiança ALTA (7 pontos)**, e o termo *"cadeirante"* agora é corretamente mapeado para as regras de acompanhante de PCD, resolvendo as dúvidas que antes retornavam com confiança baixa ou sugeriam apenas a navegação por categorias.
---

## Limitações

- O assistente depende **estritamente do arquivo `data/base_conhecimento.json`**. Se a base não for atualizada, as respostas ficam desatualizadas.
- **Não utiliza IA generativa real.** A busca é feita por **correspondência de palavras-chave** e regras simples de pontuação, conforme exigido na disciplina de **PCP (Pensamento Computacional / Projeto de Computação)**.
- As respostas são orientativas e **não substituem os canais oficiais** dos órgãos públicos.
- A base atual cobre 4 categorias e 10 orientações, podendo ser expandida manualmente.

> **Aviso:** este assistente NÃO é um canal oficial.
