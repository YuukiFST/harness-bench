---
title: Oh My Pi
type: entity
summary: Fork direto do Pi; 11,4x bytes na 1a requisicao, polo modificado de H2
tags: [oh-my-pi, fork, h2, bracos]
created: 2026-09-10
updated: 2026-09-10
sources: [wiki/sources/frontierharness-runta-2026.md]
---

# Oh My Pi

*Fork* direto do [[pi-coding-agent]], versao 17.2.10 na Camada 1. Com a linhagem fixa, envia **11,4x os bytes** do ascendente na primeira requisicao da mesma tarefa (64.945 vs 5.676): 13,5x schemas, 10,2x system, 2,75x n. schemas, 13,6x tokens. Reenvia historico com +625 bytes/passo mas no 5o passo ja troca o resultado mais antigo por referencia de 54 bytes **sem pressao de contexto** (risco: source: [[lost-in-the-middle-liu-2023]]).

## Evidencia externa

FrontierHarness (source: [[frontierharness-runta-2026]]): oh-my-pi 56,7%/$4,75 vs Pi 60,0%/$2,43 — mesmo protocolo, modelo Kimi K3 fixo.

## No PCC

Polo modificado de H2: se pi e oh-my-pi nao diferirem em [[succ-mtok]], H2 e refutada (achado reportavel; carga maior nao implica pior — pode recuperar em menos passos). Sem adaptador no executor — escrito neste projeto. Auditoria do diff via [[harness-handbook-wang-2026]] (BGPD).

## Contradictions

Nenhuma registrada.
