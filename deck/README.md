# Apresentação PCC — deck reconstruído

Deck da apresentação oral do projeto de pesquisa "O harness como decisão do desenvolvedor"
(Metodologia Científica, IFMT). Conteúdo (textos, números, notas, ordem dos 17 slides)
congelado de `../dist/apresentacao-pcc.html` na versão de 2026-09-14 (experimento Finn:
OpenCode vs pi): não alterar palavras nem números. Mudança de conteúdo passa por
`tools/deck_edits_<data>.py`, espelhando `tools/slides_edits_<data>.py`.

## Stack

- Vite 7 + TypeScript estrito (`noImplicitAny`, sem `any`, sem `@ts-ignore`)
- Three.js (capa/fecho: partículas + malha lenta; slide 3: sólidos PBR, sombras,
  anel-toro emissivo, pacotes de luz, OrbitControls, rótulos HTML sempre no topo)
  com fallback SVG 2D via `window.h3fallback()`
- Motion (transição entre slides com profundidade, fragmentos com spring + stagger)
- Fontes locais OFL: Space Grotesk (display) + Inter (texto), via `@fontsource`

Sem CDN, sem fonte/imagem/biblioteca por rede. Build com `base: './'`: abre por
duplo clique em `../dist/apresentacao-pcc/index.html`, offline.

## Comando único: construir e verificar

```powershell
npm run build
```

Depois abrir `../dist/apresentacao-pcc/index.html` com `?v=<aleatório>` para forçar
recarga em `file://`. O `dist/apresentacao-pcc.html` antigo segue intacto.

## Verificação (Chrome, 1920×1080)

```powershell
chrome-devtools-axi open file:///C:/Users/Desenvolvimento/Desktop/harness-bench/dist/apresentacao-pcc/index.html?v=1
chrome-devtools-axi resize 1920 1080
chrome-devtools-axi eval "document.querySelectorAll('.slide').length"
chrome-devtools-axi console
chrome-devtools-axi perf-start
# percorrer os 17 slides com a seta, interagir no slide 3, tecla N nas notas
chrome-devtools-axi perf-stop
```

Contrato preservado: setas, Home/End, F, O, N, ?, 0–5 no slide 3D, hash `#n` na URL,
barra de progresso, `hooks.enter/leave/step`, índice por `id` via `S('s-...')`,
`window.h3fallback()`, notas com os `[n]` do dump do `.docx`.

## Notas de performance

Sem `UnrealBloomPass`: o brilho vem de emissivo + sprites aditivos, para manter
60 fps em GPU integrada. `pixelRatio` limitado a 1.5, `rAF` só no slide ativo,
neblina e sombras 1024px. Medir com `perf-start`/`perf-stop` nos slides com 3D.
