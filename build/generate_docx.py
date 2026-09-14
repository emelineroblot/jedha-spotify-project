"""Convertit les .md en .docx (pandoc), puis met en forme via Word (COM) :
polices, marges, bordures de tableaux, pied de page numéroté, export PDF,
et vérifie le nombre de pages attendu par l'énoncé."""
import subprocess
import sys
import time
from pathlib import Path

import ctypes
import ctypes.wintypes as wt

import pythoncom
import win32com.client as win32

user32 = ctypes.windll.user32


def dismiss_dialogs(pid: int, seconds: float = 4.0):
    """Ferme les boîtes de dialogue modales de Word (ex. « Word n'est pas le programme
    par défaut… ») qui bloquent les appels COM avec RPC_E_CALL_REJECTED."""
    deadline = time.time() + seconds
    while time.time() < deadline:
        found = []

        @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
        def cb(h, _):
            p = wt.DWORD()
            user32.GetWindowThreadProcessId(h, ctypes.byref(p))
            cls = ctypes.create_unicode_buffer(64)
            user32.GetClassNameW(h, cls, 64)
            if p.value == pid and cls.value == "#32770" and user32.IsWindowVisible(h):
                found.append(h)
            return True

        user32.EnumWindows(cb, 0)
        for h in found:
            user32.PostMessageW(h, 0x0010, 0, 0)  # WM_CLOSE
        time.sleep(0.5)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "livrables"
OUT.mkdir(exist_ok=True)

# (source md, nom de sortie, pages max attendues)
DOCS = [
    ("etape1-data-maturity-assessment.md", "01-data-maturity-assessment", 2),
    ("etape2-framework-gouvernance.md", "02-data-governance-policy", 3),
    ("etape3-plan-implementation.md", "03-implementation-plan", 3),
]

FOOTER = "Spotify — Data Governance · Emeline ROBLOT · Septembre 2026 · Page "

# constantes Word
wdAlignParagraphRight = 2
wdFieldPage = 33
wdFieldNumPages = 26
wdStatisticPages = 2
wdExportFormatPDF = 17


def cm(x: float) -> float:
    return x * 28.35


def pandoc(src: Path, dst: Path):
    subprocess.run(
        ["pandoc", str(src), "-o", str(dst), "--resource-path", str(ROOT),
         "--from", "markdown+yaml_metadata_block"],
        check=True, cwd=ROOT,
    )


def polish(word, pid: int, path: Path, max_pages: int) -> int:
    doc = word.Documents.Open(str(path))
    dismiss_dialogs(pid)
    try:
        # mise en page
        for sec in doc.Sections:
            ps = sec.PageSetup
            ps.TopMargin = ps.BottomMargin = cm(1.8)
            ps.LeftMargin = ps.RightMargin = cm(2.0)
        # polices et interlignes
        normal = doc.Styles("Normal")
        normal.Font.Name = "Calibri"
        normal.Font.Size = 10
        normal.ParagraphFormat.SpaceAfter = 4
        normal.ParagraphFormat.SpaceBefore = 0
        normal.ParagraphFormat.LineSpacingRule = 0  # single
        for name, size, color in (("Title", 20, 0x54B91D), ("Subtitle", 12, 0x8A8A8A),
                                  ("Heading 1", 13, 0x54B91D), ("Heading 2", 11, 0x141419)):
            try:
                st = doc.Styles(name)
                st.Font.Name = "Calibri"
                st.Font.Size = size
                st.Font.Bold = True
                st.Font.Color = color  # BGR
                st.ParagraphFormat.SpaceBefore = 8 if name.startswith("Heading") else 0
                st.ParagraphFormat.SpaceAfter = 3
            except Exception:
                pass
        for name in ("Author", "Date"):
            try:
                st = doc.Styles(name)
                st.Font.Size = 10
                st.Font.Color = 0x8A8A8A
                st.ParagraphFormat.SpaceAfter = 2
            except Exception:
                pass
        # tableaux : police réduite, bordures fines, largeur page
        for t in doc.Tables:
            t.Range.Font.Size = 8
            t.Range.ParagraphFormat.SpaceAfter = 1
            t.Range.ParagraphFormat.SpaceBefore = 1
            t.Borders.Enable = True
            t.Borders.InsideLineWidth = 2  # wdLineWidth025pt
            t.Borders.OutsideLineWidth = 2
            t.Rows(1).Range.Font.Bold = True
            t.Rows(1).Shading.BackgroundPatternColor = 0xEFEFEF
            # largeurs de colonnes : fixées par les tirets des séparateurs markdown (pandoc)
        # blockquote (hypothèses) : encadré discret
        try:
            bq = doc.Styles("Block Text")
            bq.Font.Size = 9
            bq.Font.Italic = False
            bq.ParagraphFormat.LeftIndent = 8
            bq.ParagraphFormat.Shading.BackgroundPatternColor = 0xF5F5F5
        except Exception:
            pass
        # images : centrées (largeur fixée dans le markdown via {width=...})
        for shp in doc.InlineShapes:
            shp.Range.ParagraphFormat.Alignment = 1  # wdAlignParagraphCenter
            shp.Range.ParagraphFormat.SpaceAfter = 2
        # pied de page numéroté
        footer = doc.Sections(1).Footers(1)  # wdHeaderFooterPrimary
        rng = footer.Range
        rng.Text = FOOTER
        rng.Font.Size = 8
        rng.Font.Color = 0x8A8A8A
        rng.ParagraphFormat.Alignment = wdAlignParagraphRight
        rng.Collapse(0)  # wdCollapseEnd
        doc.Fields.Add(rng, wdFieldPage)
        rng = footer.Range
        rng.Collapse(0)
        rng.InsertAfter(" / ")
        rng.Collapse(0)
        doc.Fields.Add(rng, wdFieldNumPages)
        doc.Fields.Update()
        doc.Repaginate()
        pages = doc.ComputeStatistics(wdStatisticPages)
        doc.Save()
        dismiss_dialogs(pid, 1)
        doc.ExportAsFixedFormat(str(path.with_suffix(".pdf")), wdExportFormatPDF)
    finally:
        doc.Close(False)
        dismiss_dialogs(pid, 1)
    return pages


def _word_pid() -> int:
    out = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process WINWORD).Id"],
                         capture_output=True, text=True).stdout.split()
    pids = [int(x) for x in out if x.isdigit()]
    return max(pids)  # le dernier lancé


def main():
    pythoncom.CoInitialize()
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    pid = _word_pid()
    ok = True
    try:
        for src, name, max_pages in DOCS:
            dst = OUT / f"{name}.docx"
            # Word rejette parfois un appel quand il est occupé : on réessaie
            for attempt in range(3):
                pandoc(ROOT / src, dst)
                try:
                    pages = polish(word, pid, dst, max_pages)
                    break
                except pythoncom.com_error as e:
                    if attempt == 2:
                        raise
                    print(f"  retry {attempt + 1} ({e.args[1]})")
                    time.sleep(3)
            flag = "OK" if pages <= max_pages else "TROP LONG"
            if pages > max_pages:
                ok = False
            print(f"{dst.name}: {pages} page(s) (max {max_pages}) -> {flag}")
    finally:
        word.Quit()
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
