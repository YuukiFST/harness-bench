"""Prose pass over dist/projeto-de-pesquisa.docx, 2026-09-18, second script of the day.

Pass 1 (no-ai-slop): remove the patterns listed in
docs/research/estrutura-do-projeto-e-revisao.md section 5 (causal closers,
colon cadence, "not X; Y" contrasts, aphoristic closers, fragment openers).
Pass 2 (humanizer): staging words, long single sentences, one-line closers.
Facts, numbers, denominators and citations unchanged. Direct quotes untouched.
Indices are from `docx_prose.py dump` after tools/docx_edits_2026-09-18.py.

Run once: python tools/docx_edits_2026-09-18b.py
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
# Section 2 starts on printed page 2 (Word 2026-09-18, Information(1)); the
# summary still said 3 since the 2026-09-14 rewrite.
SUMARIO_PAGES = {36: ("3", "2")}  # paragraph index: (old, new)

P = {
 "44": ("Ferramentas como Next.js, TanStack e Effect também se adaptam ao trabalho de agentes. Escolher o modelo "
        "deixou de bastar; o desenvolvedor, na assinatura, e a empresa, em escala, precisam conhecer o que avança "
        "junto, e o *harness* é a parte dessa escolha que ninguém mediu na construção de um produto inteiro. As "
        "comparações publicadas usam tarefas isoladas. Este projeto mede esse custo construindo o Finn duas vezes, "
        "com o OpenCode e com o pi, sobre o mesmo modelo e a mesma especificação, com os tokens contados fora do "
        "*harness*."),
 "70": ("A primeira pendência é a atribuição. As comparações publicadas usam tarefas isoladas e agregam *prompt*, "
        "ferramentas, contexto e laço sem separá-los. Ning et al. (2026) nomeiam a lacuna em §5.2.1 e pedem, em "
        "§5.2.7, “métricas que isolem componentes do *harness*” (Ning et al., 2026, tradução nossa). Lee et al. "
        "(2026, Tabela 7) mostram que essas decisões são isoláveis. Uma busca que edita só o código do *harness*, "
        "com o modelo fixo, chegou a 76,4% no TerminalBench-2 (89 tarefas, Claude Opus 4.6) contra 74,7% do "
        "Terminus-KIRA, de onde partiu. Este projeto responde pelo lado da medição e separa, em cada requisição, a "
        "carga fixa do conteúdo da conversa, ao longo de um produto completo."),
 "72": ("As métricas serão tokens por construção, ao lado da fração de testes aprovados, e o Succ/Mtok (sucessos por "
        "milhão de tokens) de Lin et al. (2026). O efeito é específico do modelo e pode inverter de sinal. No "
        "Holistic Agent Leaderboard, os modelos da Anthropic vão melhor com o BrowserUse e os da OpenAI com o SeeAct "
        "(Kapoor et al., 2025), e o FrontierHarness registra, para o Claude Code, *cache* de 25,0% ponderado por "
        "tokens contra 67,8% na célula mediana (Runta, 2026). O desenho terá dois níveis de modelo, com conclusões "
        "por nível."),
 "74": ("Quanto à finalidade, a pesquisa é aplicada; o produto é um critério de escolha para o desenvolvedor e a "
        "empresa. Quanto à abordagem, é quali-quantitativa: tokens e sucesso são medidas quantitativas, e a "
        "atribuição da diferença à carga fixa ou aos passos é qualitativa. Quanto aos objetivos, é exploratória; "
        "dois *harnesses* construindo o mesmo produto completo a partir da mesma especificação não têm precedente "
        "publicado. Quanto aos procedimentos, é experimental, com variável independente manipulada (o *harness*) e "
        "variáveis controladas (modelo, especificação, espaço de trabalho inicial e limites). Quanto ao método, é "
        "dedutiva, com hipóteses declaradas antes da coleta."),
 "75": ("Duas partes deste projeto usaram um agente de codificação, declarado conforme a Portaria CNPq nº 2.664/2026 "
        "(Brasil, 2026). A ferramenta foi o Claude Code; a finalidade, entender o tema, buscar artigos e registrar "
        "as decisões de produto e de pilha do Finn antes do experimento. O levantamento das fontes seguiu o *LLM "
        "Wiki* de Karpathy (2026), mantido no repositório (YuukiFST, 2026c): fontes brutas guardadas sem alteração, "
        "páginas de síntese escritas pelo agente, registro cronológico e fila de revisão. O autor curou as fontes e "
        "conferiu cada afirmação citada na obra original. A especificação do Finn usou o Helmsman (YuukiFST, 2026a), "
        "rotina do autor que separa o que o sistema faz, respondido só pelo autor, de como construir, decidido pelo "
        "agente e registrado em *ticket* com alternativas e critério; decisões que dependem de fato externo passam "
        "por subagentes de pesquisa. O autor responde pelo texto final e por cada decisão de produto."),
 "76": ("A medição terá duas camadas. A Camada 1 mede a forma da requisição contra um *endpoint* simulado: esquemas "
        "de ferramenta, bytes de *prompt* de sistema e tokens por requisição, na primeira e a cada passo. É "
        "determinística, não consome cota e fornece a carga fixa de que H2 depende. A Camada 2 mede a construção "
        "do produto contra o modelo real; consome cota e é estocástica. A Camada 2 também diz quanto dessa carga por "
        "requisição pesa no resultado."),
 "77": ("Os braços serão o OpenCode (Opencode, 2026a) e o pi (Earendil, 2026): código aberto, sem interface "
        "(opencode run e pi --mode json) e URL base compatível com a API da OpenAI, o que os faz atravessar o "
        "*proxy*. O pi envia quatro ferramentas e um *prompt* de sistema curto, sem subagentes nem permissões; o "
        "OpenCode envia mais esquemas, *prompt* maior, subagentes, permissões e compactação de contexto. As versões "
        "serão fixadas e registradas no repositório (YuukiFST, 2026c). O projeto escreve apenas o instrumento, os "
        "*prompts* e os testes de aceitação."),
 "78": ("O produto será o Finn, SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e "
        "recebe lançamento, relatório e aviso no celular (YuukiFST, 2026b). Produto e pilha foram decididos antes do "
        "experimento em 21 *tickets* fechados. A partir deles o autor escreverá uma especificação única, congelada "
        "por SHA-256: produto, pilha (TypeScript, TanStack Start, tRPC, Drizzle ORM, PostgreSQL, Vitest), restrições "
        "e nove unidades, uma por *ticket* técnico, em ordem de dependência: separação por empresa, governança, "
        "*flags*, *pipeline* de voz, confirmação da transcrição, auditoria, relatório, agendador e cobrança. O "
        "executor invoca o *harness* uma vez por unidade, em ordem, com *prompt* idêntico para os dois braços; o que "
        "o agente construiu em uma unidade é o ponto de partida da seguinte, e o autor não escreve código no espaço "
        "de trabalho. A pontuação será a fração dos testes de aceitação aprovados. O autor os escreverá antes da "
        "execução, os manterá fora do espaço de trabalho e os rodará sobre uma cópia dele ao fim de cada unidade. Os "
        "testes do próprio agente não contam, porque um modelo que alucina uma API escreve testes que simulam a "
        "alucinação. Uma unidade conta como concluída quando todos os seus testes passam, e a construção, quando "
        "todos passam ao fim."),
 "79": ("Serão dois níveis de modelo, primário e de robustez, gratuitos e no mesmo *gateway* (Opencode, 2026b), com "
        "resultados relatados por nível. Uma inversão da ordenação entre os braços de um nível para o outro será "
        "reportada como resultado."),
 "81": ("Haverá um único limite, idêntico para os dois braços: relógio de parede por unidade, três vezes a maior "
        "mediana dos braços nas unidades-piloto. O número de passos não será limitado, porque um teto de passos é "
        "decisão de projeto de *harness* e apagaria a diferença sob teste. O comprimento máximo de saída será forçado "
        "igual pelo *proxy*. Os parâmetros de amostragem serão registrados sem normalização. O *gateway* não os "
        "honra, e Miller (2024) desaconselha mexer na temperatura para reduzir variância. O isolamento de ambiente "
        "será verificado por um portão que falha fechado."),
 "82": ("Cada célula (braço, nível) receberá n ≥ 3 construções completas após descartes, na função redutora de "
        "variância que Miller (2024) atribui à reamostragem. Os resultados sairão como mediana com dispersão; no "
        "nível gratuito, requisições idênticas podem variar em tokens de saída. Se a cota não comportar a matriz, a "
        "cobertura será reduzida antes das repetições."),
 "83": ("A medida principal será o total de tokens por construção, sempre ao lado da fração final de testes "
        "aprovados, para que um braço que falhe barato não pareça o mais barato. A comparação inferencial será o "
        "teste de Wilcoxon dos postos sinalizados, bilateral, α = 0,05, pareado por unidade, sobre tokens por unidade "
        "e Succ/Mtok por unidade. O teste é não paramétrico porque nove pares não sustentam suposição distribucional, "
        "e pareado porque a dificuldade da unidade é o maior fator de perturbação (Miller, 2024). As unidades não "
        "são independentes, pois a seguinte parte do que o mesmo braço construiu; essa dependência é parte do custo "
        "do *harness* e será reportada por unidade. Com n = 3 e 9 unidades, a diferença mínima detectável é de cerca "
        "de 0,76σ. Para H2, os tokens de cada unidade serão decompostos em carga fixa (Camada 1 multiplicada pelo "
        "número de passos) e conversa, com a parcela de cada uma reportada por unidade e por construção. As "
        "predições serão pré-registradas por nível, e um resultado nulo para H2 será reportado."),
 "84": ("Cada unidade de cada construção receberá uma classe. Unidade não concluída conta como resultado, com a "
        "fração de testes aprovada, e a construção segue, estouro de relógio incluído; repetir converteria "
        "indisponibilidade do serviço em diferença entre *harnesses*. Medição inconfiável descarta a construção "
        "inteira, registrada, sem reparo nem repetição. A classe vem do registro do *proxy*; o código de saída não "
        "discrimina o desfecho."),
 "86": ("O projeto parte de quatro limitações. O efeito do *harness* é específico do modelo e pode inverter de "
        "sinal; as conclusões valem por nível, e o objetivo (5) testa isso. O produto é um único SaaS sobre uma "
        "única pilha; outras pilhas ficam como trabalho futuro. A especificação é do autor e cada braço carrega os "
        "próprios erros de uma unidade à seguinte; a mitigação é a mesma entrada, o mesmo espaço vazio e a "
        "comparação pareada por unidade. Como o produto é próprio, os valores absolutos não são comparáveis a "
        "placares públicos; a comparação válida é entre os braços, e o custo em dinheiro entra como contrafactual "
        "rotulado sobre tarifas pagas publicadas."),
 "100": ("O total em dinheiro é zero; o limite é a cota do nível gratuito do *gateway*, a ser medida nas "
         "unidades-piloto. Cada construção rodará em lotes ao longo de dias, retomada na fronteira entre unidades, e "
         "o custo monetário aparecerá só como contrafactual sobre tarifas pagas publicadas."),
}


def main() -> None:
    edits = Path("tmp/edits_2026-09-18b.json")
    edits.parent.mkdir(exist_ok=True)
    edits.write_text(json.dumps({"paragraphs": P}, ensure_ascii=False, indent=1), encoding="utf-8")
    subprocess.run([sys.executable, "tools/docx_prose.py", "apply", str(DOCX), str(edits)], check=True)

    with zipfile.ZipFile(DOCX) as z:
        infos = z.infolist()
        items = {i.filename: z.read(i.filename) for i in infos}
    xml = items["word/document.xml"].decode("utf-8")
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
