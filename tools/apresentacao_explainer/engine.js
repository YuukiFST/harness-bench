// Motor de leitura do deck (padrão SlideEngine do visual-explainer, inline, sem asset externo).
// Desde 2026-09-23: palco fixo 1920×1080 escalado por inteiro (frontend-slides, AGENTS.md "Slides");
// um slide ativo por vez via .active/.visible, sem scroll. Navegação: barra de progresso, trilho
// lateral, atalhos, sumário (O), ajuda (?), notas (N), tema (T), tela cheia (F), #slide-N,
// roda do mouse, toque e retomada por localStorage.
var STAGE_W = 1920, STAGE_H = 1080;

function SlideEngine() {
  this.stage = document.getElementById('deckStage');
  this.slides = [].slice.call(this.stage.querySelectorAll('.slide'));
  this.current = -1;
  this.total = this.slides.length;
  this.storeKey = ['harness-bench:apresentacao-explainer', location.pathname, document.title, this.total].join(':');
  this.fitStage();
  this.buildChrome();
  this.bindEvents();
  this.show(this.initialIndex());
}
SlideEngine.prototype.fitStage = function () {
  var stage = this.stage;
  function fit() {
    var k = Math.min(window.innerWidth / STAGE_W, window.innerHeight / STAGE_H);
    var x = (window.innerWidth - STAGE_W * k) / 2, y = (window.innerHeight - STAGE_H * k) / 2;
    stage.style.transform = 'translate(' + x + 'px,' + y + 'px) scale(' + k + ')';
  }
  fit();
  window.addEventListener('resize', fit);
};
SlideEngine.prototype.titleOf = function (i) {
  var s = this.slides[i];
  var explicit = s.getAttribute('data-title');
  if (explicit) return explicit;
  var el = s.querySelector('.slide__display,.slide__heading,blockquote');
  var title = el ? el.textContent.trim().replace(/\s+/g, ' ') : 'Slide ' + (i + 1);
  return title.length > 58 ? title.slice(0, 56) + '…' : title;
};
SlideEngine.prototype.buildChrome = function () {
  var self = this;
  var bar = document.createElement('div'); bar.className = 'deck-progress'; document.body.appendChild(bar); this.bar = bar;
  var dots = document.createElement('nav'); dots.className = 'deck-dots'; dots.setAttribute('aria-label', 'Navegação entre slides');
  this.slides.forEach(function (_, i) {
    var title = self.titleOf(i);
    var d = document.createElement('button'); d.type = 'button'; d.className = 'deck-dot'; d.title = title;
    d.setAttribute('aria-label', 'Ir ao slide ' + (i + 1) + ': ' + title);
    var label = document.createElement('span'); label.className = 'deck-dot-label'; label.textContent = (i + 1) + ' · ' + title; d.appendChild(label);
    d.onclick = function () { self.show(i); }; dots.appendChild(d);
  });
  document.body.appendChild(dots); this.dots = [].slice.call(dots.children);
  var arrows = document.createElement('div'); arrows.className = 'deck-arrows';
  var prev = document.createElement('button'); prev.type = 'button'; prev.textContent = '←'; prev.setAttribute('aria-label', 'Slide anterior'); prev.onclick = function () { self.prev(); };
  var next = document.createElement('button'); next.type = 'button'; next.textContent = '→'; next.setAttribute('aria-label', 'Próximo slide'); next.onclick = function () { self.next(); };
  arrows.appendChild(prev); arrows.appendChild(next); document.body.appendChild(arrows);
  var hints = document.createElement('div'); hints.className = 'deck-hints'; hints.textContent = '← → navegam · N notas · O sumário · T tema · ? ajuda'; document.body.appendChild(hints); this.hints = hints;
  this.hintTimer = setTimeout(function () { hints.classList.add('faded'); }, 6000);
  var theme = document.createElement('button'); theme.type = 'button'; theme.className = 'deck-theme'; theme.textContent = 'T'; theme.setAttribute('aria-label', 'Alternar tema claro/escuro'); theme.onclick = function () { self.toggleTheme(); }; document.body.appendChild(theme);
  var notes = document.createElement('aside'); notes.className = 'deck-notes'; notes.setAttribute('aria-label', 'Notas do apresentador'); document.body.appendChild(notes); this.notes = notes;
  var overlay = document.createElement('div'); overlay.className = 'deck-overlay'; overlay.setAttribute('aria-hidden', 'true');
  var panel = document.createElement('div'); panel.className = 'deck-panel'; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-modal', 'true'); panel.setAttribute('aria-label', 'Painel do deck'); panel.tabIndex = -1;
  overlay.appendChild(panel); document.body.appendChild(overlay); this.overlay = overlay; this.panel = panel;
  overlay.addEventListener('click', function (e) { if (e.target === overlay) self.closeOverlay(); });
};
SlideEngine.prototype.toggleTheme = function () {
  var root = document.documentElement;
  var dark = root.classList.contains('theme-dark') || (!root.classList.contains('theme-light') && window.matchMedia('(prefers-color-scheme: dark)').matches);
  root.classList.toggle('theme-dark', !dark);
  root.classList.toggle('theme-light', dark);
};
SlideEngine.prototype.clearPanel = function () { while (this.panel.firstChild) this.panel.removeChild(this.panel.firstChild); };
SlideEngine.prototype.addPanelHeader = function (text) { var h = document.createElement('div'); h.className = 'deck-panel__header'; h.textContent = text; this.panel.appendChild(h); };
SlideEngine.prototype.renderOutline = function () {
  var self = this; this.clearPanel(); this.addPanelHeader('Sumário');
  this.slides.forEach(function (_, i) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'deck-panel__button';
    if (i === self.current) b.setAttribute('aria-current', 'true');
    var n = document.createElement('span'); n.className = 'deck-panel__number'; n.textContent = String(i + 1);
    var t = document.createElement('span'); t.textContent = self.titleOf(i);
    b.appendChild(n); b.appendChild(t); b.onclick = function () { self.show(i); self.closeOverlay(); }; self.panel.appendChild(b);
  });
};
SlideEngine.prototype.renderHelp = function () {
  var rows = [['→ / ↓ / Espaço / PgDn', 'próximo'], ['← / ↑ / PgUp', 'anterior'], ['Home / End', 'primeiro / último'], ['N', 'notas do apresentador'], ['O', 'sumário'], ['T', 'tema claro / escuro'], ['F', 'tela cheia'], ['?', 'ajuda'], ['Esc', 'fechar']];
  this.clearPanel(); this.addPanelHeader('Atalhos');
  rows.forEach(function (row) {
    var item = document.createElement('div'); item.className = 'deck-help-row';
    var label = document.createElement('span'); label.textContent = row[1];
    var key = document.createElement('kbd'); key.textContent = row[0];
    item.appendChild(label); item.appendChild(key); this.panel.appendChild(item);
  }, this);
};
SlideEngine.prototype.openOverlay = function (mode) {
  this.lastFocus = document.activeElement; this.overlay.classList.add('open'); this.overlay.setAttribute('aria-hidden', 'false');
  mode === 'help' ? this.renderHelp() : this.renderOutline(); this.panel.focus(); this.fadeHints();
};
SlideEngine.prototype.closeOverlay = function () {
  this.overlay.classList.remove('open'); this.overlay.setAttribute('aria-hidden', 'true');
  if (this.lastFocus && typeof this.lastFocus.focus === 'function') this.lastFocus.focus();
};
SlideEngine.prototype.overlayOpen = function () { return this.overlay.classList.contains('open'); };
SlideEngine.prototype.toggleNotes = function () { this.notes.classList.toggle('open'); this.renderNotes(); };
SlideEngine.prototype.renderNotes = function () {
  if (!this.notes.classList.contains('open')) return;
  var src = this.slides[this.current].querySelector('.notes');
  while (this.notes.firstChild) this.notes.removeChild(this.notes.firstChild);
  if (src) { this.notes.appendChild(src.cloneNode(true)); this.notes.firstChild.style.display = 'block'; }
  else { this.notes.textContent = 'Sem notas neste slide.'; }
};
SlideEngine.prototype.bindEvents = function () {
  var self = this;
  document.addEventListener('keydown', function (e) {
    if (e.target.closest('input,textarea,[contenteditable]')) return;
    // Atalhos do navegador (Ctrl+F, Ctrl+T, Cmd+N) passam direto.
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.key === 'Escape' && self.overlayOpen()) { e.preventDefault(); self.closeOverlay(); return; }
    if (e.key === 'o' || e.key === 'O') { e.preventDefault(); self.overlayOpen() ? self.closeOverlay() : self.openOverlay('outline'); return; }
    if (e.key === '?') { e.preventDefault(); self.overlayOpen() ? self.closeOverlay() : self.openOverlay('help'); return; }
    if (e.key === 'n' || e.key === 'N') { e.preventDefault(); self.toggleNotes(); return; }
    if (e.key === 't' || e.key === 'T') { e.preventDefault(); self.toggleTheme(); return; }
    if (e.key === 'f' || e.key === 'F') { e.preventDefault(); document.fullscreenElement ? document.exitFullscreen().catch(function () {}) : document.documentElement.requestFullscreen().catch(function () {}); return; }
    if (self.overlayOpen()) return;
    if (['ArrowDown', 'ArrowRight', ' ', 'PageDown'].indexOf(e.key) > -1) { e.preventDefault(); self.next(); }
    else if (['ArrowUp', 'ArrowLeft', 'PageUp'].indexOf(e.key) > -1) { e.preventDefault(); self.prev(); }
    else if (e.key === 'Home') { e.preventDefault(); self.show(0); }
    else if (e.key === 'End') { e.preventDefault(); self.show(self.total - 1); }
    self.fadeHints();
  });
  window.addEventListener('hashchange', function () { var i = self.fromHash(); if (i !== null && i !== self.current) self.show(i); });
  // Roda: um passo por gesto; o intervalo evita que a inércia do trackpad pule vários slides.
  var wheelLock = 0;
  window.addEventListener('wheel', function (e) {
    if (self.overlayOpen() || e.target.closest('.deck-notes,.deck-dots')) return;
    var now = Date.now(); if (now < wheelLock || Math.abs(e.deltaY) < 12) return;
    wheelLock = now + 650; e.deltaY > 0 ? self.next() : self.prev();
  }, { passive: true });
  var tX, tY;
  window.addEventListener('touchstart', function (e) { tX = e.touches[0].clientX; tY = e.touches[0].clientY; }, { passive: true });
  window.addEventListener('touchend', function (e) {
    // Mesma exclusão da roda: rolar notas ou lista não troca de slide.
    if (self.overlayOpen() || e.target.closest('.deck-notes,.deck-dots')) return;
    var dx = tX - e.changedTouches[0].clientX, dy = tY - e.changedTouches[0].clientY;
    var d = Math.abs(dx) > Math.abs(dy) ? dx : dy;
    if (Math.abs(d) > 50) { d > 0 ? self.next() : self.prev(); }
  });
};
SlideEngine.prototype.fromHash = function () { var m = /^#(?:slide-)?(\d+)$/.exec(location.hash); if (!m) return null; var i = (+m[1]) - 1; return i >= 0 && i < this.total ? i : null; };
SlideEngine.prototype.initialIndex = function () {
  var i = this.fromHash();
  if (i !== null) return i;
  try { var saved = parseInt(localStorage.getItem(this.storeKey), 10); if (saved > 0 && saved < this.total) return saved; } catch (e) { }
  return 0;
};
SlideEngine.prototype.show = function (i) {
  i = Math.max(0, Math.min(i, this.total - 1));
  if (i === this.current) return;
  this.slides.forEach(function (s, j) { s.classList.toggle('active', j === i); s.classList.toggle('visible', j === i); s.setAttribute('aria-hidden', j === i ? 'false' : 'true'); });
  this.current = i;
  this.update();
};
SlideEngine.prototype.next = function () { this.show(this.current + 1); };
SlideEngine.prototype.prev = function () { this.show(this.current - 1); };
SlideEngine.prototype.update = function () {
  var c = this.current;
  this.bar.style.width = ((c + 1) / this.total * 100) + '%';
  this.dots.forEach(function (d, i) { i === c ? d.setAttribute('aria-current', 'true') : d.removeAttribute('aria-current'); });
  this.renderNotes();
  try { history.replaceState(null, '', '#slide-' + (c + 1)); localStorage.setItem(this.storeKey, String(c)); } catch (e) { }
};
SlideEngine.prototype.fadeHints = function () { clearTimeout(this.hintTimer); this.hints.classList.add('faded'); };

// Verificação de entrega: mede em px do palco 1920×1080 (divide pela escala atual; slides ocultos
// mantêm layout, pois usam visibility).
// Falha quando um bloco estoura o próprio slide, um cartão corta texto, ou dois blocos irmãos se sobrepõem.
function checkSlideOverflow() {
  var failures = [];
  document.querySelectorAll('.slide').forEach(function (slide, index) {
    var problems = [];
    var box = slide.getBoundingClientRect();
    var k = box.width / STAGE_W;
    slide.querySelectorAll('.slide__head,.slide__mid > *,.slide__source,.card,.pipeline__step,.refs,.gantt,.ledger,blockquote').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if ((box.bottom - r.bottom) / k < 20 || (box.right - r.right) / k < 20) problems.push('fora do slide: ' + el.className);
      if (el.scrollHeight - el.clientHeight > 1 && getComputedStyle(el).overflowY !== 'visible') problems.push('corte: ' + el.className);
    });
    var blocks = [].slice.call(slide.querySelectorAll('.slide__mid > *, .cards > .card'));
    blocks.forEach(function (a, i) {
      blocks.slice(i + 1).forEach(function (b) {
        if (a.contains(b) || b.contains(a) || a.parentNode !== b.parentNode) return;
        var p = a.getBoundingClientRect(), q = b.getBoundingClientRect();
        if (p.left < q.right - 1 && q.left < p.right - 1 && p.top < q.bottom - 1 && q.top < p.bottom - 1) problems.push('sobreposição');
      });
    });
    if (problems.length) {
      slide.setAttribute('data-slide-check', 'overflow');
      slide.setAttribute('data-slide-check-label', 'ESTOURO — ' + problems[0]);
      failures.push('Slide ' + (index + 1) + ': ' + problems.join('; '));
    } else {
      slide.removeAttribute('data-slide-check');
      slide.removeAttribute('data-slide-check-label');
    }
  });
  if (failures.length) console.error('Verificação de entrega falhou. ' + failures.join(' | '));
  else console.info('Verificação de entrega: nenhum slide estoura o palco.');
  return failures;
}
window.checkSlideOverflow = checkSlideOverflow;

window.deckEngine = new SlideEngine();
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.fonts.ready.then(function () { requestAnimationFrame(checkSlideOverflow); });
}
