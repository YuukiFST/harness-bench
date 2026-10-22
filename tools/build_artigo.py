# -*- coding: utf-8 -*-
"""Build dist/artigo-cientifico.docx, the article version of the research project.

The research project (`dist/projeto-de-pesquisa.docx`) is concluded and frozen.
The article reuses its prose almost verbatim and reshapes it to the course's
article handout (`files/Aula Formatacao de artigos com modelos metodologia.pdf`):

- A4, margins 3 cm top/left and 2 cm bottom/right, Times New Roman 12,
  1.5 line spacing, 1.25 cm first-line indent, justified text, page number
  bottom right;
- title centred, upper case, bold, 14 pt, subtitle in lower case;
- authors under the title, each with a footnote (course, unit, e-mail);
- resumo and abstract in one paragraph, 10 pt, single spacing, up to 250 words,
  followed by 3 to 6 keywords separated by full stops;
- introducao, referencial teorico, material e metodo, resultados e discussao,
  consideracoes finais, referencias (12 pt, left, single, 6 pt before/after).

Orcamento and cronograma belong to the project only and are dropped. The
results section reports Layer 1 (`docs/spec/41-layer1-request-shape.md`,
`layer1/data/report.md`), the only measurement taken so far.

Unlike the project, which is edited in place with `tools/docx_prose.py`, the
article is generated: edit the text below and rerun

    python tools/build_artigo.py

Markup inside text: *italic*, **bold**, [[FN1]] / [[FN2]] footnote references.
"""
from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DST = ROOT / "dist" / "artigo-cientifico.docx"

TEXT_WIDTH = 9071  # 21 cm - 3 cm - 2 cm, in twips
INDENT = 709       # 1.25 cm
QUOTE_INDENT = 2268  # 4 cm, long quotation (NBR 10520)

TITLE = ("O *HARNESS* NO CUSTO E NO DESEMPENHO DE AGENTES DE CODIFICAÇÃO: "
         "tokens e taxa de sucesso com o mesmo modelo")

AUTHORS = [
    "Fausto Yuuki T.A Freire[[FN1]]",
    "Inara Silva[[FN2]]",
]

FOOTNOTES = {
    1: ("Discente do Curso de Sistemas para Internet – Departamento de Área de "
        "Informática – Instituto Federal de Educação, Ciência e Tecnologia de "
        "Mato Grosso – Campus Cuiabá Cel. Octayde Jorge da Silva, Rua Profa. "
        "Zulmira Canavarros, 95 – CEP: 78005-200. faustoyuuki@gmail.com"),
    2: ("Professora orientadora – Departamento de Área de Informática – "
        "Instituto Federal de Educação, Ciência e Tecnologia de Mato Grosso – "
        "Campus Cuiabá Cel. Octayde Jorge da Silva. inara.ferrer@ifmt.edu.br"),
}

RESUMO = (
    "Um agente de codificação tem duas partes: o modelo de linguagem e o *harness*, "
    "o software que monta o contexto, expõe as ferramentas e conduz a "
    "execução. Medições recentes indicam que, com o mesmo modelo, a escolha do *harness* "
    "muda pouco a taxa de sucesso e muito o custo, mas usam tarefas isoladas de "
    "*benchmarks*. Este artigo apresenta um experimento que mede, com o modelo fixo, a "
    "diferença de tokens e de taxa de sucesso atribuível ao *harness* na construção de um "
    "mesmo produto, o Finn, um SaaS financeiro por voz. A pesquisa é aplicada, "
    "quali-quantitativa, exploratória e experimental. O OpenCode e o Pi constroem o Finn "
    "do zero a partir da mesma especificação, extraída de uma versão de referência feita "
    "pelo autor e dividida em unidades. Um *proxy* reverso conta os tokens "
    "da mesma forma para os dois, testes de aceitação escritos antes da execução "
    "definem o sucesso, e o teste de Wilcoxon pareado por unidade compara os tokens em "
    "dois níveis de modelo. A primeira camada da medição, sem tarefa real e contra um "
    "*endpoint* simulado, mostrou que a primeira requisição do OpenCode tem 6.659 tokens, "
    "contra 1.228 do Pi, cerca de cinco vezes mais, quase toda em esquemas de ferramenta e "
    "*system prompt*. O OpenCode também faz uma chamada extra ao modelo, para gerar o "
    "título da sessão. Esses números são compatíveis com a hipótese de que a carga fixa "
    "por requisição explica a maior parte da diferença de custo, o que a construção "
    "completa vai testar."
)
PALAVRAS_CHAVE = ("Inteligência artificial. Engenharia de software. OpenCode. Pi. "
                  "Experimento controlado.")

