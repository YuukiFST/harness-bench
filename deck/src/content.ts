// Conteúdo congelado do deck: textos, números e ordem dos 15 slides.
// Fonte: dist/apresentacao-pcc.html (auditado). Não alterar palavras nem números.
// Qualquer correção aparente vai para _review.md, nunca para edição direta.

export interface FrontierRow {
  name: string;
  pass: number;
  costPerPass: number;
}

export interface HarnessNode {
  id: number;
  name: string;
  text: string;
  src: string;
  pos: [number, number, number];
  color: string;
  sphere?: boolean;
  flat?: boolean;
}

export interface Layer1Arm {
  first: number;
  tok: number;
  schemas: number;
  steps: [number, number, number, number, number];
}

export interface TimelineNode {
  year: string;
  title: string;
  claim: string;
}

export interface GanttRow {
  phase: string;
  months: [number, number, number, number, number];
}

export const FH: FrontierRow[] = [
  { name: "Exo", pass: 53.3, costPerPass: 1.05 },
  { name: "Pi", pass: 60.0, costPerPass: 2.43 },
  { name: "OpenCode", pass: 50.0, costPerPass: 3.24 },
  { name: "DSH Creator", pass: 63.3, costPerPass: 3.28 },
  { name: "Codex", pass: 66.7, costPerPass: 3.47 },
  { name: "oh-my-pi", pass: 56.7, costPerPass: 4.75 },
  { name: "Claude Code", pass: 63.3, costPerPass: 18.34 },
];

export const FH_META = {
  title: "Mesmo modelo, custo por tarefa 17,5× diferente",
  subtitle:
    "FrontierHarness (Runta, 2026): 12 configurações de 9 <em>harnesses</em>, modelo Kimi K3, 30 tarefas, 1 tentativa por célula, set. 2026",
  denom:
    "Aprovação 50,0–66,7 % e US$ 1,05–18,34 nas 12 configurações; o gráfico mostra as 7 com valor no texto do post. Razão 17,5× calculada pelo autor. Blogue institucional, não revisado por pares.",
} as const;

export const H3: HarnessNode[] = [
  {
    id: 0,
    name: "Modelo de linguagem",
    text: "Sem estado. Fixo em todos os braços. Tudo ao redor é o <em>harness</em>: componentes externos ao modelo e editáveis.",
    src: "Lin <em>et al.</em> (2026, §1)",
    pos: [0, 0, 0],
    color: "#f5b638",
    sphere: true,
  },
  {
    id: 1,
    name: "Prompt de sistema",
    text: "Molda o estilo de trabalho. Na Camada 1, pi envia 2.499 bytes; oh-my-pi, 25.395 (10,2×).",
    src: "Lin <em>et al.</em> (2026, §1); layer1/data, 28 ago. 2026",
    pos: [-3.6, 0.6, 0.9],
    color: "#3b7bd6",
  },
  {
    id: 2,
    name: "Ferramentas",
    text: "Expõem sistema de arquivos e shell ao modelo. Esquemas viajam a cada requisição: 4 no pi, 11 no oh-my-pi.",
    src: "Lin <em>et al.</em> (2026, §1); layer1/data",
    pos: [3.6, 0.6, 0.9],
    color: "#3b7bd6",
  },
  {
    id: 3,
    name: "Middleware de contexto",
    text: "Controla contexto, execução e recuperação: compactação, memória, permissões, verificação.",
    src: "Lin <em>et al.</em> (2026, §1); Ning <em>et al.</em> (2026, §2)",
    pos: [0, 0.6, -3.8],
    color: "#3b7bd6",
  },
  {
    id: 4,
    name: "Laço de execução",
    text: "Monta prompts, gerencia estado, invoca ferramentas, coordena o laço. Do ReAct mínimo ao planejamento com subagentes.",
    src: "Wang <em>et al.</em> (2026); Yao <em>et al.</em> (2022)",
    pos: [0, 0.6, 3.8],
    color: "#3b7bd6",
  },
  {
    id: 5,
    name: "Proxy externo",
    text: "Fora do <em>harness</em>: instrumento do projeto. Conta requisições, tokens e latência igual para todos os braços.",
    src: "Projeto, §3 [63]; objetivo 1",
    pos: [0, -3.3, 0],
    color: "#7bd88f",
    flat: true,
  },
];

