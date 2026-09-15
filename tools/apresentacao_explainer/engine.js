// Motor de leitura do deck (padrão SlideEngine do visual-explainer, inline, sem asset externo).
// Só navegação: barra de progresso, trilho lateral, contador, atalhos, sumário (O), ajuda (?),
// notas do apresentador (N), tema (T), #slide-N e retomada por localStorage.
function SlideEngine() {
  this.deck = document.querySelector('.deck');
  this.slides = [].slice.call(document.querySelectorAll('.slide'));
  this.current = 0;
  this.total = this.slides.length;
  this.storeKey = ['harness-bench:apresentacao-explainer', location.pathname, document.title, this.total].join(':');
  this.buildChrome();
  this.bindEvents();
  this.observe();
  this.restore();
  this.update();
}
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
    d.onclick = function () { self.goTo(i); }; dots.appendChild(d);
  });
  document.body.appendChild(dots); this.dots = [].slice.call(dots.children);
  var arrows = document.createElement('div'); arrows.className = 'deck-arrows';
  var prev = document.createElement('button'); prev.type = 'button'; prev.textContent = '←'; prev.setAttribute('aria-label', 'Slide anterior'); prev.onclick = function () { self.prev(); };
  var next = document.createElement('button'); next.type = 'button'; next.textContent = '→'; next.setAttribute('aria-label', 'Próximo slide'); next.onclick = function () { self.next(); };
  arrows.appendChild(prev); arrows.appendChild(next); document.body.appendChild(arrows);
  var ctr = document.createElement('div'); ctr.className = 'deck-counter'; ctr.setAttribute('aria-live', 'polite'); document.body.appendChild(ctr); this.counter = ctr;
  var hints = document.createElement('div'); hints.className = 'deck-hints'; hints.textContent = '← → navegam · N notas · O sumário · ? ajuda'; document.body.appendChild(hints); this.hints = hints;
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
    b.appendChild(n); b.appendChild(t); b.onclick = function () { self.goTo(i); self.closeOverlay(); }; self.panel.appendChild(b);
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
    if (e.target.closest('.table-wrap,input,textarea,[contenteditable]')) return;
    if (e.key === 'Escape' && self.overlayOpen()) { e.preventDefault(); self.closeOverlay(); return; }
    if (e.key === 'o' || e.key === 'O') { e.preventDefault(); self.overlayOpen() ? self.closeOverlay() : self.openOverlay('outline'); return; }
    if (e.key === '?') { e.preventDefault(); self.overlayOpen() ? self.closeOverlay() : self.openOverlay('help'); return; }
    if (e.key === 'n' || e.key === 'N') { e.preventDefault(); self.toggleNotes(); return; }
    if (e.key === 't' || e.key === 'T') { e.preventDefault(); self.toggleTheme(); return; }
    if (e.key === 'f' || e.key === 'F') { e.preventDefault(); document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); return; }
    if (self.overlayOpen()) return;
    if (['ArrowDown', 'ArrowRight', ' ', 'PageDown'].indexOf(e.key) > -1) { e.preventDefault(); self.next(); }
    else if (['ArrowUp', 'ArrowLeft', 'PageUp'].indexOf(e.key) > -1) { e.preventDefault(); self.prev(); }
    else if (e.key === 'Home') { e.preventDefault(); self.goTo(0); }
    else if (e.key === 'End') { e.preventDefault(); self.goTo(self.total - 1); }
    self.fadeHints();
  });
  window.addEventListener('hashchange', function () { var i = self.fromHash(); if (i !== null && i !== self.current) self.goTo(i); });
  var tY;
  this.deck.addEventListener('touchstart', function (e) { tY = e.touches[0].clientY; }, { passive: true });
  this.deck.addEventListener('touchend', function (e) { var dy = tY - e.changedTouches[0].clientY; if (Math.abs(dy) > 50) { dy > 0 ? self.next() : self.prev(); } });
};
SlideEngine.prototype.fromHash = function () { var m = /^#(?:slide-)?(\d+)$/.exec(location.hash); if (!m) return null; var i = (+m[1]) - 1; return i >= 0 && i < this.total ? i : null; };
SlideEngine.prototype.restore = function () {
  var i = this.fromHash();
  if (i === null) { try { var saved = localStorage.getItem(this.storeKey); if (saved !== null) { var j = parseInt(saved, 10); if (j > 0 && j < this.total) i = j; } } catch (e) { } }
  if (i !== null && i > 0) { var self = this; this.current = i; setTimeout(function () { self.slides[i].scrollIntoView({ block: 'start' }); }, 60); }
};
SlideEngine.prototype.observe = function () {
  var self = this;
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) { if (entry.isIntersecting) { entry.target.classList.add('visible'); self.current = self.slides.indexOf(entry.target); self.update(); } });
  }, { threshold: 0.5 });
  this.slides.forEach(function (s) { obs.observe(s); });
};
SlideEngine.prototype.goTo = function (i) { i = Math.max(0, Math.min(i, this.total - 1)); this.slides[i].scrollIntoView({ behavior: 'smooth' }); };
SlideEngine.prototype.next = function () { if (this.current < this.total - 1) this.goTo(this.current + 1); };
SlideEngine.prototype.prev = function () { if (this.current > 0) this.goTo(this.current - 1); };
SlideEngine.prototype.update = function () {
  var c = this.current, pct = Math.round((c + 1) / this.total * 100);
  this.bar.style.width = pct + '%';
  this.dots.forEach(function (d, i) { i === c ? d.setAttribute('aria-current', 'true') : d.removeAttribute('aria-current'); });
  this.counter.textContent = (c + 1) + ' / ' + this.total + ' · ' + pct + '%';
  this.renderNotes();
  try { history.replaceState(null, '', '#slide-' + (c + 1)); localStorage.setItem(this.storeKey, String(c)); } catch (e) { }
};
SlideEngine.prototype.fadeHints = function () { clearTimeout(this.hintTimer); this.hints.classList.add('faded'); };

// Verificação de entrega: com prefers-reduced-motion, marca todo slide cujo conteúdo estoura 100dvh.
function checkSlideOverflow() {
  var failures = [];
  document.querySelectorAll('.slide').forEach(function (slide, index) {
    var excess = Math.ceil(slide.scrollHeight - slide.clientHeight);
    if (excess > 1) {
      slide.setAttribute('data-slide-check', 'overflow');
      slide.setAttribute('data-slide-check-label', 'ESTOURO — dividir ou reduzir (' + excess + 'px)');
      failures.push('Slide ' + (index + 1) + ': estouro vertical ' + excess + 'px');
    } else {
      slide.removeAttribute('data-slide-check');
      slide.removeAttribute('data-slide-check-label');
    }
  });
  if (failures.length) console.error('Verificação de entrega falhou. ' + failures.join(' | '));
  else console.info('Verificação de entrega: nenhum slide estoura a tela.');
  return failures;
}
window.checkSlideOverflow = checkSlideOverflow;

new SlideEngine();
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  requestAnimationFrame(checkSlideOverflow);
}