ABSTRACT = (
    "A coding agent has two parts: the language model and the *harness*, the software "
    "that builds the context, exposes the tools and drives the execution. Recent "
    "measurements indicate that, with the same model, the choice of *harness* changes the "
    "success rate little and the cost a great deal, but they rely on isolated *benchmark* "
    "tasks. This article presents an experiment that measures, with the model held fixed, "
    "the difference in tokens and success rate attributable to the *harness* when building "
    "the same product, Finn, a voice-driven finance SaaS. The research is applied, "
    "mixed-methods, exploratory and experimental. OpenCode and Pi build Finn from scratch "
    "from the same specification, extracted from a reference build made by the author and "
    "split into units. A reverse proxy counts tokens in the same way "
    "for both, acceptance tests written before the runs define success, and a Wilcoxon "
    "signed-rank test paired by unit compares the tokens at two model tiers. The first "
    "measurement layer, with no real task and against a mock endpoint, showed that "
    "OpenCode’s first request carries 6,659 tokens against Pi’s 1,228, about five times "
    "as many, almost all of them in tool schemas and system prompt. OpenCode also makes "
    "an extra model call to generate the session title. These figures are consistent with "
    "the hypothesis that the fixed per-request load explains most of the cost difference, "
    "which the full construction will test."
)
KEYWORDS = "Artificial intelligence. Software engineering. OpenCode. Pi. Controlled experiment."

