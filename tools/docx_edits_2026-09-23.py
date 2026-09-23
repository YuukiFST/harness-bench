"""Rewrite of dist/projeto-de-pesquisa.docx, 2026-09-23.

Adds HarnessTax (Pan et al., 2026; wiki/sources/harnesstax-pan-2026.md) and
SoL-Pi (Liu et al., 2026; wiki/sources/sol-pi-liu-2026.md), drops the
references they make redundant (Alier Forment, HarnessRank, Kapoor 2024/2025,
Lee, Runta, Wang, Yao, Yang), rewrites H1 so it covers success rate and can be
refuted, adds the two missing threats (unit dependence under Wilcoxon, free
tier swapping the model), italicises every in-text et al., bolds every
reference title, and cuts the document from 12 to 9 pages (Word count).
The humanizer skill ran on the prose before each pass was applied.
The Cuiabá line stays city-only: NBR 14724 asks for the city alone on the
folha de rosto, and AGENTS.md makes the NBR win over the course handout.

Passes run in order; indices of each pass come from `docx_prose.py dump`
after the previous one. The sumário numbers are set after the last pass.

Run once on the 89fccf9 docx: python tools/docx_edits_2026-09-23.py
"""
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from docx_prose import _rewrite_zip, apply  # noqa: E402

DOCX = Path("dist/projeto-de-pesquisa.docx")
SUMARIO = {"1 INTRODUÇÃO": "1", "2 REFERENCIAL TEÓRICO": "2", "3 MATERIAL E MÉTODO": "3",
           "4 ORÇAMENTO": "5", "5 CRONOGRAMA": "5", "6 REFERÊNCIAS": "5"}
