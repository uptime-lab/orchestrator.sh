#!/usr/bin/env python3
"""Build /docs/ from docs-src/*.md. No dependencies beyond the standard library.

    python3 tools/build_docs.py          # write docs/
    python3 tools/build_docs.py --check  # fail on a missing image or a broken internal link

A page is docs-src/<order>-<slug>.md with a front matter block:

    ---
    title: Adding a device
    summary: One sentence shown on the index and under the title.
    section: Devices
    ---

The Markdown subset: ## and ### headings, paragraphs, - and 1. lists (one
level), fenced code, tables, > blockquotes (a callout; start it with
**Note:**, **Warning:** or **Tip:**), images on their own line as
![alt text](img/<slug>/<file>.jpg "caption") (a file ending in .mp4 becomes
a looping silent clip), and inline `code`, **bold**,
*emphasis*, [links](url). Link to another page as [text](../<slug>/).
Images live in docs/img/<slug>/ and are referenced relative to docs/.
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs-src")
OUT = os.path.join(ROOT, "docs")
SEARCH = '<div class="search" role="search"><input type="search" id="docs-search" placeholder="Search the docs" aria-label="Search the documentation" autocomplete="off" spellcheck="false"><kbd>/</kbd><ol id="docs-results" hidden></ol></div>'
SECTION_ORDER = ["Start", "Devices", "Operating a fleet", "Automation", "Administration"]

problems = []


def inline(text):
    out, pos = [], 0
    token = re.compile(r"`([^`]+)`|\*\*([^*]+)\*\*|\*([^*]+)\*|\[([^\]]+)\]\(([^)\s]+)\)")
    for m in token.finditer(text):
        out.append(html.escape(text[pos:m.start()], quote=False))
        if m.group(1) is not None:
            out.append("<code>%s</code>" % html.escape(m.group(1), quote=False))
        elif m.group(2) is not None:
            out.append("<b>%s</b>" % inline(m.group(2)))
        elif m.group(3) is not None:
            out.append("<em>%s</em>" % inline(m.group(3)))
        else:
            out.append('<a href="%s">%s</a>' % (html.escape(m.group(5)), inline(m.group(4))))
        pos = m.end()
    out.append(html.escape(text[pos:], quote=False))
    return "".join(out)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


IMAGE = re.compile(r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)\s*$')


def plain(text):
    """Markdown inline text reduced to words, for the search index."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*>|#]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def sections(md):
    """(anchor, heading, text) per ## section; the text before the first heading has an empty anchor."""
    out, anchor, heading, buf, fence = [], "", "", [], False
    for line in md.split("\n"):
        if line.startswith("```"):
            fence = not fence
            continue
        if not fence and line.startswith("## "):
            out.append((anchor, heading, plain(" ".join(buf))))
            heading = line[3:].strip()
            anchor, buf = slugify(heading), []
        elif not (line.startswith("|") and set(line) <= set("|-: ")):
            buf.append(line[4:] if line.startswith("### ") else line)
    out.append((anchor, heading, plain(" ".join(buf))))
    return [x for x in out if x[1] or x[2]]


