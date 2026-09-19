"""Régénère tous les livrables à partir des .md et des ressources :
    python build/build_all.py
Prérequis : pandoc, Microsoft Word et PowerPoint (export PDF via COM),
pip install python-pptx python-docx openpyxl matplotlib pywin32."""
import os
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # generate_plan importe generate_docx
os.chdir(HERE.parent)
for step in ("generate_charts", "generate_checklist", "generate_docx", "generate_pptx", "generate_plan"):
    print(f"\n== {step} ==")
    try:
        runpy.run_path(str(HERE / f"{step}.py"), run_name="__main__")
    except SystemExit as e:
        if e.code:
            sys.exit(e.code)