# (kind, text). kinds: h = section heading, p = body paragraph, q = long quotation,
# table = Tabela 1, src = table source line.
BODY = [
    ("h", "1 INTRODUÇÃO"),
    ("p", "Um *coding agent* tem duas partes: o modelo de linguagem e o *harness*, o software "
          "ao redor dele que monta o contexto, expõe as ferramentas e conduz a execução. Pan "
          "*et al.* (2026), da Universidade da Califórnia em Berkeley, avaliaram sete modelos "
          "em três *harnesses* e concluíram que a escolha do *harness* influencia notavelmente "
          "o custo. No SWE-bench Lite, o Fable 5 resolve 97,8% das tentativas no Claude Code e "
          "96,7% no Pi, e o Claude Code custa aproximadamente o dobro por tentativa (US$ 1,33 "
          "contra US$ 0,67)."),
    ("p", "Quem paga por tokens paga também essa diferença. Essas medições usam tarefas "
          "isoladas de *benchmarks* que os modelos podem ter visto no treino, e os próprios "
          "autores apontam como próximo passo medir o *harness* em fluxos reais de "
          "desenvolvimento, com tarefas de várias sessões. Este trabalho constrói o mesmo "
          "produto com o OpenCode e com o Pi, sobre o mesmo modelo e a mesma especificação, e "
          "conta os tokens fora do *harness*. O produto é o Finn, um SaaS voltado para o setor "
          "financeiro das empresas."),
    ("p", "O tema é o efeito do *harness* sobre o custo e o desempenho de um modelo de "
          "linguagem fixo na construção de um produto de software completo. O problema é: com "
          "o mesmo modelo, quanto a escolha do *harness* influencia o custo e a taxa de "
          "sucesso na construção do mesmo software?"),
    ("p", "O objetivo geral é medir, com o mesmo modelo, a diferença de tokens e de taxa de "
          "sucesso atribuível ao *harness* na construção do mesmo produto a partir da mesma "
          "especificação, com o OpenCode e o Pi como *coding agents*, e separar a parcela que "
          "vem da carga fixa por requisição. Os objetivos específicos são: (1) construir o "
          "*proxy* que conta requisições, tokens e latência por *coding agent*; (2) construir "
          "o Finn de referência e extrair dele a especificação e os testes; (3) construir o "
          "Finn nos dois *harnesses*, com o mesmo modelo, *prompt* e espaço inicial; (4) "
          "repetir em um segundo modelo e verificar se a ordenação dos *coding agents* se "
          "mantém; (5) comparar os tokens relatados por cada *harness* com os medidos no "
          "*proxy*; (6) publicar executor, *prompts*, testes, dados e scripts de análise."),
    ("p", "H1: com o modelo fixo, o *harness* muda mais o custo do que o sucesso. Os tokens "
          "por unidade diferem entre o OpenCode e o Pi, e a fração de testes aprovados fica "
          "igual. H1 será refutada se o teste pareado não apontar diferença de tokens ou se as "
          "medianas da fração final de testes aprovados diferirem entre os *coding agents*."),
    ("p", "H2: a carga fixa por requisição (*system prompt* e esquemas de ferramenta) explica "
          "a maior parte da diferença de tokens, e o número de passos explica a menor. H2 será "
          "refutada se os passos ou o conteúdo da conversa explicarem a maior parte."),
    ("p", "Um *proxy* reverso entre cada *harness* e o modelo contará requisições, tokens e "
          "latência da mesma forma para os dois *coding agents*. Cada *coding agent* "
          "construirá o Finn do zero ao menos três vezes, a partir da especificação extraída "
          "do Finn de referência do autor, e a diferença entre os *coding agents* será "
          "comparada unidade a unidade."),
    ("p", "Após esta introdução, a seção 2 apresenta o referencial teórico e a seção 3, o "
          "material e método. A seção 4 traz os resultados da primeira camada de medição e a "
          "seção 5, as considerações finais."),

    ("h", "2 REFERENCIAL TEÓRICO"),
    ("p", "Segundo Ning *et al.* (2026, p. 7, tradução nossa), um *harness* “converte um "
          "modelo de linguagem sem estado em um agente funcional ao ancorar suas saídas em "
          "execução externa, estado persistente e realimentação verificável”. Lin *et al.* "
          "(2026) delimitam essa camada:"),
    ("q", "Na prática, esse progresso depende não apenas do modelo de linguagem subjacente, "
          "mas igualmente dos componentes de engenharia que o cercam: o *system prompt* que "
          "molda o estilo de trabalho, as ferramentas que expõem o sistema de arquivos e o "
          "shell, e o middleware que controla contexto, execução e recuperação. Esse conjunto "
          "de componentes externos ao modelo e editáveis é chamado coletivamente de *harness* "
          "do agente. (Lin *et al.*, 2026, p. 1, tradução nossa)."),
    ("p", "Avaliar um agente é avaliar o *harness* e o modelo juntos (Grace *et al.*, 2026). "
          "Por isso só esse conjunto varia entre os *coding agents* deste experimento. O Pi "
          "envia quatro ferramentas e um *system prompt* curto (Earendil, 2026), e o OpenCode "
          "envia mais ferramentas, subagentes e permissões (Opencode, 2026a)."),
    ("p", "Na Tabela 1 de Lin *et al.* (2026), *harnesses* escritos por humanos vão de 47,2% "
          "de aprovação no OpenCode a 71,9% no Codex, no Terminal-Bench 2. Zhang *et al.* "
          "(2026) sustentam que, em tarefas longas e entre modelos de fronteira comparáveis, a "
          "variação de desempenho devida ao *harness* é frequentemente comparável ou maior que "
          "a devida ao modelo. Pan *et al.* (2026) mediram outra coisa no SWE-bench Lite: o "
          "efeito médio do *harness* sobre a taxa de sucesso ficou dentro de ±2%, enquanto o "
          "Claude Code custou, em média, cerca de 2,0 vezes o Pi. Em Jin *et al.* (2026), no "
          "SWE-bench Verified de 500 tarefas, trocar o mini-SWE-agent pelo HERMES, com o "
          "GPT-5.6 Sol, levou a resolução de 96,20% para 97,00% e o custo por tarefa de "
          "US$ 1,15 para US$ 1,80. Com o GPT-5 Mini, a resolução subiu de 60,80% para "
          "80,20%."),
    ("p", "No Terminal-Bench 2.0, com 89 tarefas e ao menos cinco execuções por par, o Gemini "
          "2.5 Pro resolveu 32,6% das tarefas no Terminus 2 e 15,7% no OpenHands, mas os "
          "autores concluem que o modelo costuma pesar mais que o *harness* (Merrill *et al.*, "
          "2026). Entre o OpenCode e o Pi, o DeepSeek-AI (2026) obteve 85,0% e 86,1% no "
          "Terminal-Bench v2.1 com o DeepSeek-V4.1-Flash, e Furgale *et al.* (2026), 52,8% e "
          "75,3% no Terminal-Bench 2.0 com o GPT-5.5. Como as fontes divergem sobre o sucesso, este "
          "trabalho mede sucesso e custo juntos."),
    ("p", "A primeira pendência é saber de onde vem a diferença de custo. Para Pan *et al.* "
          "(2026), o imposto do *harness* pode começar na primeira requisição: nos sete "
          "modelos, o contexto inicial médio do Claude Code passa de dez vezes o do Pi, e no "
          "Claude Fable 5 os turnos quase se igualam (15,3 contra 15,4). Liu *et al.* (2026) "
          "apontam o resto da conversa. Mudando só a execução das ações, a compactação de "
          "contexto, o tratamento das observações e a leitura delegada, cortaram de 44,7% a "
          "49,0% dos tokens em relação ao Pi e mantiveram de 93,7% a 94,3% da pontuação dele."),
    ("p", "O gerenciamento de contexto, sozinho, também muda custo e sucesso com o modelo fixo. "
          "No SWE-agent com o Qwen3-Coder 480B, mascarar observações antigas baixou o custo "
          "por tarefa de US$ 1,29 para US$ 0,61 nas 500 tarefas do SWE-bench Verified "
          "(Lindenbauer *et al.*, 2025). Com o Claude 4 Sonnet, o gerenciamento de contexto "
          "elevou a resolução de 42,0% para 48,6% em 100 tarefas do SWE-Bench Pro (Wong "
          "*et al.*, 2025). Ning *et al.* (2026, p. 66, tradução nossa) pedem “métricas que isolem componentes "
          "do *harness*”, e H2 testa se pesa mais a carga fixa ou a conversa."),
    ("p", "A segunda pendência é a instrumentação. Cada *harness* conta turnos e tokens do seu "
          "jeito, e Pan *et al.* (2026) registram que a definição de turno varia entre eles. "
          "Aqui a medição ocorre em um *proxy* externo, igual para os dois *coding agents*, e "
          "o objetivo (5) compara essa medida com o relato de cada *harness*."),
    ("p", "As métricas serão tokens por construção, ao lado da fração de testes aprovados, e o "
          "Succ/Mtok (sucessos por milhão de tokens) de Lin *et al.* (2026). O efeito também "
          "depende do modelo, pois em nove de doze comparações de Pan *et al.* (2026) o maior "
          "sucesso veio de um *harness* que não é o do fornecedor do modelo. Por isso o "
          "desenho terá dois níveis de modelo."),

    ("h", "3 MATERIAL E MÉTODO"),
    ("p", "A pesquisa é aplicada quanto à finalidade, quali-quantitativa quanto à abordagem, "
          "exploratória quanto aos objetivos, experimental quanto aos procedimentos e dedutiva "
          "quanto ao método. É exploratória porque não se encontrou comparação publicada de "
          "*harnesses* construindo o mesmo produto completo. O *harness* é a variável "
          "manipulada, e modelo, especificação, espaço de trabalho inicial e limites ficam "
          "controlados."),
    ("p", "Declara-se o uso do Claude Code no levantamento das fontes, organizado pelo método "
          "*LLM Wiki* de Karpathy (2026) no repositório do projeto (YuukiFST, 2026c), nas "
          "decisões do Finn, mapeadas com o Helmsman (YuukiFST, 2026a), e na sua versão de "
          "referência. O autor conferiu cada afirmação citada na obra e responde pelo texto e "
          "pelas decisões de produto."),
    ("p", "A medição terá duas camadas. A Camada 1 mede, contra um *endpoint* simulado, os "
          "esquemas de ferramenta, o *system prompt* e os tokens de cada requisição, ou seja, "
          "a carga fixa de cada *coding agent* sem tarefa. A Camada 2 mede a construção contra "
          "o modelo real."),
    ("p", "Os *coding agents* serão o OpenCode (Opencode, 2026a) e o Pi (Earendil, 2026). Os "
          "dois são de código aberto (Opencode, 2026a; Pan *et al.*, 2026). As versões serão "
          "fixadas e registradas no repositório (YuukiFST, 2026c). A coleta roda em um PC "
          "pessoal com NixOS, e a inferência usa o nível gratuito do *gateway*, sem custo "
          "financeiro."),
    ("p", "O produto será o Finn, SaaS multiempresa em que a empresa cliente fala com o "
          "próprio financeiro por voz e recebe lançamento, relatório e aviso no celular "
          "(YuukiFST, 2026b), decidido em 24 *tickets*. O autor construirá antes uma versão de "
          "referência e marcará no git o fim de cada etapa. Dela sairá a especificação, "
          "congelada por SHA-256: produto, pilha, interface dos testes e funcionalidades em "
          "JSON, no formato de Young (2025), uma unidade por etapa, ao menos seis. O executor "
          "chama o *harness* uma vez por unidade, com o mesmo *prompt* nos dois *coding "
          "agents*, e cada unidade parte do que o agente construiu na anterior. Nenhum código "
          "do autor entra no espaço de trabalho."),
    ("p", "A pontuação será a fração dos testes de aceitação aprovados. O autor escreverá os "
          "testes antes da execução, fora do espaço de trabalho, e os rodará sobre uma cópia "
          "dele ao fim de cada unidade. Todos devem passar antes na referência, no marco da "
          "etapa. Os testes escritos pelo agente não contam, e uma unidade conta como "
          "concluída quando todos os seus testes passam."),
    ("p", "Serão dois níveis de modelo, primário e de robustez, ambos gratuitos no mesmo "
          "*gateway* (Opencode, 2026b), com resultados relatados por nível. Se a ordenação dos "
          "*coding agents* inverter de um nível para o outro, a inversão será reportada como "
          "resultado."),
    ("p", "O *proxy* guardará os tokens que o *gateway* informa em cada resposta, com o cache "
          "à parte, e separará em cada requisição a carga fixa (*system prompt* e ferramentas) "
          "do resto da conversa, para H2. A contagem do *harness* serve só para verificação "
          "cruzada."),
    ("p", "Haverá um único limite, igual para os dois *coding agents*: tempo de relógio por "
          "unidade, de três vezes a maior mediana dos *coding agents* nas unidades-piloto. O "
          "número de passos fica livre, porque um teto de passos é decisão de projeto de "
          "*harness* e apagaria a diferença sob teste."),
    ("p", "Cada combinação de *coding agent* e nível terá ao menos três construções completas "
          "válidas, relatadas em mediana e dispersão. A comparação usará o teste de Wilcoxon "
          "dos postos sinalizados, bilateral, α = 0,05, sobre tokens e Succ/Mtok, pareado por "
          "unidade. O pareamento remove a dificuldade comum aos dois *coding agents* (Miller, "
          "2024). O resultado principal será a razão entre as medianas de tokens por "
          "construção dos *coding agents*. A fração de testes aprovados será relatada sem "
          "teste, pois um empate em 100% não deixa diferença a testar. As predições serão "
          "registradas antes da coleta."),
    ("p", "Unidade não concluída conta como resultado, com a fração de testes aprovados, e a "
          "construção segue. Medição não confiável, como a troca do modelo servido no meio da "
          "coleta, descarta a construção inteira."),

    ("h", "4 RESULTADOS E DISCUSSÃO"),
    ("p", "A Camada 2 ainda não foi executada, pois depende do Finn de referência e dos testes "
          "de aceitação. Esta seção traz a Camada 1, medida em 28 de agosto de 2026 com o "
          "OpenCode 1.17.9 e o Pi 0.80.10 (YuukiFST, 2026c). Os dois receberam a mesma tarefa "
          "de sondagem, um *prompt* de 83 bytes que pede para ler um arquivo curto e resumi-lo "
          "em uma frase, contra um *endpoint* simulado e determinístico. Os tokens foram "
          "contados com o tokenizador cl100k_base, que serve para comparar os *coding agents* "
          "entre si e não substitui a contagem do *gateway*."),
    ("table", "Tabela 1 – Primeira requisição de cada *coding agent* na Camada 1"),
    ("src", "Fonte: elaborado pelo autor com dados de YuukiFST (2026c)."),
    ("p", "Antes de fazer qualquer trabalho, o OpenCode envia cerca de cinco vezes os tokens do "
          "Pi (Tabela 1). Os esquemas de ferramenta e o *system prompt* somam 99,2% dos bytes "
          "do OpenCode e 95,1% dos do Pi. A conversa, a única parte que vem da tarefa, tem "
          "quase o mesmo tamanho nos dois."),
    ("p", "Nos cinco primeiros passos, os dois reenviam o histórico inteiro, e cada passo "
          "acrescenta um valor constante: 698 bytes no OpenCode e 555 no Pi. No quinto passo, a "
          "requisição do OpenCode tem 32.789 bytes e a do Pi, 7.896. Da diferença de 24.893 "
          "bytes, 97,7% já estava na primeira requisição, ou seja, vem da carga fixa e se "
          "repete a cada passo."),
    ("p", "O OpenCode faz ainda uma chamada ao modelo sem ferramentas, de 2.526 bytes, para "
          "gerar o título da sessão antes da tarefa. Essa chamada não aparece no relato do "
          "próprio *harness*. Chamadas assim são o motivo de o objetivo (5) comparar a "
          "contagem do *proxy* com o relato de cada *harness*."),
    ("p", "Os números concordam com Pan *et al.* (2026), para quem o imposto do *harness* pode "
          "começar na primeira requisição, e são compatíveis com H2. Eles ainda não testam H2. "
          "A Camada 1 tem uma única tarefa curta, sem modelo real, e o número de passos de uma "
          "construção pode ser outro. Se os dois *coding agents* precisarem de números de "
          "passos parecidos, a carga fixa deve responder pela maior parte da diferença de "
          "tokens. Se o Pi precisar de muito mais passos, a vantagem inicial pode se perder. "
          "Furgale *et al.* (2026) registraram esse caso no SWE-bench Verified com o GPT-5.5 "
          "(esforço xhigh). "
          "O Pi 0.72.1 fez 66 chamadas e gastou 2,2 milhões de tokens por tarefa para 78,2% "
          "de acerto, e o OpenCode 1.14.33, 1,3 milhão para 78,6%."),

    ("h", "5 CONSIDERAÇÕES FINAIS"),
    ("p", "Este trabalho partiu da constatação de que, com o mesmo modelo, o *harness* pode "
          "mudar o custo de um *coding agent* sem mudar muito a taxa de sucesso, e de que as "
          "medições disponíveis usam tarefas isoladas de *benchmarks*. Para medir esse efeito na "
          "construção de um produto completo, o artigo propôs um experimento em que o OpenCode "
          "e o Pi constroem o Finn a partir da mesma especificação, com os tokens contados em "
          "um *proxy* externo e o sucesso decidido por testes de aceitação escritos antes da "
          "execução."),
    ("p", "O objetivo geral ainda não foi atingido, porque depende da Camada 2. Até aqui, o "
          "trabalho definiu o protocolo e mediu a carga fixa dos dois *coding agents* em uma "
          "tarefa de sondagem, e o repositório já publica o instrumento e os dados dessa "
          "medição (YuukiFST, 2026c). Nessa medição, o OpenCode enviou cerca de cinco vezes os "
          "tokens do Pi na primeira requisição. H1 e H2 continuam abertas."),
    ("p", "O projeto tem quatro limitações. O efeito do *harness* depende do modelo, então as "
          "conclusões valem por nível. O produto é um único SaaS, especificado a partir da "
          "solução do autor. Cada *coding agent* carrega os próprios erros de uma unidade à "
          "seguinte, então as unidades não são independentes, embora o teste de Wilcoxon "
          "suponha que sejam; o valor-p será lido como indicativo, ao lado da diferença e da "
          "dispersão. Por fim, o nível gratuito do *gateway* pode trocar o modelo ou cortar a "
          "cota durante a coleta. A Camada 1, por sua vez, usou uma única tarefa e uma única "
          "máquina, e as razões da Tabela 1 valem só para ela."),
    ("p", "Como trabalhos futuros, além da Camada 2, sugere-se repetir o experimento com outros "
          "produtos e outros *harnesses* e medir quanto cada componente do *harness* pesa no "
          "custo, como pedem Ning *et al.* (2026)."),
]

