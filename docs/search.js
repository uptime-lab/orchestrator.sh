/* Search over /docs/search.json: every word of the query must match a word
   prefix in the page title, the section heading or its text. No dependencies,
   no network beyond this site. */
(function () {
  "use strict";
  var input = document.getElementById("docs-search");
  var list = document.getElementById("docs-results");
  if (!input || !list) return;
  var index = null, active = -1;

  function load() {
    if (index) return Promise.resolve(index);
    return fetch("/docs/search.json").then(function (r) { return r.json(); }).then(function (data) {
      index = data.map(function (e) {
        return { e: e, title: (e.p + " " + e.h).toLowerCase(), text: e.t.toLowerCase() };
      });
      return index;
    });
  }
  function words(s) { return s.toLowerCase().split(/[^a-z0-9_.\/-]+/).filter(Boolean); }
  function has(hay, w) { return (" " + hay).indexOf(" " + w) !== -1 || hay.indexOf(w) !== -1 && w.length > 3; }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function snippet(text, w) {
    var at = text.toLowerCase().indexOf(w);
    if (at < 0) at = 0;
    var from = Math.max(0, at - 50), to = Math.min(text.length, at + 110);
    return (from ? "…" : "") + esc(text.slice(from, to)) + (to < text.length ? "…" : "");
  }
  function search(q) {
    var ws = words(q);
    if (!ws.length) return [];
    var hits = [];
    index.forEach(function (it) {
      var score = 0;
      for (var i = 0; i < ws.length; i++) {
        if (has(it.title, ws[i])) score += 5;
        else if (has(it.text, ws[i])) score += 1;
        else return;
      }
      hits.push({ it: it, score: score });
    });
    hits.sort(function (a, b) { return b.score - a.score; });
    return hits.slice(0, 8).map(function (h) { return { e: h.it.e, w: ws[0] }; });
  }
  function show(results, q) {
    active = -1;
    if (!q.trim()) { list.hidden = true; list.innerHTML = ""; return; }
    list.innerHTML = results.length ? results.map(function (r) {
      return '<li><a href="' + r.e.u + '"><b>' + esc(r.e.p) + (r.e.h ? " › " + esc(r.e.h) : "") + "</b><span>" + snippet(r.e.t, r.w) + "</span></a></li>";
    }).join("") : '<li class="none">Nothing found.</li>';
    list.hidden = false;
  }
  function move(d) {
    var links = list.querySelectorAll("a");
    if (!links.length) return;
    active = (active + d + links.length) % links.length;
    for (var i = 0; i < links.length; i++) links[i].classList.toggle("on", i === active);
    links[active].scrollIntoView({ block: "nearest" });
  }
  input.addEventListener("input", function () {
    var q = input.value;
    load().then(function () { if (input.value === q) show(search(q), q); });
  });
  input.addEventListener("focus", load);
  input.addEventListener("keydown", function (ev) {
    if (ev.key === "ArrowDown") { ev.preventDefault(); move(1); }
    else if (ev.key === "ArrowUp") { ev.preventDefault(); move(-1); }
    else if (ev.key === "Enter") { var a = list.querySelector("a.on") || list.querySelector("a"); if (a) location.href = a.getAttribute("href"); }
    else if (ev.key === "Escape") { input.value = ""; show([], ""); input.blur(); }
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) { ev.preventDefault(); input.focus(); }
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".search")) list.hidden = true; });
})();