def render(md, page):
    lines = md.split("\n")
    out, toc, i = [], [], 0

    def para(buf):
        if buf:
            out.append("<p>%s</p>" % inline(" ".join(s.strip() for s in buf)))

    buf = []
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            para(buf); buf = []
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(code), quote=False))
        elif line.startswith("## ") or line.startswith("### "):
            para(buf); buf = []
            level = 2 if line.startswith("## ") else 3
            text = line[level + 1:].strip()
            anchor = slugify(text)
            if level == 2:
                toc.append((anchor, text))
            out.append('<h%d id="%s">%s</h%d>' % (level, anchor, inline(text), level))
        elif IMAGE.match(line):
            para(buf); buf = []
            alt, src, caption = IMAGE.match(line).groups()
            if not alt.strip():
                problems.append("%s: image %s has no alt text" % (page, src))
            if not os.path.isfile(os.path.join(OUT, src)):
                problems.append("%s: missing image %s" % (page, src))
            if src.endswith(".mp4"):
                # A screen clip: loads and plays when scrolled into view (search.js), loops, no sound.
                fig = '<figure><video data-src="../%s" aria-label="%s" muted loop playsinline preload="none"></video>' % (
                    html.escape(src), html.escape(alt))
            else:
                fig = '<figure><a href="../%s"><img src="../%s" alt="%s" loading="lazy"></a>' % (
                    html.escape(src), html.escape(src), html.escape(alt))
            if caption:
                fig += "<figcaption>%s</figcaption>" % inline(caption)
            out.append(fig + "</figure>")
        elif line.startswith("> "):
            para(buf); buf = []
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i][1:].strip()); i += 1
            i -= 1
            text = " ".join(quote)
            kind = "note"
            m = re.match(r"\*\*(Note|Warning|Tip):\*\*\s*", text)
            if m:
                kind = m.group(1).lower()
            out.append('<aside class="callout %s"><p>%s</p></aside>' % (kind, inline(text)))
        elif re.match(r"^(- |\d+\. )", line):
            para(buf); buf = []
            ordered = not line.startswith("- ")
            items = []
            while i < len(lines) and (re.match(r"^(- |\d+\. )", lines[i]) or (lines[i].startswith("  ") and items)):
                if re.match(r"^(- |\d+\. )", lines[i]):
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i]).strip())
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            i -= 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
        elif line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
            para(buf); buf = []
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            head = cells(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(cells(lines[i])); i += 1
            i -= 1
            table = "<table><thead><tr>%s</tr></thead><tbody>" % "".join("<th>%s</th>" % inline(c) for c in head)
            for r in rows:
                table += "<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r)
            out.append('<div class="table">%s</tbody></table></div>' % table)
        elif not line.strip():
            para(buf); buf = []
        else:
            buf.append(line)
        i += 1
    para(buf)
    return "\n".join(out), toc


def load():
    pages = []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".md"):
            continue
        raw = open(os.path.join(SRC, name), encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            problems.append("%s: no front matter" % name); continue
        meta = dict((k.strip(), v.strip()) for k, v in (l.split(":", 1) for l in m.group(1).split("\n") if ":" in l))
        slug = re.sub(r"^\d+-", "", name[:-3])
        for key in ("title", "summary", "section"):
            if not meta.get(key):
                problems.append("%s: front matter lacks %s" % (name, key))
        if meta.get("section") not in SECTION_ORDER:
            problems.append("%s: unknown section %r" % (name, meta.get("section")))
        pages.append({"slug": slug, "meta": meta, "body": m.group(2), "name": name})
    key = lambda p: (SECTION_ORDER.index(p["meta"]["section"]) if p["meta"].get("section") in SECTION_ORDER else 99, p["name"])
    return sorted(pages, key=key)


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Uptime Orchestrator docs</title>
<meta name="description" content="{summary}">
<link href="/fonts/fonts.css" rel="stylesheet">
<link href="/docs/docs.css" rel="stylesheet">
<script src="/docs/search.js" defer></script>
</head>
<body>

<header class="nav">
  <div class="wrap">
    <a class="mark" href="/">Uptime <span>Orchestrator</span> <small>for Raspberry Pi fleets</small></a>
    <nav aria-label="Site">
      <a href="/#four-minutes">How it works</a>
      <a href="/#install">Install</a>
      <a href="/docs/" aria-current="page">Docs</a>
      <a href="/subscription/">Pricing</a>
    </nav>
    <span class="proto">Public beta</span>
  </div>
</header>
"""

FOOT = """
<footer>
  <div class="wrap">
    <span>Uptime Orchestrator is made by Uptime Lab, the people behind the Compute Blade. Raspberry Pi is a trademark of Raspberry Pi Ltd.</span>
    <span><a href="https://github.com/uptime-lab/orchestrator">Source</a> · <a href="/docs/">Docs</a> · <a href="/subscription/">Subscriptions</a> · <a href="/imprint/">Imprint</a> · <a href="/privacy/">Privacy</a></span>
  </div>
</footer>

</body>
</html>
"""


def sidebar(pages, current):
    out, section = ['<nav class="side" aria-label="Documentation">', SEARCH], None
    for p in pages:
        if p["meta"]["section"] != section:
            if section is not None:
                out.append("</ul>")
            section = p["meta"]["section"]
            out.append("<h4>%s</h4><ul>" % html.escape(section))
        cur = ' aria-current="page"' if p["slug"] == current else ""
        out.append('<li><a href="/docs/%s/"%s>%s</a></li>' % (p["slug"], cur, html.escape(p["meta"]["title"])))
    out.append("</ul></nav>")
    return "\n".join(out)


def main():
    check = "--check" in sys.argv
    pages = load()
    slugs = set(p["slug"] for p in pages)
    anchors = dict((p["slug"], set(slugify(h) for h in re.findall(r"^#{2,3} (.+)$", p["body"], re.M))) for p in pages)
    written = {}
    for n, p in enumerate(pages):
        body, toc = render(p["body"], p["name"])
        for target, anchor in re.findall(r'href="\.\./([a-z0-9-]+)/(?:#([a-z0-9-]*))?"', body):
            if target not in slugs:
                problems.append("%s: link to unknown page ../%s/" % (p["name"], target))
            elif anchor and anchor not in anchors[target]:
                problems.append("%s: link to ../%s/#%s, a heading that page does not have" % (p["name"], target, anchor))
        meta = p["meta"]
        doc = HEAD.format(title=html.escape(meta["title"]), summary=html.escape(meta["summary"], quote=True))
        doc += '\n<main class="docs wrap">\n' + sidebar(pages, p["slug"])
        doc += '\n<article>\n<div class="stamp"><b>%s</b> Documentation</div>\n<h1>%s</h1>\n<p class="summary">%s</p>\n' % (
            html.escape(meta["section"]), html.escape(meta["title"]), inline(meta["summary"]))
        if len(toc) > 2:
            doc += '<nav class="toc" aria-label="On this page"><ul>%s</ul></nav>\n' % "".join(
                '<li><a href="#%s">%s</a></li>' % (a, inline(t)) for a, t in toc)
        doc += body + '\n<div class="pager">'
        if n > 0:
            doc += '<a class="prev" href="/docs/%s/"><small>Previous</small>%s</a>' % (pages[n - 1]["slug"], html.escape(pages[n - 1]["meta"]["title"]))
        if n + 1 < len(pages):
            doc += '<a class="next" href="/docs/%s/"><small>Next</small>%s</a>' % (pages[n + 1]["slug"], html.escape(pages[n + 1]["meta"]["title"]))
        doc += "</div>\n</article>\n</main>\n" + FOOT
        written[os.path.join(OUT, p["slug"], "index.html")] = doc

    index = HEAD.format(title="Documentation", summary="How to install Uptime Orchestrator, add devices and run a fleet.")
    index += '\n<main class="docs-index wrap">\n<div class="stamp"><b>Docs</b> Uptime Orchestrator 0.1</div>\n<h1>Documentation</h1>\n'
    index += SEARCH + "\n"
    index += '<p class="summary">From an empty server to a managed fleet. The reference pages for self-hosting live with the source, in <a href="https://github.com/uptime-lab/orchestrator/tree/main/docs">the repository</a>.</p>\n'
    section = None
    for p in pages:
        if p["meta"]["section"] != section:
            if section is not None:
                index += "</div>\n"
            section = p["meta"]["section"]
            index += '<h2>%s</h2>\n<div class="cards">\n' % html.escape(section)
        index += '<a class="card" href="/docs/%s/"><h3>%s</h3><p>%s</p></a>\n' % (
            p["slug"], html.escape(p["meta"]["title"]), inline(p["meta"]["summary"]))
    if section is not None:
        index += "</div>\n"
    index += "</main>\n" + FOOT
    written[os.path.join(OUT, "index.html")] = index

    entries = []
    for p in pages:
        for anchor, heading, text in sections(p["body"]):
            entries.append({"u": "/docs/%s/%s" % (p["slug"], "#" + anchor if anchor else ""),
                            "p": p["meta"]["title"], "h": heading,
                            "t": (p["meta"]["summary"] + " " + text) if not anchor else text})
    written[os.path.join(OUT, "search.json")] = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))

    if problems:
        print("\n".join(problems), file=sys.stderr)
    if check:
        sys.exit(1 if problems else 0)
    for path, doc in written.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(doc)
    print("%d pages written, %d search entries, %d problems" % (len(written) - 1, len(entries), len(problems)))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