PASSES = json.loads(r"""
[
 {
  "paragraphs": {
   "9": "O HARNESS NO CUSTO E NO DESEMPENHO DE AGENTES DE CODIFICAÇÃO: TOKENS E TAXA DE SUCESSO COM O MODELO FIXO",
   "22": "O HARNESS NO CUSTO E NO DESEMPENHO DE AGENTES DE CODIFICAÇÃO: TOKENS E TAXA DE SUCESSO COM O MODELO FIXO",
   "43": "Um agente de codificação tem duas partes: o modelo de linguagem e o *harness*, o software ao redor dele que monta o contexto, expõe as ferramentas e conduz a execução (Claude Code, Codex, OpenCode, pi). Pan *et al.* (2026), da Universidade da Califórnia em Berkeley, avaliaram sete modelos em três *harnesses* e concluíram que a escolha do *harness* quase não muda a taxa de sucesso, mas muda o custo. No SWE-bench Lite, o Claude Fable 5 resolve 97,8% das tentativas no Claude Code e 96,7% no pi, e o Claude Code custa cerca do dobro por tentativa (US$ 1,33 contra US$ 0,67).",
   "44": "Quem paga por tokens, o desenvolvedor na assinatura ou a empresa em escala, paga também essa diferença, que os autores chamam de imposto do *harness*. As medições publicadas usam tarefas isoladas de *benchmarks* que os modelos podem ter visto no treino. Os próprios autores apontam como próximo passo medir o *harness* em fluxos reais de desenvolvimento, com tarefas que se estendem por várias sessões. Este projeto constrói o mesmo produto, o Finn, duas vezes, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, e conta os tokens fora do *harness*.",
   "46": "O efeito do *harness* sobre o custo e o desempenho de um modelo de linguagem fixo na construção de um produto de software completo.",
   "48": "Com o modelo fixo, quanto mudam o custo em tokens e a taxa de sucesso ao construir o mesmo software com um *harness* em vez de outro, e quanto da diferença de custo vem da carga fixa que cada *harness* envia em toda requisição?",
   "50": "Medir, com o modelo fixo, a diferença de tokens e de taxa de sucesso atribuível ao *harness* na construção do mesmo produto a partir da mesma especificação, com o OpenCode e o pi como braços, e separar a parcela que vem da carga fixa por requisição.",
   "52": "1) construir o *proxy* que conta requisições, tokens e latência por braço;",
   "53": "2) escrever a especificação do Finn em nove unidades, com testes de aceitação;",
   "54": "3) construir o Finn nos dois *harnesses*, com o mesmo modelo, *prompt* e espaço inicial;",
   "55": "4) repetir em um segundo modelo e verificar se a ordenação dos braços se mantém;",
   "56": "5) comparar os tokens relatados por cada *harness* com os medidos no *proxy*;",
   "57": "6) publicar executor, *prompts*, testes, dados e scripts de análise.",
   "58": null,
   "60": "Pesquisa aplicada, quali-quantitativa, exploratória e experimental, de método dedutivo. Um *proxy* reverso entre cada *harness* e o modelo contará requisições, tokens e latência da mesma forma para os dois braços. Cada braço construirá o Finn do zero, em nove unidades, ao menos três vezes, e a diferença entre os braços será comparada unidade a unidade. A seção 3 detalha o método.",
   "62": "H1: com o modelo fixo, o *harness* muda mais o custo do que o sucesso. Os tokens por unidade diferem entre o OpenCode e o pi, e a fração de testes aprovados fica igual. H1 será refutada se o teste pareado não apontar diferença de tokens ou se apontar diferença de sucesso.",
   "63": "H2: a carga fixa por requisição (*prompt* de sistema e esquemas de ferramenta) explica a maior parte da diferença de tokens, e o número de passos explica a menor. H2 será refutada se os passos ou o conteúdo da conversa explicarem a maior parte.",
   "64": "Após esta introdução, a seção 2 apresenta o referencial teórico e a seção 3, o material e método. As seções 4, 5 e 6 trazem o orçamento, o cronograma e as referências.",
   "66": "Segundo Ning *et al.* (2026, §2, tradução nossa), um *harness* “converte um modelo de linguagem sem estado em um agente funcional ao ancorar suas saídas em execução externa, estado persistente e realimentação verificável”. Lin *et al.* (2026) delimitam o que essa camada contém:",
   "68": "Só esse conjunto varia entre os braços deste experimento. O pi envia quatro ferramentas (ler, escrever, editar e executar comandos) e um *prompt* de sistema curto. O OpenCode envia mais ferramentas e um *prompt* maior, com planejamento, compactação de contexto, subagentes e permissões.",
   "69": "A interface entre modelo e ambiente é objeto de projeto desde Yang *et al.* (2024). Na Tabela 1 de Lin *et al.* (2026), *harnesses* escritos por humanos sobre o GPT-5.4 vão de 47,2% de aprovação no OpenCode a 71,9% no Codex, no Terminal-Bench 2. Zhang *et al.* (2026) sustentam que, entre modelos de fronteira comparáveis, a parcela do desempenho que vem do *harness* é comparável ou maior que a do modelo. Pan *et al.* (2026) mediram outra coisa no SWE-bench Lite: o efeito médio do *harness* sobre a taxa de sucesso ficou dentro de ±2%, enquanto o Claude Code custou cerca de 2,0 vezes o pi. Como as fontes divergem sobre o sucesso, este projeto mede sucesso e custo juntos.",
   "70": "A primeira pendência é saber de onde vem a diferença de custo. Pan *et al.* (2026) apontam a primeira requisição. O contexto inicial do Claude Code passa de dez vezes o do pi, com número de turnos parecido (15,3 contra 15,4 no Claude Fable 5). Liu *et al.* (2026) apontam o resto da conversa. Com os mesmos modelos, mudar a execução das ações, a compactação de contexto e o tratamento das observações cortou de 44,7% a 49,0% dos tokens em relação ao pi, com desempenho comparável. Ning *et al.* (2026, §5.2.7, tradução nossa) pedem “métricas que isolem componentes do *harness*”. Este projeto separa, em cada requisição, a carga fixa do conteúdo da conversa, e H2 testa qual das duas pesa mais.",
   "71": "A segunda pendência é a instrumentação. Cada *harness* conta turnos e tokens do seu jeito, e Pan *et al.* (2026) registram que a definição de turno varia entre eles. Aqui a medição ocorre em um *proxy* externo, igual para os dois braços, e o objetivo (5) compara essa medida com o relato de cada *harness*.",
   "72": "As métricas serão tokens por construção, sempre ao lado da fração de testes aprovados, e o Succ/Mtok (sucessos por milhão de tokens) de Lin *et al.* (2026). O efeito também depende do modelo. Em nove de doze comparações de Pan *et al.* (2026), o maior sucesso de um modelo veio de um *harness* de outro fornecedor. Por isso o desenho terá dois níveis de modelo, com conclusões por nível.",
   "74": "Quanto à finalidade, a pesquisa é aplicada, pois entrega um critério de escolha de *harness*. Quanto à abordagem, é quali-quantitativa. Tokens e sucesso são medidas quantitativas, e a atribuição da diferença à carga fixa ou aos passos é qualitativa. Quanto aos objetivos, é exploratória, já que não há comparação publicada de *harnesses* construindo o mesmo produto completo. Quanto aos procedimentos, é experimental. O *harness* é a variável manipulada, e modelo, especificação, espaço de trabalho inicial e limites ficam controlados. Quanto ao método, é dedutiva, com hipóteses declaradas antes da coleta.",
   "75": "Conforme a Portaria CNPq nº 2.664/2026 (Brasil, 2026), declara-se o uso do Claude Code em duas partes deste projeto. A primeira foi o levantamento das fontes, organizado pelo método *LLM Wiki* de Karpathy (2026) e mantido no repositório do projeto (YuukiFST, 2026c). O autor curou as fontes e conferiu cada afirmação citada na obra original. A segunda foi a especificação do Finn, feita com o Helmsman (YuukiFST, 2026a), rotina do autor em que ele decide o que o sistema faz e o agente registra como construir. O autor responde pelo texto final e por cada decisão de produto.",
   "76": "A medição terá duas camadas. A Camada 1 mede, contra um *endpoint* simulado, a forma de cada requisição: esquemas de ferramenta, *prompt* de sistema e tokens. Ela é determinística, não gasta cota e fornece a carga fixa que H2 usa. A Camada 2 mede a construção do produto contra o modelo real, gasta cota e varia de uma execução para outra.",
   "77": "Os braços serão o OpenCode (Opencode, 2026a) e o pi (Earendil, 2026). Os dois são de código aberto, rodam sem interface e aceitam URL base compatível com a API da OpenAI, o que permite passá-los pelo *proxy*. As versões serão fixadas e registradas no repositório (YuukiFST, 2026c).",
   "78": "O produto será o Finn, SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e recebe lançamento, relatório e aviso no celular (YuukiFST, 2026b). Produto e pilha foram decididos antes do experimento, em 21 *tickets*. O autor escreverá uma especificação única, congelada por SHA-256, com a pilha (TypeScript, TanStack Start, tRPC, Drizzle ORM, PostgreSQL, Vitest) e nove unidades em ordem de dependência. O executor chama o *harness* uma vez por unidade, com o mesmo *prompt* nos dois braços, e cada unidade parte do que o agente construiu na anterior. O autor não escreve código no espaço de trabalho.",
   "79": "Serão dois níveis de modelo, primário e de robustez, ambos gratuitos no mesmo *gateway* (Opencode, 2026b), com resultados relatados por nível. Se a ordenação dos braços inverter de um nível para o outro, a inversão será reportada como resultado.",
   "80": "O *proxy* ficará entre cada braço e o *gateway* e contará os tokens sobre os bytes transmitidos, com o mesmo tokenizador para os dois braços. As contagens do *harness* e do *gateway* incluem conteúdo que nenhum braço enviou, então servem só para verificação cruzada e cálculo de custo.",
   "81": "Haverá um único limite, igual para os dois braços: tempo de relógio por unidade, de três vezes a maior mediana dos braços nas unidades-piloto. Pan *et al.* (2026) limitaram cada tentativa a 100 turnos. Aqui o número de passos fica livre, porque um teto de passos é decisão de projeto de *harness* e apagaria a diferença sob teste. O comprimento máximo de saída será igualado pelo *proxy*, e os parâmetros de amostragem serão registrados sem ajuste, como recomenda Miller (2024).",
   "82": "Cada combinação de braço e nível terá ao menos três construções completas válidas, com resultados em mediana e dispersão. Se a cota não comportar a matriz, reduz-se primeiro a cobertura da matriz, mantendo as três repetições.",
   "83": "A comparação usará o teste de Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por unidade, sobre tokens, fração de testes aprovados e Succ/Mtok por unidade. O teste é não paramétrico porque nove pares não sustentam suposição de distribuição, e pareado porque a dificuldade da unidade é a maior fonte de variação (Miller, 2024). Para H2, os tokens de cada unidade serão divididos em carga fixa (Camada 1 vezes o número de passos) e conversa. As predições serão registradas antes da coleta, e um resultado nulo será reportado.",
   "84": "Unidade não concluída conta como resultado, com a fração de testes aprovada, e a construção segue. Medição não confiável, como a troca do modelo servido no meio da construção, descarta a construção inteira, sem reparo nem repetição. A classe de cada unidade vem do registro do *proxy*.",
   "86": "O projeto tem cinco limitações. O efeito do *harness* depende do modelo, então as conclusões valem por nível, e o objetivo (4) testa isso. O produto é um único SaaS em uma única pilha. A especificação é do autor, e cada braço carrega os próprios erros de uma unidade à seguinte. Por isso as unidades não são independentes, como o teste de Wilcoxon supõe, e o valor-p será lido como indicativo, ao lado da diferença e da dispersão. O nível gratuito do *gateway* pode trocar o modelo ou cortar a cota durante a coleta, e o *proxy* registra o modelo declarado em cada resposta. Por fim, os valores absolutos não são comparáveis a placares públicos, e o custo em dinheiro entra só como estimativa sobre tarifas pagas publicadas.",
   "91": "Inferência dos modelos (dois níveis, nível gratuito do *gateway*)",
   "100": "O total é zero. O limite real é a cota gratuita do *gateway*, a ser medida nas unidades-piloto, e cada construção rodará em lotes ao longo de dias, retomada entre unidades.",
   "102": "O projeto foi escrito entre agosto e setembro de 2026, e os experimentos começam em outubro. Como a cota gratuita é o limite, a matriz roda em um lote por dia.",
   "183": null,
   "186": null,
   "187": null,
   "188": null,
   "189": "KARPATHY, Andrej. **LLM Wiki**: a pattern for building personal knowledge bases using LLMs. 2026. Gist (GitHub). Disponível em: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f. Acesso em: 14 set. 2026.",
   "190": null,
   "194": "OPENCODE. **OpenCode**: the open source coding agent. 2026a. Repositório de código. Disponível em: https://github.com/anomalyco/opencode. Acesso em: 14 set. 2026.",
   "195": "OPENCODE. **Zen**. 2026b. Documentação do produto. Disponível em: https://opencode.ai/docs/zen/. Acesso em: 28 ago. 2026.",
   "196": null,
   "197": null,
   "199": null,
   "200": "YUUKIFST. **agent-dotfiles**: skill Helmsman, mapa de decisões para agentes de codificação. 2026a. Repositório de código. Disponível em: https://github.com/YuukiFST/agent-dotfiles/tree/main/skills/helmsman. Acesso em: 15 set. 2026.",
   "201": "YUUKIFST. **Finn**: SaaS universal de financeiro por voz. 2026b. Repositório de código. Disponível em: https://github.com/YuukiFST/Finn. Acesso em: 14 set. 2026.",
   "202": "YUUKIFST. **harness-bench**: executor, prompts, testes de aceitação, dados brutos e scripts de análise deste projeto. 2026c. Repositório de código. Disponível em: https://github.com/YuukiFST/harness-bench. Acesso em: 28 ago. 2026."
  },
  "insert_after": {
   "78": "A pontuação será a fração dos testes de aceitação aprovados. O autor escreverá os testes antes da execução, os manterá fora do espaço de trabalho e os rodará sobre uma cópia dele ao fim de cada unidade. Os testes escritos pelo agente não contam, e uma unidade conta como concluída quando todos os seus testes passam.",
   "191": "LIU, Haozhe *et al.* **SoL-Pi**: recursively scaling auto-research loops for efficient agent harness. arXiv:2609.20519, 2026. *Preprint*, não revisado por pares. Disponível em: https://arxiv.org/abs/2609.20519. Acesso em: 23 set. 2026.",
   "195": "PAN, Melissa Z.; YANG, Shuo; ARABZADEH, Negar; CHIANG, Wei-Lin; STOICA, Ion; ZAHARIA, Matei. **HarnessTax**: how much does the harness matter for coding agents? 2026. Publicação de blogue de pesquisa, não revisada por pares. Disponível em: https://harnesstax.github.io/. Acesso em: 23 set. 2026."
  }
 },
 {
  "paragraphs": {
   "59": "Pesquisa aplicada, quali-quantitativa, exploratória e experimental, de método dedutivo. Um *proxy* reverso entre cada *harness* e o modelo contará requisições, tokens e latência da mesma forma para os dois braços. Cada braço construirá o Finn do zero, em nove unidades, ao menos três vezes, e a diferença entre os braços será comparada unidade a unidade.",
   "73": "A pesquisa é aplicada quanto à finalidade, quali-quantitativa quanto à abordagem, exploratória quanto aos objetivos, experimental quanto aos procedimentos e dedutiva quanto ao método. É exploratória porque não há comparação publicada de *harnesses* construindo o mesmo produto completo. O *harness* é a variável manipulada, e modelo, especificação, espaço de trabalho inicial e limites ficam controlados.",
   "74": "Conforme a Portaria CNPq nº 2.664/2026 (Brasil, 2026), declara-se o uso do Claude Code no levantamento das fontes, organizado pelo método *LLM Wiki* de Karpathy (2026) no repositório do projeto (YuukiFST, 2026c), e na especificação do Finn, feita com o Helmsman (YuukiFST, 2026a). O autor conferiu cada afirmação citada na obra original e responde pelo texto e pelas decisões de produto.",
   "75": "A medição terá duas camadas. A Camada 1 mede, contra um *endpoint* simulado, os esquemas de ferramenta, o *prompt* de sistema e os tokens de cada requisição. Ela é determinística, não gasta cota e fornece a carga fixa que H2 usa. A Camada 2 mede a construção do produto contra o modelo real e varia de uma execução para outra.",
   "82": "Cada combinação de braço e nível terá ao menos três construções completas válidas, relatadas em mediana e dispersão.",
   "100": "O limite real é a cota gratuita do *gateway*, a ser medida nas unidades-piloto.",
   "102": "Os experimentos começam em outubro de 2026 e rodam em um lote por dia, dentro da cota gratuita."
  }
 },
 {
  "paragraphs": {
   "44": "Quem paga por tokens, o desenvolvedor na assinatura ou a empresa em escala, paga também essa diferença, que os autores chamam de imposto do *harness*. Essas medições usam tarefas isoladas de *benchmarks* que os modelos podem ter visto no treino, e os próprios autores apontam como próximo passo medir o *harness* em fluxos reais de desenvolvimento, com tarefas de várias sessões. Este projeto constrói o mesmo produto, o Finn, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, e conta os tokens fora do *harness*.",
   "68": "Na Tabela 1 de Lin *et al.* (2026), *harnesses* escritos por humanos sobre o GPT-5.4 vão de 47,2% de aprovação no OpenCode a 71,9% no Codex, no Terminal-Bench 2. Zhang *et al.* (2026) sustentam que, entre modelos de fronteira comparáveis, a parcela do desempenho que vem do *harness* é comparável ou maior que a do modelo. Pan *et al.* (2026) mediram outra coisa no SWE-bench Lite: o efeito médio do *harness* sobre a taxa de sucesso ficou dentro de ±2%, enquanto o Claude Code custou cerca de 2,0 vezes o pi. Como as fontes divergem sobre o sucesso, este projeto mede sucesso e custo juntos.",
   "69": "A primeira pendência é saber de onde vem a diferença de custo. Pan *et al.* (2026) apontam a primeira requisição. O contexto inicial do Claude Code passa de dez vezes o do pi, com número de turnos parecido (15,3 contra 15,4 no Claude Fable 5). Liu *et al.* (2026) apontam o resto da conversa. Mudando só a execução das ações, a compactação de contexto e o tratamento das observações, cortaram de 44,7% a 49,0% dos tokens em relação ao pi e mantiveram de 93,7% a 94,3% da pontuação dele. Ning *et al.* (2026, §5.2.7, tradução nossa) pedem “métricas que isolem componentes do *harness*”, e H2 testa se pesa mais a carga fixa ou a conversa.",
   "80": "O *proxy* contará os tokens sobre os bytes transmitidos, com o mesmo tokenizador para os dois braços. As contagens do *harness* e do *gateway* incluem conteúdo que nenhum braço enviou e servem só para verificação cruzada.",
   "81": "Haverá um único limite, igual para os dois braços: tempo de relógio por unidade, de três vezes a maior mediana dos braços nas unidades-piloto. Pan *et al.* (2026) limitaram cada tentativa a 100 turnos. Aqui o número de passos fica livre, porque um teto de passos é decisão de projeto de *harness* e apagaria a diferença sob teste.",
   "83": "A comparação usará o teste de Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por unidade, sobre tokens, fração de testes aprovados e Succ/Mtok. O teste é não paramétrico porque nove pares não sustentam suposição de distribuição, e pareado porque a dificuldade da unidade é a maior fonte de variação (Miller, 2024). Para H2, os tokens de cada unidade serão divididos em carga fixa (Camada 1 vezes o número de passos) e conversa. As predições serão registradas antes da coleta.",
   "84": "Unidade não concluída conta como resultado, com a fração de testes aprovada, e a construção segue. Medição não confiável, como a troca do modelo servido no meio da coleta, descarta a construção inteira.",
   "86": "O projeto tem quatro limitações. O efeito do *harness* depende do modelo, então as conclusões valem por nível. O produto é um único SaaS em uma única pilha. Cada braço carrega os próprios erros de uma unidade à seguinte, então as unidades não são independentes, como o teste de Wilcoxon supõe, e o valor-p será lido como indicativo, ao lado da diferença e da dispersão. Por fim, o nível gratuito do *gateway* pode trocar o modelo ou cortar a cota durante a coleta.",
   "186": "LIN, Jiahang *et al.* **Agentic harness engineering**: observability-driven automatic evolution of coding-agent harnesses. arXiv:2604.25850, 2026. *Preprint*, não revisado por pares. Disponível em: https://arxiv.org/abs/2604.25850. Acesso em: 28 ago. 2026.",
   "192": "PAN, Melissa Z. *et al.* **HarnessTax**: how much does the harness matter for coding agents? 2026. Publicação de blogue de pesquisa, não revisada por pares. Disponível em: https://harnesstax.github.io/. Acesso em: 23 set. 2026.",
   "193": null,
   "197": "ZHANG, Yunbei *et al.* **Stop comparing LLM agents without disclosing the harness**. arXiv:2605.23950, 2026. *Preprint*, não revisado por pares. Disponível em: https://arxiv.org/abs/2605.23950. Acesso em: 28 ago. 2026."
  }
 },
 {
  "paragraphs": {
   "75": "A medição terá duas camadas. A Camada 1 mede, contra um *endpoint* simulado, os esquemas de ferramenta, o *prompt* de sistema e os tokens de cada requisição, e fornece a carga fixa que H2 usa. A Camada 2 mede a construção do produto contra o modelo real.",
   "80": "O *proxy* contará os tokens sobre os bytes transmitidos, com o mesmo tokenizador para os dois braços. As contagens do *harness* e do *gateway* servem só para verificação cruzada.",
   "81": "Haverá um único limite, igual para os dois braços: tempo de relógio por unidade, de três vezes a maior mediana dos braços nas unidades-piloto. O número de passos fica livre, porque um teto de passos é decisão de projeto de *harness* e apagaria a diferença sob teste.",
   "100": null,
   "102": "Os experimentos começam em outubro de 2026, dentro da cota gratuita do *gateway*."
  }
 },
 {
  "paragraphs": {
   "93": "*Harnesses* e ferramentas de código aberto",
   "101": null,
   "117": "DEFINIÇÃO DO TEMA E DAS HIPÓTESES",
   "124": "CONSTRUÇÃO DO PROXY E DOS TESTES",
   "173": "REVISÃO FINAL E APRESENTAÇÃO"
  }
 },
 {
  "paragraphs": {
   "44": "Quem paga por tokens paga também essa diferença, que os autores chamam de imposto do *harness*. Essas medições usam tarefas isoladas de *benchmarks* que os modelos podem ter visto no treino, e os próprios autores apontam como próximo passo medir o *harness* em fluxos reais de desenvolvimento, com tarefas de várias sessões. Este projeto constrói o mesmo produto, o Finn, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, e conta os tokens fora do *harness*.",
   "67": "Só esse conjunto varia entre os braços deste experimento. O pi envia quatro ferramentas e um *prompt* de sistema curto, e o OpenCode envia mais ferramentas, um *prompt* maior, subagentes e permissões."
  }
 },
 {
  "paragraphs": {
   "71": "As métricas serão tokens por construção, ao lado da fração de testes aprovados, e o Succ/Mtok (sucessos por milhão de tokens) de Lin *et al.* (2026). O efeito também depende do modelo, pois em nove de doze comparações de Pan *et al.* (2026) o maior sucesso veio de um *harness* de outro fornecedor. Por isso o desenho terá dois níveis de modelo.",
   "83": "A comparação usará o teste de Wilcoxon dos postos sinalizados, bilateral, α = 0,05, sobre tokens, fração de testes aprovados e Succ/Mtok, pareado por unidade porque a dificuldade da unidade é a maior fonte de variação (Miller, 2024). Para H2, os tokens de cada unidade serão divididos em carga fixa (Camada 1 vezes o número de passos) e conversa. As predições serão registradas antes da coleta."
  }
 },
 {
  "paragraphs": {
   "86": "O projeto tem quatro limitações. O efeito do *harness* depende do modelo, então as conclusões valem por nível. O produto é um único SaaS em uma única pilha. Cada braço carrega os próprios erros de uma unidade à seguinte, então as unidades não são independentes, embora o teste de Wilcoxon suponha que sejam; o valor-p será lido como indicativo, ao lado da diferença e da dispersão. Por fim, o nível gratuito do *gateway* pode trocar o modelo ou cortar a cota durante a coleta."
  }
 }
]
""")


def set_sumario() -> None:
    # The sumário is static text with a tab stop, which docx_prose cannot render.
    xml = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf-8")
    for heading, page in SUMARIO.items():
        pattern = re.compile(r'(<w:t xml:space="preserve">' + re.escape(heading)
                             + r'</w:t><w:tab/><w:t xml:space="preserve">)\d+(</w:t>)')
        xml, hits = pattern.subn(r"\g<1>" + page + r"\g<2>", xml)
        if hits != 1:
            raise SystemExit(f"sumário line {heading!r} matched {hits} times")
    _rewrite_zip(DOCX, {"word/document.xml": xml.encode("utf-8")})


def main() -> None:
    for edits in PASSES:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(edits, f, ensure_ascii=False)
        apply(DOCX, Path(f.name))
        Path(f.name).unlink()
    # Page numbers are only final once every pass has run.
    set_sumario()


if __name__ == "__main__":
    main()