export const L1: { pi: Layer1Arm; omp: Layer1Arm } = {
  pi: { first: 5676, tok: 1228, schemas: 4, steps: [5676, 6231, 6786, 7341, 7896] },
  omp: { first: 64945, tok: 16714, schemas: 11, steps: [64945, 65273, 65898, 66523, 67148] },
};

export const TL: TimelineNode[] = [
  {
    year: "2022",
    title: "Yao <em>et al.</em> · ReAct",
    claim:
      "O laço observar/agir mínimo. É um <em>harness</em> legítimo, o mais raso; ponto de partida do <em>harness</em> zero.",
  },
  {
    year: "2024",
    title: "Yang <em>et al.</em> · SWE-agent",
    claim: "A interface entre modelo e ambiente é objeto de projeto desde aqui: melhora sem tocar nos pesos.",
  },
  {
    year: "2024",
    title: "Kapoor <em>et al.</em> · AI agents that matter",
    claim: "A avaliação de agentes ignora o custo e por isso erra sobre a origem dos ganhos.",
  },
  {
    year: "2025",
    title: "Kapoor <em>et al.</em> · HAL",
    claim:
      "Avaliações raramente relatam custo; comparações entre <em>harnesses</em> são raras. Anthropic vai melhor com BrowserUse, OpenAI com SeeAct: efeito específico do modelo.",
  },
  {
    year: "2026",
    title: "Lin <em>et al.</em> · Agentic Harness Engineering",
    claim:
      "Definição operacional e Succ/Mtok. Tabela 1: 47,2 % (OpenCode) a 71,9 % (Codex), GPT-5.4, Terminal-Bench 2, 89 tarefas; 24,7 pp (cálculo do autor).",
  },
  {
    year: "2026",
    title: "Zhang <em>et al.</em> · Binding Constraint Thesis",
    claim:
      "Com modelos de fronteira comparáveis, a parcela do <em>harness</em> é frequentemente comparável ou maior que a do modelo, e pode dominá-la.",
  },
  {
    year: "2026",
    title: "Lee <em>et al.</em> · Meta-Harness",
    claim:
      "Editar só o código do <em>harness</em>, modelo fixo: 76,4 % contra 74,7 % do Terminus-KIRA (TerminalBench-2, 89 tarefas, Claude Opus 4.6). Decisões são isoláveis.",
  },
  {
    year: "2026",
    title: "Ning <em>et al.</em> · Code as agent harness",
    claim:
      "Definição: converte um modelo sem estado em agente funcional. §5.2.1 nomeia a lacuna de atribuição; §5.2.7 pede métricas por componente.",
  },
  {
    year: "2026",
    title: "Wang <em>et al.</em> · Harness Handbook",
    claim: "O <em>harness</em> monta os prompts, gerencia o estado, invoca as ferramentas e coordena o laço.",
  },
  {
    year: "2026",
    title: "Runta · FrontierHarness",
    claim:
      "12 configurações, Kimi K3: 50,0–66,7 % e US$ 1,05–18,34 por tarefa concluída. Cache do Claude Code 25,0 % ponderado vs 67,8 % na célula mediana.",
  },
];

export const GANTT_MONTHS: string[] = ["Set", "Out", "Nov", "Dez", "Jan"];

export const GANTT: GanttRow[] = [
  { phase: "Leitura e levantamento bibliográfico", months: [1, 1, 0, 0, 0] },
  { phase: "Definição do tema, do problema e das hipóteses", months: [1, 1, 0, 0, 0] },
  { phase: "Construção do instrumento e do harness zero", months: [0, 1, 1, 0, 0] },
  { phase: "Escrevendo introdução", months: [0, 0, 1, 0, 0] },
  { phase: "Escrevendo referencial teórico", months: [0, 0, 1, 0, 0] },
  { phase: "Escrevendo material e método", months: [0, 0, 1, 1, 0] },
  { phase: "Execução da matriz de experimentos", months: [0, 0, 0, 1, 1] },
  { phase: "Análise dos resultados", months: [0, 0, 0, 0, 1] },
  { phase: "Elaborando as referências", months: [0, 0, 0, 0, 1] },
  { phase: "Revisão final e preparação da apresentação", months: [0, 0, 0, 0, 1] },
];

