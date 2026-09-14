"""Régénère tous les livrables à partir des .md et des ressources :
    python build/build_all.py
Prérequis : pandoc, Microsoft Word et PowerPoint (export PDF via COM),
pip install python-pptx python-docx openpyxl matplotlib pywin32."""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for step in ("generate_charts", "generate_checklist", "generate_docx", "generate_pptx"):
    print(f"\n== {step} ==")
    try:
        runpy.run_path(str(HERE / f"{step}.py"), run_name="__main__")
    except SystemExit as e:
        if e.code:
            sys.exit(e.code)
