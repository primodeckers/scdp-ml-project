# -*- coding: utf-8 -*-
"""
Exporta RELATORIO_FINAL_Atividade2_ML.md para rene_estevam_deckers_atividade_2.docx
(formatação próxima ao template: Times New Roman 12 pt, justificado, espaçamento 1,5).

Requer: pip install python-docx
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.shared import Cm, Pt

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / "RELATORIO_FINAL_Atividade2_ML.md"
OUT_PATH = ROOT / "rene_estevam_deckers_atividade_2.docx"


def set_run_font(run, size_pt: int = 12) -> None:
    run.font.name = "Times New Roman"
    run.font.size = Pt(size_pt)
    try:
        from docx.oxml.ns import qn

        r = run._element
        rPr = r.get_or_add_rPr()
        rFonts = rPr.get_or_add_rFonts()
        rFonts.set(qn("w:eastAsia"), "Times New Roman")
        rFonts.set(qn("w:cs"), "Times New Roman")
    except Exception:
        pass


def format_paragraph_body(p) -> None:
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        set_run_font(run, 12)


def preprocess_links(text: str) -> str:
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)


def add_inline_runs(paragraph, text: str, size_pt: int = 12) -> None:
    text = preprocess_links(text)
    parts = re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            r = paragraph.add_run(part[2:-2])
            r.bold = True
            set_run_font(r, size_pt)
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            r = paragraph.add_run(part[1:-1])
            r.font.name = "Courier New"
            r.font.size = Pt(size_pt - 1)
        else:
            r = paragraph.add_run(part)
            set_run_font(r, size_pt)


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.count("|") >= 2


def is_table_sep(line: str) -> bool:
    s = line.strip().replace(" ", "")
    return bool(re.match(r"^\|?[-:|]+\|?$", s))


def parse_table(lines: list[str], start: int) -> tuple[list[list[str]], int]:
    rows: list[list[str]] = []
    i = start
    while i < len(lines) and is_table_row(lines[i]):
        row = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if is_table_sep(lines[i]):
            i += 1
            continue
        rows.append(row)
        i += 1
    return rows, i


def export() -> None:
    if not MD_PATH.is_file():
        print("Arquivo não encontrado:", MD_PATH, file=sys.stderr)
        sys.exit(1)

    raw_lines = MD_PATH.read_text(encoding="utf-8").splitlines()
    lines = [ln.rstrip() for ln in raw_lines]

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)

    i = 0
    md_dir = MD_PATH.parent

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            i += 1
            continue

        if stripped.startswith("*[") and "Inserir figura" in stripped:
            i += 1
            continue

        if stripped.startswith("![") and "](" in stripped:
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
            if m:
                rel = m.group(2).strip()
                img_path = (md_dir / rel).resolve()
                if img_path.is_file():
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run = p.add_run()
                    run.add_picture(str(img_path), width=Cm(15))
                    p.paragraph_format.space_after = Pt(6)
                else:
                    p = doc.add_paragraph()
                    add_inline_runs(p, f"[Imagem não encontrada: {rel}]", 12)
                    format_paragraph_body(p)
            i += 1
            continue

        if stripped.startswith("# "):
            t = stripped[2:].strip()
            p = doc.add_heading(t, level=1)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            for run in p.runs:
                set_run_font(run, 14)
            i += 1
            continue

        if stripped.startswith("## "):
            t = stripped[3:].strip()
            p = doc.add_heading(t, level=2)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            for run in p.runs:
                set_run_font(run, 13)
            i += 1
            continue

        if stripped.startswith("### "):
            t = stripped[4:].strip()
            p = doc.add_heading(t, level=3)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            for run in p.runs:
                set_run_font(run, 12)
            i += 1
            continue

        if stripped.startswith("> "):
            inner = stripped[2:].strip()
            p = doc.add_paragraph()
            add_inline_runs(p, inner, 12)
            format_paragraph_body(p)
            p.paragraph_format.left_indent = Cm(0.8)
            i += 1
            continue

        if stripped.startswith("- ") or (
            stripped.startswith("* ") and len(stripped) > 2
        ):
            p = doc.add_paragraph(style="List Bullet")
            add_inline_runs(p, stripped[2:].strip(), 12)
            format_paragraph_body(p)
            i += 1
            continue

        if len(stripped) >= 2 and stripped.startswith("*") and stripped.endswith("*"):
            inner = stripped[1:-1]
            if inner and not inner.startswith("*"):
                p = doc.add_paragraph()
                r = p.add_run(inner)
                r.italic = True
                set_run_font(r, 12)
                format_paragraph_body(p)
                i += 1
                continue

        if is_table_row(line):
            table_rows, new_i = parse_table(lines, i)
            if not table_rows:
                i = new_i
                continue
            cols = len(table_rows[0])
            table = doc.add_table(rows=len(table_rows), cols=cols)
            table.style = "Table Grid"
            for ri, row_cells in enumerate(table_rows):
                for ci, cell_text in enumerate(row_cells):
                    if ci < len(table.rows[ri].cells):
                        cell = table.rows[ri].cells[ci]
                        cell.text = cell_text
                        for para in cell.paragraphs:
                            format_paragraph_body(para)
            doc.add_paragraph()
            i = new_i
            continue

        p = doc.add_paragraph()
        add_inline_runs(p, stripped, 12)
        format_paragraph_body(p)
        i += 1

    doc.save(OUT_PATH)
    print("Gerado:", OUT_PATH)


if __name__ == "__main__":
    export()