# Tabela 1: layer1/data/report.md, first request, isolated environment.
TABLE_HEAD = ["Medida", "OpenCode 1.17.9", "Pi 0.80.10", "Razão"]
TABLE_ROWS = [
    ["Esquemas de ferramenta (quantidade)", "9", "4", "2,3"],
    ["Bytes dos esquemas de ferramenta", "20.007", "2.900", "6,9"],
    ["Bytes do *system prompt*", "9.738", "2.499", "3,9"],
    ["Bytes da conversa", "114", "135", "0,8"],
    ["Bytes do envelope da requisição", "138", "142", "1,0"],
    ["Total de bytes", "29.997", "5.676", "5,3"],
    ["Tokens (cl100k_base)", "6.659", "1.228", "5,4"],
]

REFERENCES = [
    "DEEPSEEK-AI. **DeepSeek-V4.1-Flash**: pushing the limits of KV cache compression. "
    "arXiv:2609.19969, 2026. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2609.19969. Acesso em: 22 out. 2026.",
    "EARENDIL. **Pi, minimal and performant**. 2026. Publicação de blogue institucional. "
    "Disponível em: https://earendil.com/posts/pi-autoresearch-and-databricks/. Acesso em: "
    "28 ago. 2026.",
    "FURGALE, Paul *et al.* **NVIDIA-labs OO Agents**: native Python object-oriented "
    "agents. arXiv:2607.20709, 2026. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2607.20709. Acesso em: 22 out. 2026.",
    "GRACE, Mikaela *et al.* **Demystifying evals for AI agents**. 2026. Publicação de "
    "blogue de engenharia (Anthropic), não revisada por pares. Disponível em: "
    "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents. Acesso em: "
    "22 out. 2026.",
    "JIN, Haibo *et al.* **Harness engineering for software engineering via modular "
    "executable dev-primitives**. arXiv:2610.07832, 2026. *Preprint*, não revisado por "
    "pares. Disponível em: https://arxiv.org/abs/2610.07832. Acesso em: 22 out. 2026.",
    "KARPATHY, Andrej. **LLM Wiki**: a pattern for building personal knowledge bases using "
    "LLMs. 2026. Gist (GitHub). Disponível em: "
    "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f. Acesso em: 14 set. "
    "2026.",
    "LIN, Jiahang *et al.* **Agentic harness engineering**: observability-driven automatic "
    "evolution of coding-agent harnesses. arXiv:2604.25850, 2026. *Preprint*, não revisado "
    "por pares. Disponível em: https://arxiv.org/abs/2604.25850. Acesso em: 28 ago. 2026.",
    "LINDENBAUER, Tobias *et al.* **The complexity trap**: simple observation masking is "
    "as efficient as LLM summarization for agent context management. arXiv:2508.21433, "
    "2025. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2508.21433. Acesso em: 22 out. 2026.",
    "LIU, Haozhe *et al.* **SoL-Pi**: recursively scaling auto-research loops for efficient "
    "agent harness. arXiv:2609.20519, 2026. *Preprint*, não revisado por pares. Disponível "
    "em: https://arxiv.org/abs/2609.20519. Acesso em: 23 set. 2026.",
    "MERRILL, Mike A. *et al.* Terminal-Bench: benchmarking agents on hard, realistic "
    "tasks in command line interfaces. In: INTERNATIONAL CONFERENCE ON LEARNING "
    "REPRESENTATIONS, 2026. **Proceedings** [...]. [*S. l.*: *s. n.*], 2026. Disponível em: "
    "https://proceedings.iclr.cc/paper_files/paper/2026/hash/444a3737adaee10d86ad2ef5f74468e6-"
    "Abstract-Conference.html. Acesso em: 22 out. 2026.",
    "MILLER, Evan. **Adding error bars to evals**: a statistical approach to language model "
    "evaluations. arXiv:2411.00640, 2024. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2411.00640. Acesso em: 28 ago. 2026.",
    "NING, Xuying *et al.* **Code as agent harness**. arXiv:2605.18747, 2026. *Preprint*, "
    "não revisado por pares. Disponível em: https://arxiv.org/abs/2605.18747. Acesso em: 28 "
    "ago. 2026.",
    "OPENCODE. **OpenCode**: the open source coding agent. 2026a. Repositório de código. "
    "Disponível em: https://github.com/anomalyco/opencode. Acesso em: 14 set. 2026.",
    "OPENCODE. **Zen**. 2026b. Documentação do produto. Disponível em: "
    "https://opencode.ai/docs/zen/. Acesso em: 28 ago. 2026.",
    "PAN, Melissa Z. *et al.* **HarnessTax**: how much does the harness matter for coding "
    "agents? 2026. Publicação de blogue de pesquisa, não revisada por pares. Disponível em: "
    "https://harnesstax.github.io/. Acesso em: 23 set. 2026.",
    "WONG, Sherman *et al.* **Confucius Code Agent**: scalable agent scaffolding for "
    "real-world codebases. arXiv:2512.10398, 2025. *Preprint*, não revisado por pares. "
    "Disponível em: https://arxiv.org/abs/2512.10398. Acesso em: 22 out. 2026.",
    "YOUNG, Justin. **Effective harnesses for long-running agents**. 2025. Publicação de "
    "blogue de engenharia (Anthropic), não revisada por pares. Disponível em: "
    "https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. "
    "Acesso em: 24 set. 2026.",
    "YUUKIFST. **agent-dotfiles**: skill Helmsman, mapa de decisões para agentes de "
    "codificação. 2026a. Repositório de código. Disponível em: "
    "https://github.com/YuukiFST/agent-dotfiles/tree/main/skills/helmsman. Acesso em: 15 "
    "set. 2026.",
    "YUUKIFST. **Finn**: SaaS universal de financeiro por voz. 2026b. Repositório de código. "
    "Disponível em: https://github.com/YuukiFST/Finn. Acesso em: 14 set. 2026.",
    "YUUKIFST. **harness-bench**: executor, prompts, testes de aceitação, dados brutos e "
    "scripts de análise deste projeto. 2026c. Repositório de código. Disponível em: "
    "https://github.com/YuukiFST/harness-bench. Acesso em: 28 ago. 2026.",
    "ZHANG, Yunbei *et al.* **Stop comparing LLM agents without disclosing the harness**. "
    "arXiv:2605.23950, 2026. *Preprint*, não revisado por pares. Disponível em: "
    "https://arxiv.org/abs/2605.23950. Acesso em: 28 ago. 2026.",
]

