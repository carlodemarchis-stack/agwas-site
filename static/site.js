/* The hero sentence: two pickers, a line of copy that follows them, and a ten-second rotation
   that cross-fades between pairings until a visitor touches either picker. */
(function () {
  var data = JSON.parse(document.getElementById('picker-data').textContent);
  var A = data.who, B = data.what, TOUR = data.tour;
  var who = document.getElementById('who'), what = document.getElementById('what');
  var whoTxt = document.getElementById('whoTxt'), whatTxt = document.getElementById('whatTxt');
  var answer = document.getElementById('answer');
  if (!who || !what) return;

  function paint() {
    whoTxt.textContent = who.value; whatTxt.textContent = what.value;
    answer.innerHTML = '<b>' + A[who.value] + '</b> On ' + B[what.value] + '.';
  }
  function measure(el, txt) {
    var m = el.parentNode.querySelector('.measure');
    if (!m) { m = document.createElement('span'); m.className = 'measure'; el.parentNode.appendChild(m); }
    m.textContent = txt; return m.getBoundingClientRect().width;
  }
  /* old word ghosts out while the new one comes in; the box eases between the two measured widths */
  function swap(el, txt) {
    var oldTxt = el.textContent; if (oldTxt === txt) return;
    var w0 = measure(el, oldTxt), w1 = measure(el, txt);
    var ghost = document.createElement('span'); ghost.className = 'ghost'; ghost.textContent = oldTxt;
    el.parentNode.insertBefore(ghost, el);
    el.style.transition = 'none'; el.style.width = w0 + 'px'; el.style.opacity = 0; el.textContent = txt;
    void el.offsetWidth; el.style.transition = '';
    requestAnimationFrame(function () { el.style.width = w1 + 'px'; el.style.opacity = 1; ghost.style.opacity = 0; });
    setTimeout(function () { ghost.remove(); el.style.width = ''; }, 650);
  }
  var busy = false;
  function fadeTo(fn) {
    if (busy) return; busy = true; setTimeout(function () { busy = false; }, 720);
    fn();
    swap(whoTxt, who.value); swap(whatTxt, what.value);
    answer.classList.add('fade');
    setTimeout(function () { answer.innerHTML = '<b>' + A[who.value] + '</b> On ' + B[what.value] + '.'; answer.classList.remove('fade'); }, 300);
  }
  var step = 0, timer = null;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function tick() { step = (step + 1) % TOUR.length; fadeTo(function () { who.value = TOUR[step][0]; what.value = TOUR[step][1]; }); }
  function start() { if (reduce || timer) return; timer = setInterval(tick, 10000); }
  function stop() { clearInterval(timer); timer = null; }
  who.onchange = what.onchange = function () { stop(); paint(); };
  ['pointerdown', 'focusin', 'touchstart'].forEach(function (ev) {
    document.querySelector('.sentence').addEventListener(ev, stop, { passive: true });
  });
  document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
  paint(); start();
})();

/* a link to something inside a closed fold opens the fold first */
document.addEventListener('click', function (e) {
  var a = e.target.closest('a[href^="#"]'); if (!a) return;
  var el = document.getElementById(a.getAttribute('href').slice(1)); if (!el) return;
  var d = el.closest('details'); if (d && !d.open) d.open = true;
});

/* the note band: rotate through the day's notes, pause while hovered or focused */
(function () {
  var band = document.querySelector('.noteband'); if (!band) return;
  var items = band.querySelectorAll('.nb-item'); if (items.length < 2) return;
  var idx = band.querySelector('#nbIdx'), i = 0, timer = null;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(n) {
    items[i].classList.remove('on'); i = (n + items.length) % items.length; items[i].classList.add('on');
    if (idx) idx.textContent = i + 1;
  }
  function start() { if (reduce || timer) return; timer = setInterval(function () { show(i + 1); }, 8000); }
  function stop() { clearInterval(timer); timer = null; }
  band.addEventListener('mouseenter', stop); band.addEventListener('mouseleave', start);
  band.addEventListener('focusin', stop); band.addEventListener('focusout', start);
  band.addEventListener('touchstart', stop, { passive: true });
  document.addEventListener('visibilitychange', function () { document.hidden ? stop() : start(); });
  start();
})();
