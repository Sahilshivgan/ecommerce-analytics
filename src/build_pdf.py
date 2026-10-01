"""Step 8 - Build ONE PDF (Project_Guide.pdf) from docs/0*.md (+ figures)."""
import re
from utils import ROOT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Preformatted

ss = getSampleStyleSheet()
S = {"title": ParagraphStyle("t", parent=ss["Title"], fontSize=26, leading=32, textColor=colors.HexColor("#1b4965")),
     "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontSize=18, textColor=colors.HexColor("#1b4965"), spaceAfter=8),
     "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontSize=13, textColor=colors.HexColor("#2a6f97"), spaceBefore=8),
     "h3": ParagraphStyle("h3", parent=ss["Heading3"], fontSize=10.5, spaceBefore=6),
     "p": ParagraphStyle("p", parent=ss["BodyText"], fontSize=9.5, leading=13, spaceAfter=4),
     "q": ParagraphStyle("q", parent=ss["BodyText"], fontSize=9.5, leading=13, spaceBefore=6, textColor=colors.HexColor("#1b4965")),
     "b": ParagraphStyle("b", parent=ss["BodyText"], fontSize=9.5, leading=13, leftIndent=14, bulletIndent=4, spaceAfter=2),
     "code": ParagraphStyle("c", fontName="Courier", fontSize=7.5, leading=9.5, backColor=colors.HexColor("#f1f3f5"), leftIndent=4)}

def inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', t)

story = [Spacer(1, 6 * cm), Paragraph("E-Commerce Sales &amp; Customer Analytics", S["title"]),
         Paragraph("Industry-style data analytics project: complete guide (what, why, when, how, where) + interview Q&amp;A", S["p"]),
         Spacer(1, 1 * cm), Paragraph("Prepared by: Sahil Shivgan", S["p"]),
         Paragraph("Stack: Python, pandas, SQL (SQLite), matplotlib, reportlab", S["p"])]
for f in sorted((ROOT / "docs").glob("0*.md")):
    story.append(PageBreak()); code = []; incode = False
    for line in f.read_text().splitlines():
        if line.startswith("```"):
            if incode: story.append(Preformatted("\n".join(code), S["code"])); code = []
            incode = not incode; continue
        if incode: code.append(line); continue
        if not line.strip(): continue
        im = re.match(r"!\[.*?\]\((.+?)\)", line)
        if im:
            p = ROOT / im.group(1); w, h = ImageReader(str(p)).getSize()
            story.append(Image(str(p), width=15 * cm, height=15 * cm * h / w)); continue
        if line.startswith("# "): story.append(Paragraph(inline(line[2:]), S["h1"]))
        elif line.startswith("## "): story.append(Paragraph(inline(line[3:]), S["h2"]))
        elif line.startswith("### "): story.append(Paragraph(inline(line[4:]), S["h3"]))
        elif line.startswith("- "): story.append(Paragraph(inline(line[2:]), S["b"], bulletText="\u2022"))
        elif line.startswith("**Q"): story.append(Paragraph(inline(line), S["q"]))
        else: story.append(Paragraph(inline(line), S["p"]))

def footer(c, d):
    c.setFont("Helvetica", 8); c.drawCentredString(A4[0] / 2, 1 * cm, f"E-Commerce Analytics Project Guide - page {d.page}")
SimpleDocTemplate(str(ROOT / "Project_Guide.pdf"), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2 * cm, bottomMargin=1.8 * cm, title="E-Commerce Analytics Project Guide",
                  author="Sahil Shivgan").build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF built")