# --------------------------------------------------------------------------- XML

W_NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
MARKUP = re.compile(r"(\*\*.+?\*\*|\*.+?\*|\[\[FN\d+\]\])")


def runs(text: str, size: int = 24, bold: bool = False) -> str:
    """Markup text -> <w:r> elements at the given half-point size."""
    out = []
    for chunk in MARKUP.split(text):
        if not chunk:
            continue
        fn = re.fullmatch(r"\[\[FN(\d+)\]\]", chunk)
        if fn:
            out.append('<w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr>'
                       f'<w:footnoteReference w:id="{fn.group(1)}"/></w:r>')
            continue
        b, i = bold, False
        if chunk.startswith("**") and chunk.endswith("**"):
            chunk, b = chunk[2:-2], True
        elif chunk.startswith("*") and chunk.endswith("*"):
            chunk, i = chunk[1:-1], True
        props = ("<w:b/><w:bCs/>" if b else "") + ("<w:i/><w:iCs/>" if i else "")
        props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        out.append(f'<w:r><w:rPr>{props}</w:rPr>'
                   f'<w:t xml:space="preserve">{html.escape(chunk, quote=False)}</w:t></w:r>')
    return "".join(out)


def para(text: str, *, jc: str = "both", line: int = 360, before: int = 0, after: int = 0,
         first: int = 0, left: int = 0, size: int = 24, bold: bool = False,
         keep_next: bool = False) -> str:
    ppr = ("<w:keepNext/>" if keep_next else "")
    ppr += f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
    ppr += f'<w:ind w:left="{left}" w:firstLine="{first}"/><w:jc w:val="{jc}"/>'
    return f"<w:p><w:pPr>{ppr}</w:pPr>{runs(text, size, bold)}</w:p>"


