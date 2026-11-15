// 共通アニメーション部品（時間 t 秒を渡すと、その瞬間の絵を描く）
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, a, b) => clamp((t - a) / (b - a));
const eOut = x => 1 - Math.pow(1 - x, 3);
const eOutExpo = x => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x));
const eInOut = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const eOutBack = x => { const c = 1.9, c3 = c + 1; return 1 + c3 * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const $ = id => document.getElementById(id);

// 登場アニメ：from の位置・大きさ・回転・ぼかしから定位置へ
function enter(id, t, t0, o = {}) {
  const el = typeof id === 'string' ? $(id) : id;
  const dur = o.dur ?? 0.4, ease = o.ease ?? eOutExpo;
  const p = ease(prog(t, t0, t0 + dur));
  const op = prog(t, t0, t0 + Math.min(dur, o.fade ?? 0.1));
  const fx = o.x ?? 0, fy = o.y ?? 0, fs = o.s ?? 1, fr = o.r ?? 0, fb = o.blur ?? 0;
  const x = (1 - p) * fx, y = (1 - p) * fy, s = fs + (1 - fs) * p, r = (1 - p) * fr + (o.rot ?? 0);
  el.style.opacity = t < t0 ? 0 : op;
  el.style.transform = `translate(${x}px,${y}px) scale(${s}) rotate(${r}deg)`;
  el.style.filter = fb ? `blur(${(1 - p) * fb}px)` : '';
  return p;
}
function shakeXY(t, t0, dur, amp) {
  if (t < t0 || t > t0 + dur) return [0, 0];
  const k = Math.pow(1 - (t - t0) / dur, 2);
  return [Math.sin(t * 173) * amp * k, Math.cos(t * 229) * amp * k];
}
function flash(id, t, t0, dur = 0.25, max = 0.9) {
  const el = $(id);
  el.style.opacity = (t < t0 || t > t0 + dur) ? 0 : max * (1 - (t - t0) / dur);
}
function typewriter(id, text, t, t0, cps = 14) {
  const n = Math.floor(clamp((t - t0) * cps, 0, text.length));
  $(id).textContent = text.slice(0, n);
  return n;
}
function drawLine(el, t, t0, dur) {
  const len = el.getTotalLength();
  el.style.strokeDasharray = len;
  el.style.strokeDashoffset = len * (1 - eInOut(prog(t, t0, t0 + dur)));
}
// シーンの出し分け（data-a 〜 data-b 秒だけ表示）
function scenes(t) {
  let cur = null;
  document.querySelectorAll('section').forEach(s => {
    const on = t >= +s.dataset.a && t < +s.dataset.b;
    s.style.display = on ? 'block' : 'none';
    if (on) cur = s;
  });
  return cur;
}
