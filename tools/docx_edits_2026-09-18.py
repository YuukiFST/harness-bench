"""Rewrite dist/projeto-de-pesquisa.docx to the course template: shorter blocks,
new title and theme (the harness as the lever on a fixed model's cost and
performance), one-line specific objectives, section 2 reduced to the two open
questions. Indices are from `docx_prose.py dump` on 2026-09-18.

Run once: python tools/docx_edits_2026-09-18.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

DOCX = Path("dist/projeto-de-pesquisa.docx")
TITLE = ("COMO O HARNESS ALTERA O CUSTO E O DESEMPENHO DE UM MODELO DE LINGUAGEM: "
         "TOKENS E TAXA DE SUCESSO DE AGENTES DE CODIFICAÇÃO COM O MODELO FIXO")

P = {
 "9": TITLE,
 "22": TITLE,
 "43": ("Os agentes de codificação avançam em duas frentes. Os modelos de linguagem melhoram a cada versão, "
        "e a camada de software ao redor deles, o *harness* (Claude Code, Codex, Cursor, OpenCode, pi), muda o que o "
        "mesmo modelo custa e entrega. No FrontierHarness (Runta, 2026), doze configurações de nove *harnesses* sobre "
        "o mesmo modelo ficam entre 50,0% e 66,7% de aprovação, e o custo por tarefa concluída vai de US$ 1,05 a "
        "US$ 18,34. Dois deles são de código aberto e rodam sem interface: o pi conclui 60,0% das tarefas a US$ 2,43 "
        "e o OpenCode 50,0% a US$ 3,24."),
 "44": ("As ferramentas de desenvolvimento seguem o mesmo movimento: Next.js, TanStack e Effect passaram a se adaptar "
        "ao trabalho de agentes. Escolher o modelo deixou de bastar; o desenvolvedor, na assinatura, e a empresa, em "
        "escala, precisam conhecer o que avança junto, e o *harness* é a parte dessa escolha que ninguém mediu na "
        "construção de um produto inteiro. As comparações publicadas usam tarefas isoladas. Este projeto mede esse "
        "custo construindo o mesmo produto duas vezes, do zero, com o OpenCode e com o pi, sobre o mesmo modelo e a "
        "mesma especificação, contando os tokens fora do *harness*."),
 "46": ("O efeito do *harness* sobre o custo e o desempenho de um modelo de linguagem fixo: quantos tokens e que taxa "
        "de sucesso o mesmo modelo entrega ao construir o mesmo produto sob dois *harnesses* diferentes."),
 "48": ("Com o modelo já escolhido, quanto mudam o custo em tokens e a taxa de sucesso ao construir o mesmo software "
        "com um *harness* em vez de outro, e quanto dessa diferença vem da carga fixa que cada *harness* envia em toda "
        "requisição?"),
 "50": ("Medir, com o modelo fixo, a diferença de tokens e de taxa de sucesso atribuível ao *harness* na construção do "
        "mesmo produto a partir da mesma especificação, com o OpenCode e o pi como braços, separando a parcela que vem "
        "da carga fixa por requisição, e entregar o resultado como critério de escolha reproduzível."),
 "52": "1) construir um instrumento externo que conte requisições, tokens e latência igual para os dois braços;",
 "53": "2) escrever a especificação do Finn em nove unidades, com testes de aceitação do autor;",
 "54": "3) preparar um espaço de trabalho inicial idêntico, só especificação e pilha, congelado por hash;",
 "55": "4) construir o Finn completo nos dois *harnesses*, mesmo modelo e *prompts*, com repetição e dispersão;",
 "56": "5) repetir em um segundo modelo e verificar se a ordenação entre os braços se mantém;",
 "57": "6) quantificar a divergência entre os tokens relatados pelo *harness* e os medidos no instrumento;",
 "58": "7) publicar executor, *prompts*, testes, dados e scripts, reexecutáveis a custo zero.",
 "60": ("Pesquisa aplicada, quali-quantitativa, exploratória e experimental, de método dedutivo. Os dados virão de um "
        "*proxy* reverso entre cada *harness* e o modelo, que contará requisições, tokens e latência igual para os dois "
        "braços. Cada braço construirá o Finn do zero, em nove unidades, ao menos três vezes. Espera-se obter a "
        "diferença de tokens e de taxa de sucesso atribuível ao *harness*, comparada por teste pareado por unidade. "
        "A seção 3 detalha material, método e estatística."),
 "62": ("H1: entre o OpenCode e o pi sobre o mesmo modelo, a diferença de tokens para construir o Finn a partir da mesma "
        "especificação é relevante para quem paga, comparável à de trocar de modelo sob um *harness* fixo. H1 será "
        "refutada se os intervalos de tokens por construção se sobrepuserem e o teste pareado por unidade não apontar "
        "diferença."),
 "63": ("H2: a carga fixa por requisição (*prompt* de sistema e esquemas de ferramenta, medidos na Camada 1) explica a "
        "maior parte dessa diferença; o número de passos por unidade, a menor. H2 será refutada se os passos explicarem "
        "a maior parte, desfecho possível se o *harness* com mais ferramentas concluir a unidade em menos passos."),
 "64": ("Este trabalho tem seis seções. A seção 1 traz justificativa, tema, problema, objetivos, metodologia e "
        "hipóteses. A seção 2 posiciona o trabalho na literatura e delimita as pendências que ele responde. A seção 3 "
        "descreve material e método: classificação, camadas de medição, braços, produto e especificação, limites, "
        "estatística e limitações. A seção 4 apresenta o orçamento, a seção 5 o cronograma e a seção 6 as referências."),
 "66": ("Segundo Ning et al. (2026, §2, tradução nossa), um *harness* “converte um modelo de linguagem sem estado em um "
        "agente funcional ao ancorar suas saídas em execução externa, estado persistente e realimentação verificável”. "
        "Wang et al. (2026) o descrevem pelo que faz: monta os *prompts*, gerencia o estado, invoca as ferramentas e "
        "coordena o laço. O pi é um laço próximo do ReAct mínimo (Yao et al., 2022), com quatro ferramentas; o OpenCode "
        "traz planejamento, compactação, subagentes e permissões. Lin et al. (2026) delimitam o que essa camada contém:"),
 "68": "É só esse conjunto que varia entre os braços deste experimento; o modelo fica fixo.",
 "69": ("A interface entre modelo e ambiente é objeto de projeto desde Yang et al. (2024). Na Tabela 1 de Lin et al. "
        "(2026), *harnesses* escritos por humanos sobre um modelo congelado (GPT-5.4, Terminal-Bench 2, 89 tarefas) vão "
        "de 47,2% de aprovação no OpenCode a 71,9% no Codex, 24,7 pontos percentuais (cálculo do autor). Zhang et al. "
        "(2026) enunciam a Binding Constraint Thesis: com modelos de fronteira comparáveis, a parcela do desempenho que "
        "vem do *harness* é comparável ou maior que a do modelo. Em Alier Forment et al. (2026), os dois *scaffoldings* "
        "sem MCP saíram de 5,0x a 28x mais baratos que os cinco com MCP, e o pi foi o mais barato. Três fontes não "
        "revisadas por pares apontam o mesmo. O HarnessRank (2026) ordena *harnesses* por aprovação com modelo fixo e "
        "publica custo ao lado. No FrontierHarness (Runta, 2026), o Codex conclui 66,7% das tarefas a US$ 3,47 por "
        "tarefa e o Claude Code 63,3% a US$ 18,34, 5,3x mais caro (cálculo do autor). A Databricks registra custo por "
        "tarefa variando mais de 2x sem mudança de qualidade (Databricks, 2026 apud Earendil, 2026)."),
 "70": ("A primeira pendência é a atribuição. As comparações publicadas usam tarefas isoladas e agregam *prompt*, "
        "ferramentas, contexto e laço sem separá-los. Ning et al. (2026) nomeiam a lacuna em §5.2.1 e pedem, em §5.2.7, "
        "“métricas que isolem componentes do *harness*” (Ning et al., 2026, tradução nossa). Lee et al. (2026, Tabela 7) "
        "mostram que essas decisões são isoláveis: uma busca que edita só o código do *harness*, com o modelo fixo, "
        "chegou a 76,4% no TerminalBench-2 (89 tarefas, Claude Opus 4.6) contra 74,7% do Terminus-KIRA, de onde partiu. "
        "Este projeto responde pelo lado da medição: separa, em cada requisição, a carga fixa do conteúdo da conversa, "
        "ao longo de um produto completo."),
 "71": ("A segunda pendência é a instrumentação. O que um *harness* relata sobre o próprio custo diverge do que gasta, "
        "e cada um omite um conjunto diferente de chamadas ao modelo. Kapoor et al. (2024) mostram que a avaliação de "
        "agentes ignora o custo e erra sobre a origem dos ganhos; Kapoor et al. (2025) registram que comparações entre "
        "*harnesses* são raras. A medição deste projeto ocorre em um *proxy* externo, e o objetivo (6) quantifica a "
        "divergência."),
 "72": ("As métricas serão tokens por construção, ao lado da fração de testes aprovados, e o Succ/Mtok (sucessos por "
        "milhão de tokens) de Lin et al. (2026). O efeito é específico do modelo e pode inverter de sinal: no Holistic "
        "Agent Leaderboard, os modelos da Anthropic vão melhor com o BrowserUse e os da OpenAI com o SeeAct (Kapoor et "
        "al., 2025), e o FrontierHarness registra, para o Claude Code, *cache* de 25,0% ponderado por tokens contra "
        "67,8% na célula mediana (Runta, 2026). O desenho terá dois níveis de modelo, com conclusões por nível."),
 "74": ("Quanto à finalidade, a pesquisa é aplicada; o produto é um critério de escolha para o desenvolvedor e a "
        "empresa. Quanto à abordagem, é quali-quantitativa: tokens e sucesso são medidas quantitativas, e a atribuição "
        "da diferença à carga fixa ou aos passos é qualitativa. Quanto aos objetivos, é exploratória, já que dois "
        "*harnesses* construindo o mesmo produto completo a partir da mesma especificação não têm precedente publicado. "
        "Quanto aos procedimentos, é experimental, com variável independente manipulada (o *harness*) e variáveis "
        "controladas (modelo, especificação, espaço de trabalho inicial e limites). Quanto ao método, é dedutiva, com "
        "hipóteses declaradas antes da coleta."),
 "75": ("Duas partes deste projeto usaram um agente de codificação, declarado conforme a Portaria CNPq nº 2.664/2026 "
        "(Brasil, 2026): a ferramenta foi o Claude Code e a finalidade foi entender o tema, buscar artigos e registrar "
        "as decisões de produto e de pilha do Finn antes do experimento. O levantamento das fontes seguiu o *LLM Wiki* "
        "de Karpathy (2026), mantido no repositório (YuukiFST, 2026c): fontes brutas guardadas sem alteração, páginas "
        "de síntese escritas pelo agente, registro cronológico e fila de revisão. O autor curou as fontes e conferiu "
        "cada afirmação citada na obra original. A especificação do Finn usou o Helmsman (YuukiFST, 2026a), rotina do "
        "autor que separa o que o sistema faz, respondido só pelo autor, de como construir, decidido pelo agente e "
        "registrado em *ticket* com alternativas e critério; decisões que dependem de fato externo passam por "
        "subagentes de pesquisa. O autor responde pelo texto final e por cada decisão de produto."),
 "76": ("A medição terá duas camadas. A Camada 1 mede a forma da requisição contra um *endpoint* simulado: esquemas de "
        "ferramenta, bytes de *prompt* de sistema e tokens por requisição, na primeira e a cada passo. É determinística, "
        "não consome cota e fornece a carga fixa de que H2 depende. A Camada 2 mede a construção do produto contra o "
        "modelo real; consome cota e é estocástica. Mais bytes por requisição não significam resultado pior; a Camada 2 "
        "diz quanto dessa carga chega ao resultado."),
 "77": ("Os braços serão o OpenCode (Opencode, 2026a) e o pi (Earendil, 2026): código aberto, sem interface (opencode "
        "run e pi --mode json) e URL base compatível com a API da OpenAI, o que os faz atravessar o *proxy*. O pi envia "
        "quatro ferramentas e um *prompt* de sistema curto, sem subagentes nem permissões; o OpenCode envia mais "
        "esquemas, *prompt* maior, subagentes, permissões e compactação de contexto. As versões serão fixadas e "
        "registradas no repositório (YuukiFST, 2026c). O projeto não escreve *harness* algum; escreve o instrumento, "
        "os *prompts* e os testes de aceitação."),
 "78": ("O produto será o Finn, SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e "
        "recebe lançamento, relatório e aviso no celular (YuukiFST, 2026b). Produto e pilha foram decididos antes do "
        "experimento em 21 *tickets* fechados. A partir deles o autor escreverá uma especificação única, congelada por "
        "SHA-256: produto, pilha (TypeScript, TanStack Start, tRPC, Drizzle ORM, PostgreSQL, Vitest), restrições e nove "
        "unidades, uma por *ticket* técnico, em ordem de dependência: separação por empresa, governança, *flags*, "
        "*pipeline* de voz, confirmação da transcrição, auditoria, relatório, agendador e cobrança. O executor invoca o "
        "*harness* uma vez por unidade, em ordem, com *prompt* idêntico para os dois braços; o que o agente construiu em "
        "uma unidade é o ponto de partida da seguinte, e o autor não escreve código no espaço de trabalho. A pontuação "
        "será a fração dos testes de aceitação aprovados, escritos pelo autor antes da execução, mantidos fora do espaço "
        "de trabalho e rodados sobre uma cópia dele ao fim de cada unidade; nunca os testes do próprio agente, já que um "
        "modelo que alucina uma API escreve testes que simulam a alucinação. Uma unidade conta como concluída quando "
        "todos os seus testes passam, e a construção, quando todos passam ao fim."),
 "79": ("Serão dois níveis de modelo, primário e de robustez, gratuitos e no mesmo *gateway* (Opencode, 2026b), "
        "relatados em separado, já que o efeito do *harness* é específico do modelo. Se a ordenação entre os braços se "
        "inverter entre os níveis, a inversão é o resultado."),
 "80": ("O instrumento será um *proxy* reverso entre cada braço e o *gateway*, que forçará o relatório de uso em cada "
        "requisição. Os tokens serão contados no *proxy*, sobre os bytes transmitidos, com um único tokenizador para os "
        "dois braços. O relatório do *harness* e o do *gateway* incluem conteúdo injetado que nenhum braço enviou, um "
        "deslocamento aditivo que não se cancela em razão e cobraria de cada braço um excedente proporcional ao número "
        "de passos. As contagens do *gateway* ficam para verificação cruzada e cálculo de custo, e a divergência será "
        "reportada por braço."),
 "81": ("Haverá um único limite, idêntico para os dois braços: relógio de parede por unidade, três vezes a maior mediana "
        "dos braços nas unidades-piloto. O número de passos não será limitado, porque um teto de passos é decisão de "
        "projeto de *harness* e apagaria a diferença sob teste. O comprimento máximo de saída será forçado igual pelo "
        "*proxy*. Os parâmetros de amostragem serão registrados sem normalização, já que o *gateway* não os honra e "
        "Miller (2024) desaconselha mexer na temperatura para reduzir variância. O isolamento de ambiente será "
        "verificado por um portão que falha fechado."),
 "82": ("Cada célula (braço, nível) receberá n ≥ 3 construções completas após descartes, na função redutora de variância "
        "que Miller (2024) atribui à reamostragem. Os resultados sairão como mediana com dispersão, já que requisições "
        "idênticas podem variar em tokens de saída no nível gratuito. Se a cota não comportar a matriz, a cobertura será "
        "reduzida antes das repetições."),
 "83": ("A medida principal será o total de tokens por construção, sempre ao lado da fração final de testes aprovados, "
        "para que um braço que falhe barato não pareça o mais barato. A comparação inferencial será o teste de Wilcoxon "
        "dos postos sinalizados, bilateral, α = 0,05, pareado por unidade, sobre tokens por unidade e Succ/Mtok por "
        "unidade: não paramétrico porque nove pares não sustentam suposição distribucional, pareado porque a dificuldade "
        "da unidade é o maior fator de perturbação (Miller, 2024). As unidades não são independentes, pois a seguinte "
        "parte do que o mesmo braço construiu; essa dependência é parte do custo do *harness* e será reportada por "
        "unidade. Com n = 3 e 9 unidades, a diferença mínima detectável é de cerca de 0,76σ. Para H2, os tokens de cada "
        "unidade serão decompostos em carga fixa (Camada 1 multiplicada pelo número de passos) e conversa, com a parcela "
        "de cada uma reportada por unidade e por construção. As predições serão pré-registradas por nível, e um "
        "resultado nulo para H2 será reportado."),
 "84": ("Cada unidade de cada construção receberá uma classe. Unidade não concluída é resultado: entra com a fração de "
        "testes aprovada e a construção segue, estouro de relógio incluído, já que repetir converteria indisponibilidade "
        "do serviço em diferença entre *harnesses*. Medição inconfiável descarta a construção inteira, registrada, sem "
        "reparo nem repetição. A classe vem do registro do *proxy*, porque o código de saída não discrimina o desfecho."),
 "86": ("Quatro limitações de partida. O efeito do *harness* é específico do modelo e pode inverter de sinal; as "
        "conclusões valem por nível, e o objetivo (5) testa isso. O produto é um único SaaS sobre uma única pilha; "
        "outras pilhas ficam como trabalho futuro. A especificação é do autor e cada braço carrega os próprios erros de "
        "uma unidade à seguinte; a mitigação é a mesma entrada, o mesmo espaço vazio e a comparação pareada por unidade. "
        "Os valores absolutos não são comparáveis a placares públicos, já que o produto é próprio; a comparação válida "
        "é entre os braços, e o custo em dinheiro entra como contrafactual rotulado sobre tarifas pagas publicadas."),
 "100": ("O total em dinheiro é zero. O limite real é a cota do nível gratuito do *gateway*, a ser medida nas "
         "unidades-piloto; cada construção rodará em lotes ao longo de dias, retomada na fronteira entre unidades, e o "
         "custo monetário aparecerá só como contrafactual sobre tarifas pagas publicadas."),
 "102": ("A cota gratuita é o limite vinculante, então a cadência é de um lote da matriz por dia. A folga fica na "
         "execução da matriz e na escrita da especificação e dos testes. Os meses vão de agosto de 2026 a janeiro de "
         "2027; a escrita do projeto foi concluída em setembro de 2026, mês de entrega, e os experimentos começam em "
         "outubro."),
}


# Second pass, measured in Word: justificativa back to 12 lines, objectives 1, 3, 4, 6
# to one line each; sumario page numbers for sections 3 and 5 follow the repagination.
P.update({
 "43": ("Os agentes de codificação avançam em duas frentes: o modelo de linguagem e a camada de software ao redor dele, "
        "o *harness* (Claude Code, Codex, Cursor, OpenCode, pi), que muda o que o mesmo modelo custa e entrega. No "
        "FrontierHarness (Runta, 2026), doze configurações de nove *harnesses* sobre o mesmo modelo ficam entre 50,0% e "
        "66,7% de aprovação, e o custo por tarefa concluída vai de US$ 1,05 a US$ 18,34; o pi conclui 60,0% a US$ 2,43 "
        "e o OpenCode 50,0% a US$ 3,24."),
 "44": ("As ferramentas seguem o mesmo movimento: Next.js, TanStack e Effect se adaptam ao trabalho de agentes. Escolher o modelo deixou de bastar; o desenvolvedor, na assinatura, e a empresa, em escala, precisam conhecer o que avança junto, e o *harness* é a parte dessa escolha que ninguém mediu na construção de um produto inteiro, já que as comparações publicadas usam tarefas isoladas. Este projeto mede esse custo construindo o Finn duas vezes, com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, com os tokens contados fora do *harness*."),
 "52": "1) construir o instrumento externo que conta requisições, tokens e latência por braço;",
 "54": "3) preparar o espaço de trabalho inicial idêntico para os braços, congelado por hash;",
 "55": "4) construir o Finn nos dois *harnesses*, mesmo modelo e *prompts*, com repetição;",
 "57": "6) medir a divergência entre tokens relatados pelo *harness* e medidos no instrumento;",
})
SUMARIO_PAGES = {37: ("5", "4"), 39: ("8", "7")}  # paragraph index: (old, new)


def main() -> None:
    edits = Path("tmp/edits_2026-09-18.json")
    edits.parent.mkdir(exist_ok=True)
    edits.write_text(json.dumps({"paragraphs": P}, ensure_ascii=False, indent=1), encoding="utf-8")
    subprocess.run([sys.executable, "tools/docx_prose.py", "apply", str(DOCX), str(edits)], check=True)

    # Drop the author's yellow highlight: it marked the title and the theme for rewrite.
    with zipfile.ZipFile(DOCX) as z:
        infos = z.infolist()
        items = {i.filename: z.read(i.filename) for i in infos}
    xml = items["word/document.xml"].decode("utf-8")
    print("highlight runs removed:", xml.count("<w:highlight"))
    xml = re.sub(r"<w:highlight[^>]*/>", "", xml)
    paras = re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)
    for idx, (old, new) in SUMARIO_PAGES.items():
        fixed = paras[idx].replace(f">{old}</w:t>", f">{new}</w:t>")
        assert fixed != paras[idx]
        xml = xml.replace(paras[idx], fixed, 1)
    items["word/document.xml"] = xml.encode("utf-8")
    fd, name = tempfile.mkstemp(suffix=".docx")
    os.close(fd)
    with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in infos:
            dst.writestr(info, items[info.filename])
    shutil.move(name, DOCX)


if __name__ == "__main__":
    main()