def labelled(label: str, text: str) -> str:
    """Resumo / abstract / keyword lines: 10 pt, single spacing, justified."""
    return para(f"**{label}** {text}", line=240, after=120, size=20)


def cell(text: str, width: int, *, bold: bool = False, jc: str = "left",
         top: bool = False, bottom: bool = False, keep_next: bool = True) -> str:
    borders = ""
    if top or bottom:
        borders = "<w:tcBorders>"
        borders += '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>' if top else ""
        borders += ('<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
                    if bottom else "")
        borders += "</w:tcBorders>"
    return (f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{borders}</w:tcPr>'
            + para(text, jc=jc, line=240, size=20, bold=bold, keep_next=keep_next) + "</w:tc>")


def table() -> str:
    widths = [4271, 1800, 1800, 1200]
    rows = []
    head = "".join(cell(t, w, bold=True, jc="left" if k == 0 else "center", top=True, bottom=True)
                   for k, (t, w) in enumerate(zip(TABLE_HEAD, widths)))
    rows.append(f"<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>{head}</w:tr>")
    for n, row in enumerate(TABLE_ROWS):
        last = n == len(TABLE_ROWS) - 1
        cells = "".join(cell(t, w, jc="left" if k == 0 else "center", bottom=last,
                             keep_next=not last)
                        for k, (t, w) in enumerate(zip(row, widths)))
        rows.append(f"<w:tr><w:trPr><w:cantSplit/></w:trPr>{cells}</w:tr>")
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    return ('<w:tbl><w:tblPr><w:tblW w:w="9071" w:type="dxa"/><w:jc w:val="center"/>'
            '<w:tblLayout w:type="fixed"/>'
            '<w:tblCellMar><w:left w:w="57" w:type="dxa"/><w:right w:w="57" w:type="dxa"/>'
            '</w:tblCellMar></w:tblPr>'
            f"<w:tblGrid>{grid}</w:tblGrid>{''.join(rows)}</w:tbl>")


