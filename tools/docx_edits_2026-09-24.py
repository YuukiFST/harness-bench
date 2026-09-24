"""Edit of dist/projeto-de-pesquisa.docx, 2026-09-24.

The author changed how the specification comes to exist: the author first
builds a reference Finn until it is the product they want, tagging the end of
each stage in git, and the specification is extracted from that reference.
The nine units taken from Finn tickets #14-#22 are gone; the units are the
reference's stages, at least six (the smallest count at which a two-sided
Wilcoxon signed-rank test can reach p < 0.05). The acceptance tests must pass
on the reference at each unit's tag before the specification is frozen.
The feature list follows the JSON format of Young (2025;
wiki/sources/effective-harnesses-young-2025.md), cited in [77] and listed in
section 6; the author allowed the page count to grow for references.
The no-ai-slop skill ran on the prose before the pass was applied.

Indices come from `docx_prose.py dump` on the author's 2026-09-24 docx (placed
over the working tree after 8341dfd; it has no BRASIL entry and six months in
Tabela 2).

Run once on that docx: python tools/docx_edits_2026-09-24.py
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from docx_prose import apply  # noqa: E402

DOCX = Path("dist/projeto-de-pesquisa.docx")
EDITS = json.loads(r"""
{
 "paragraphs": {
  "53": "2) construir o Finn de referência e extrair dele a especificação e os testes;",
  "59": "Pesquisa aplicada, quali-quantitativa, exploratória e experimental, de método dedutivo. Um *proxy* reverso entre cada *harness* e o modelo contará requisições, tokens e latência da mesma forma para os dois braços. Cada braço construirá o Finn do zero ao menos três vezes, a partir da especificação extraída do Finn de referência do autor, e a diferença entre os braços será comparada unidade a unidade.",
  "74": "Conforme a Portaria CNPq nº 2.664/2026 (Brasil, 2026), declara-se o uso do Claude Code no levantamento das fontes, organizado pelo método *LLM Wiki* de Karpathy (2026) no repositório do projeto (YuukiFST, 2026c), nas decisões do Finn, mapeadas com o Helmsman (YuukiFST, 2026a), e na sua versão de referência. O autor conferiu cada afirmação citada na obra original e responde pelo texto e pelas decisões de produto.",
  "77": "O produto será o Finn, SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e recebe lançamento, relatório e aviso no celular, decidido em 21 *tickets*. O autor construirá antes uma versão de referência e marcará no git o fim de cada etapa. Dela sairá a especificação, congelada por SHA-256: produto, pilha, interface dos testes e funcionalidades em JSON, no formato de Young (2025), uma unidade por etapa, ao menos seis. O executor chama o *harness* uma vez por unidade, com o mesmo *prompt* nos dois braços, e cada unidade parte do que o agente construiu na anterior. Nenhum código do autor entra no espaço de trabalho.",
  "78": "A pontuação será a fração dos testes de aceitação aprovados. O autor escreverá os testes antes da execução, fora do espaço de trabalho, e os rodará sobre uma cópia dele ao fim de cada unidade. Todos devem passar antes na referência, no marco da etapa. Os testes escritos pelo agente não contam, e uma unidade conta como concluída quando todos os seus testes passam.",
  "86": "O projeto tem quatro limitações. O efeito do *harness* depende do modelo, então as conclusões valem por nível. O produto é um único SaaS, especificado a partir da solução do autor. Cada braço carrega os próprios erros de uma unidade à seguinte, então as unidades não são independentes, embora o teste de Wilcoxon suponha que sejam; o valor-p será lido como indicativo, ao lado da diferença e da dispersão. Por fim, o nível gratuito do *gateway* pode trocar o modelo ou cortar a cota durante a coleta.",
  "123": "FINN DE REFERÊNCIA, PROXY E TESTES"
 },
 "insert_after": {
  "189": "YOUNG, Justin. **Effective harnesses for long-running agents**. 2025. Publicação de blogue de engenharia (Anthropic), não revisada por pares. Disponível em: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents. Acesso em: 24 set. 2026."
 }
}
""")


def main() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(EDITS, f, ensure_ascii=False)
    apply(DOCX, Path(f.name))
    Path(f.name).unlink()


if __name__ == "__main__":
    main()
