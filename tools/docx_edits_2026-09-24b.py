"""Second edit of dist/projeto-de-pesquisa.docx, 2026-09-24, run after
tools/docx_edits_2026-09-24.py on the author's docx.

Closes citation and list both ways (Aula 3; Aula 5: the list identifies the
sources used in the text):
- The author removed the BRASIL entry (Portaria CNPq, off theme), so [74]
  stops citing it; the AI-use declaration stays, without the norm.
- The author removed the in-text citations of YuukiFST 2026b (Finn) and 2026c
  (harness-bench) but kept both entries. An entry with no citation breaks the
  rule, so [77] cites 2026b again and [76] cites 2026c again (it had been left
  as "no repositório ." with a stray space).
Also fixes typos in the author's revision: [43] broken italics ("*coding
**agent*"), "muda influência" and a "nesse benchmark" with no antecedent;
[48] stray "porém", "ao invés de" (means the opposite; "em vez de" is the
substitution), the space before "?", and harness in italics; [69] "pi" where
the author wrote "PI" everywhere else.
The no-ai-slop skill ran on the changed sentences.
The two restored citations push 6 REFERÊNCIAS to the next page (Word: 10
pages), which the author allows for references, so the sumário line moves
from 5 to 6.

Run once, after tools/docx_edits_2026-09-24.py: python tools/docx_edits_2026-09-24b.py
"""
import json
import re
import sys
import zipfile
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from docx_prose import _rewrite_zip, apply  # noqa: E402

DOCX = Path("dist/projeto-de-pesquisa.docx")
SUMARIO = {"1 INTRODUÇÃO": "1", "2 REFERENCIAL TEÓRICO": "2", "3 MATERIAL E MÉTODO": "3",
           "4 ORÇAMENTO": "5", "5 CRONOGRAMA": "5", "6 REFERÊNCIAS": "6"}
EDITS = json.loads(r"""
{
 "paragraphs": {
  "43": "Um *coding agent* tem duas partes: o modelo de linguagem e o *harness*, o software ao redor dele que monta o contexto, expõe as ferramentas e conduz a execução. Pan *et al.* (2026), da Universidade da Califórnia em Berkeley, avaliaram sete modelos em três *harnesses* e concluíram que a escolha do *harness* influencia notavelmente o custo. No SWE-bench Lite, o Claude Fable 5 resolve 97,8% das tentativas no Claude Code e 96,7% no PI, e o Claude Code custa cerca do dobro por tentativa (US$ 1,33 contra US$ 0,67).",
  "48": "Com o modelo fixo, quanto a escolha do *harness* pode influenciar no custo e na taxa de sucesso ao construir o mesmo software com um *harness* em vez de outro?",
  "69": "A primeira pendência é saber de onde vem a diferença de custo. Pan *et al.* (2026) apontam a primeira requisição. O contexto inicial do Claude Code passa de dez vezes o do PI, com número de turnos parecido (15,3 contra 15,4 no Claude Fable 5). Liu *et al.* (2026) apontam o resto da conversa. Mudando só a execução das ações, a compactação de contexto e o tratamento das observações, cortaram de 44,7% a 49,0% dos tokens em relação ao PI e mantiveram de 93,7% a 94,3% da pontuação dele. Ning *et al.* (2026, §5.2.7, tradução nossa) pedem “métricas que isolem componentes do *harness*”, e H2 testa se pesa mais a carga fixa ou a conversa.",
  "74": "Declara-se o uso do Claude Code no levantamento das fontes, organizado pelo método *LLM Wiki* de Karpathy (2026) no repositório do projeto (YuukiFST, 2026c), nas decisões do Finn, mapeadas com o Helmsman (YuukiFST, 2026a), e na sua versão de referência. O autor conferiu cada afirmação citada na obra original e responde pelo texto e pelas decisões de produto.",
  "76": "Os braços serão o OpenCode (Opencode, 2026a) e o PI (Earendil, 2026). Os dois são de código aberto, rodam sem interface e aceitam URL base compatível com a API da OpenAI, o que permite passá-los pelo *proxy*. As versões serão fixadas e registradas no repositório (YuukiFST, 2026c).",
  "77": "O produto será o Finn, SaaS multiempresa em que a empresa cliente fala com o próprio financeiro por voz e recebe lançamento, relatório e aviso no celular (YuukiFST, 2026b), decidido em 21 *tickets*. O autor construirá antes uma versão de referência e marcará no git o fim de cada etapa. Dela sairá a especificação, congelada por SHA-256: produto, pilha, interface dos testes e funcionalidades em JSON, no formato de Young (2025), uma unidade por etapa, ao menos seis. O executor chama o *harness* uma vez por unidade, com o mesmo *prompt* nos dois braços, e cada unidade parte do que o agente construiu na anterior. Nenhum código do autor entra no espaço de trabalho."
 }
}
""")


def main() -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(EDITS, f, ensure_ascii=False)
    apply(DOCX, Path(f.name))
    Path(f.name).unlink()
    set_sumario()


def set_sumario() -> None:
    # Same as docx_edits_2026-09-23.py: the sumário is static text after a tab.
    xml = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf-8")
    for heading, page in SUMARIO.items():
        pattern = re.compile(r'(<w:t xml:space="preserve">' + re.escape(heading)
                             + r'</w:t><w:tab/><w:t xml:space="preserve">)\d+(</w:t>)')
        xml, hits = pattern.subn(r"\g<1>" + page + r"\g<2>", xml)
        if hits != 1:
            raise SystemExit(f"sumário line {heading!r} matched {hits} times")
    _rewrite_zip(DOCX, {"word/document.xml": xml.encode("utf-8")})


if __name__ == "__main__":
    main()