def document() -> str:
    body = [para(TITLE, jc="center", size=28, bold=True, after=360)]
    body += [para(a, jc="center") for a in AUTHORS]
    body.append(para("", line=360))
    body.append(labelled("Resumo:", RESUMO))
    body.append(labelled("Palavras-chave:", PALAVRAS_CHAVE))
    body.append(para("", line=240, size=20))
    body.append(labelled("Abstract:", ABSTRACT))
    body.append(labelled("Keywords:", KEYWORDS))
    for kind, text in BODY:
        if kind == "h":
            body.append(para(text, jc="left", bold=True, before=240, after=120, keep_next=True))
        elif kind == "p":
            body.append(para(text, first=INDENT))
        elif kind == "q":
            body.append(para(text, line=240, before=240, after=240, left=QUOTE_INDENT,
                             size=20))
        elif kind == "table":
            body.append(para(text, jc="center", line=240, before=120, after=60, size=20,
                             keep_next=True))
            body.append(table())
        elif kind == "src":
            body.append(para(text, jc="left", line=240, before=60, after=120, size=20))
    body.append(para("REFERÊNCIAS", jc="center", bold=True, before=240, after=120,
                     keep_next=True))
    body += [para(r, jc="left", line=240, before=120, after=120) for r in REFERENCES]
    sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter1"/>'
            '<w:footnotePr><w:numFmt w:val="decimal"/></w:footnotePr>'
            '<w:pgSz w:w="11906" w:h="16838" w:orient="portrait"/>'
            '<w:pgMar w:top="1701" w:right="1134" w:bottom="1134" w:left="1701" '
            'w:header="709" w:footer="709" w:gutter="0"/>'
            '<w:pgNumType w:start="1"/></w:sectPr>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document {W_NS}><w:body>{"".join(body)}{sect}</w:body></w:document>')


