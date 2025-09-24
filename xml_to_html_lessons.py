"""
XML → Standalone HTML converter with hierarchical TOC (Lessons → Exercises → ¶n and Page Breaks)

Usage inside Jupyter:
---------------------
from xml_to_html_lessons import convert_xml_to_html
convert_xml_to_html("pharr2025.xml", "pharr2025.html")
"""
from lxml import etree
from html import escape
from pathlib import Path
import re

def text_or_empty(x):
    return x if x is not None else ""

def get_attr(el, name, default=None):
    if name in el.attrib:
        return el.attrib[name]
    if name == "xml:lang":
        return el.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", default)
    return default

def make_anchor_id(el):
    xml_id = get_attr(el, "xml:id")
    if xml_id:
        return xml_id
    n = get_attr(el, "n")
    tag = etree.QName(el).localname
    if n:
        if tag == "pb":
            return f"p.{n}"
        if tag in ("div","p","paragraph","head","l","lg","note","item","row","cell","table","front","body","back","lesson"):
            return f"{tag}-{n}"
        return f"n{n}"
    return None

def render_node(el):
    if isinstance(el, str):
        return escape(el)
    if isinstance(el, etree._ElementUnicodeResult):
        return escape(str(el))
    if isinstance(el, etree._Comment):
        return ""
    tag = etree.QName(el).localname

    children_html = "".join(render_node(child) for child in el)
    leading_text = escape(text_or_empty(el.text))
    tail_text = escape(text_or_empty(el.tail))
    anchor_id = make_anchor_id(el)
    id_attr = f' id="{anchor_id}"' if anchor_id else ""

    if tag in ("p","paragraph"):
        n = get_attr(el,"n")
        n_prefix = f'<b class="item-number">{escape(n)}.</b> ' if n else ""
        return f'<p{id_attr}>{n_prefix}{leading_text}{children_html}</p>{tail_text}'
    if tag == "div":
        cls = get_attr(el,"type") or "section"
        n = get_attr(el,"n")
        ex_prefix = ""
        if (cls in ("exercise","ex")) and n:
            ex_prefix = f'<div class="exercise-label"><b>Exercise {escape(n)}</b></div>'
        return f'<section class="{escape(cls)}"{id_attr}>{ex_prefix}{leading_text}{children_html}</section>{tail_text}'
    if tag == "pb":
        n = get_attr(el,"n") or ""
        return f'<span class="page-break"{id_attr}>[pg. {escape(n)}]</span>{tail_text}'
    # … (same rendering code for other tags as I showed earlier) …
    return f'<span{id_attr}>{leading_text}{children_html}</span>{tail_text}'

def label_from_head(div_el):
    head = div_el.find(".//{*}head")
    if head is not None:
        txt = "".join(head.itertext()).strip()
        if txt:
            return txt
    return None

def anchor_and_label(el, default_prefix=None):
    a = make_anchor_id(el)
    label = label_from_head(el)
    n = get_attr(el, "n")
    if not label:
        if default_prefix and n:
            label = f"{default_prefix} {n}"
        elif n:
            label = n
        else:
            label = a or "(untitled)"
    return (label, a)

def build_hierarchical_toc(content_root):
    lessons = content_root.findall(".//{*}div[@type='lesson']")
    toc = []
    for lesson in lessons:
        l_label, l_anchor = anchor_and_label(lesson, "Lesson")
        exercises = lesson.findall(".//{*}div[@type='exercise']") + lesson.findall(".//{*}div[@type='ex']")
        ex_items = []
        for ex in exercises:
            e_label, e_anchor = anchor_and_label(ex, "Exercise")
            p_items = []
            for p in ex.findall(".//{*}p[@n]"):
                p_anchor = make_anchor_id(p)
                pn = get_attr(p, "n")
                if p_anchor and pn:
                    p_items.append((f"¶ {pn}", p_anchor))
            ex_items.append((e_label, e_anchor, p_items))
        page_items = []
        for pb in lesson.findall(".//{*}pb[@n]"):
            pn = get_attr(pb, "n")
            pb_anchor = make_anchor_id(pb)
            if pb_anchor and pn:
                page_items.append((f"Page {pn}", pb_anchor))
        toc.append((l_label, l_anchor, ex_items, page_items))
    return toc

BASE_STYLES = """/* CSS omitted for brevity (same as before) */"""

def make_toc_html(toc_struct):
    parts = ["<ul class='toc'>"]
    for lesson_label, lesson_anchor, ex_list, page_items in toc_struct:
        parts.append(f"<li class='toc-lesson'><a href='#{escape(lesson_anchor or '')}'>{escape(lesson_label)}</a>")
        if ex_list:
            parts.append("<ul class='children'>")
            for ex_label, ex_anchor, p_items in ex_list:
                parts.append(f"<li class='toc-ex'><a href='#{escape(ex_anchor or '')}'>{escape(ex_label)}</a>")
                if p_items:
                    parts.append("<ul class='children'>")
                    for plabel, panchor in p_items:
                        parts.append(f"<li class='toc-p'><a href='#{escape(panchor)}'>{escape(plabel)}</a></li>")
                    parts.append("</ul>")
                parts.append("</li>")
            parts.append("</ul>")
        if page_items:
            parts.append("<ul class='pages'>")
            for pg_label, pg_anchor in page_items:
                parts.append(f"<li class='toc-pb'><a href='#{escape(pg_anchor)}'>{escape(pg_label)}</a></li>")
            parts.append("</ul>")
        parts.append("</li>")
    parts.append("</ul>")
    return "\n".join(parts)

def convert_xml_to_html(xml_path, out_html_path):
    parser = etree.XMLParser(remove_comments=True, recover=True)
    tree = etree.parse(str(xml_path), parser=parser)
    root = tree.getroot()
    text_el = root.find(".//{*}text")
    content_root = text_el if text_el is not None else root

    toc_struct = build_hierarchical_toc(content_root)
    content_html = render_node(content_root)
    toc_html = make_toc_html(toc_struct)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Converted XML (Lessons TOC)</title>
<style>{BASE_STYLES}</style>
</head>
<body>
<div class="container">
  <aside class="sidebar"><h2>Contents</h2>{toc_html}</aside>
  <main class="main">{content_html}</main>
</div>
</body>
</html>"""
    Path(out_html_path).write_text(full_html, encoding="utf-8")
    return out_html_path