export const REFS: string[] = [
  "ALIER FORMENT, M. <em>et al.</em> <b>The scaffolding matters more than the interface</b>. arXiv:2608.08654, 2026. <em>Preprint</em>.",
  "BRASIL. CNPq. <b>Portaria CNPq nº 2.664, de 6 de março de 2026</b>. Política de Integridade na Atividade Científica. DOU, 11 mar. 2026.",
  "DATACURVE. <b>Pier</b>: a Harbor fork built for DeepSWE. 2026. Repositório de código.",
  "GIL, A. C. <b>Como elaborar projetos de pesquisa</b>. 7. ed. São Paulo: Atlas, 2022.",
  "HUANG, W. <em>et al.</em> <b>DeepSWE</b>: measuring frontier coding agents on original, long-horizon engineering tasks. arXiv:2607.07946, 2026. <em>Preprint</em>.",
  "JIMENEZ, C. E. <em>et al.</em> <b>SWE-bench</b>: can language models resolve real-world GitHub issues? ICLR, 2024.",
  "KAPOOR, S. <em>et al.</em> <b>AI agents that matter</b>. arXiv:2407.01502, 2024. <em>Preprint</em>.",
  "KAPOOR, S. <em>et al.</em> <b>Holistic Agent Leaderboard</b>. arXiv:2510.11977, 2025. <em>Preprint</em>.",
  "LEE, Y. <em>et al.</em> <b>Meta-Harness</b>: end-to-end optimization of model harnesses. arXiv:2603.28052, 2026. <em>Preprint</em>.",
  "LIN, J. <em>et al.</em> <b>Agentic harness engineering</b>. arXiv:2604.25850, 2026. <em>Preprint</em>.",
  "MILLER, E. <b>Adding error bars to evals</b>. arXiv:2411.00640, 2024. <em>Preprint</em>.",
  "NING, X. <em>et al.</em> <b>Code as agent harness</b>. arXiv:2605.18747, 2026. <em>Preprint</em>.",
  "PRODANOV, C. C.; FREITAS, E. C. de. <b>Metodologia do trabalho científico</b>. 2. ed. Novo Hamburgo: Feevale, 2013.",
  "RUNTA. <b>Introducing the FrontierHarness eval</b>. 2026. Blogue institucional.",
  "WANG, R. <em>et al.</em> <b>Harness Handbook</b>. arXiv:2607.13285, 2026. <em>Preprint</em>.",
  "YANG, J. <em>et al.</em> <b>SWE-agent</b>: agent-computer interfaces enable automated software engineering. NeurIPS, 2024.",
  "YAO, S. <em>et al.</em> <b>ReAct</b>: synergizing reasoning and acting in language models. ICLR, 2023.",
  "YUUKIFST. <b>harness-bench</b>: runner, dados brutos e scripts de análise deste projeto. 2026. Repositório de código.",
  "ZHANG, Y. <em>et al.</em> <b>Stop comparing LLM agents without disclosing the harness</b>. arXiv:2605.23950, 2026. <em>Preprint</em>.",
];

export const MATRIX_ARMS: string[] = ["harness zero", "pi", "oh-my-pi", "terceiros…"];
export const MATRIX_TIERS: string[] = ["nível primário", "nível de robustez"];
export const MATRIX_TASKS = 8;

export const CLASS_AXES: { k: string; v: string; w: string }[] = [
  { k: "Natureza", v: "aplicada", w: "produto: critério de escolha" },
  { k: "Abordagem", v: "quanti + quali", w: "medir custo e sucesso; atribuir a decisão" },
  { k: "Objetivos", v: "exploratória", w: "linhagem fixa sem precedente" },
  {
    k: "Procedimentos",
    v: "experimental",
    w: "VI: <em>harness</em> · controladas: modelo, tarefa, limites · grupo de controle",
  },
  { k: "Método", v: "dedutivo", w: "hipóteses antes da coleta" },
];

export const OBJECTIVES: string[] = [
  "<b>1</b> Instrumento externo: requisições, tokens, latência",
  "<b>2</b> Suíte com objetivos numerados e <em>oracle</em> próprio",
  "<b>3</b> <em>Harness</em> zero em laço ReAct (controle)",
  "<b>4</b> Mesma suíte, mesmo modelo, todos os braços, com repetição",
  "<b>5</b> Segundo modelo: a ordenação se mantém ou inverte?",
  "<b>6</b> Custo relatado × custo medido no <em>proxy</em>",
  "<b>7</b> Publicar <em>runner</em>, dados e scripts, custo zero",
];