def footnotes() -> str:
    sep = ('<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" '
           'w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>'
           '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing '
           'w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/>'
           '</w:r></w:p></w:footnote>')
    notes = []
    for n, text in FOOTNOTES.items():
        notes.append(
            f'<w:footnote w:id="{n}"><w:p><w:pPr><w:spacing w:after="0" w:line="240" '
            'w:lineRule="auto"/><w:jc w:val="both"/></w:pPr>'
            '<w:r><w:rPr><w:vertAlign w:val="superscript"/><w:sz w:val="20"/></w:rPr>'
            '<w:footnoteRef/></w:r>' + runs(" " + text, size=20) + "</w:p></w:footnote>")
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:footnotes {W_NS}>{sep}{"".join(notes)}</w:footnotes>')


FOOTER = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {W_NS}>'
          '<w:p><w:pPr><w:jc w:val="right"/></w:pPr>'
          '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
          '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r>'
          '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')

STYLES = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles {W_NS}>'
          '<w:docDefaults><w:rPrDefault><w:rPr>'
          '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
          'w:eastAsia="Times New Roman" w:cs="Times New Roman"/>'
          '<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="pt-BR"/>'
          '</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>'
          '<w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
          '</w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
          '<w:qFormat/></w:style>'
          '<w:style w:type="table" w:default="1" w:styleId="TableNormal">'
          '<w:name w:val="Normal Table"/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
          '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
          '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar>'
          '</w:tblPr></w:style></w:styles>')

SETTINGS = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings {W_NS}>'
            '<w:defaultTabStop w:val="709"/>'
            '<w:footnotePr><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr>'
            '<w:compat><w:compatSetting w:name="compatibilityMode" '
            'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat>'
            '</w:settings>')

CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
    '<Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>'
    '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
    '</Types>')

ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>')

DOC_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
    '<Relationship Id="rIdFootnotes" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/>'
    '<Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
    '</Relationships>')


def main() -> None:
    words = len(re.sub(r"\*", "", RESUMO).split())
    assert words <= 250, f"resumo has {words} words, the handout allows 250"
    title_chars = len(re.sub(r"\*", "", TITLE))
    assert title_chars <= 135, f"title has {title_chars} characters, the handout allows 135"
    DST.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", document())
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/settings.xml", SETTINGS)
        z.writestr("word/footnotes.xml", footnotes())
        z.writestr("word/footer1.xml", FOOTER)
    print(f"{DST.relative_to(ROOT)}: resumo {words} words, title {title_chars} characters")


if __name__ == "__main__":
    main()
