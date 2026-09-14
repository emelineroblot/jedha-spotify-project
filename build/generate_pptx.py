"""Génère les deux livrables PowerPoint :
  - livrables/04-presentation-executive.pptx (9 slides + annexes Q&A, notes orateur)
  - livrables/02-organigramme-roles.pptx (organigramme + fiches de rôle)
puis exporte les PDF via PowerPoint (COM). Les visuels viennent de assets/ (generate_charts.py).
Contenu source : etape4-presentation-executive.md et etape2-organigramme-roles.md."""
import subprocess
import time
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "livrables"
OUT.mkdir(exist_ok=True)

GREEN = RGBColor(0x1D, 0xB9, 0x54)
DARK_BG = RGBColor(0x12, 0x12, 0x12)
CARD = RGBColor(0x1E, 0x1E, 0x1E)
CARD2 = RGBColor(0x2A, 0x2A, 0x2A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0xB3, 0xB3, 0xB3)
ORANGE = RGBColor(0xE8, 0x87, 0x1E)
BLUE = RGBColor(0x64, 0xB5, 0xF6)
RED = RGBColor(0xFF, 0x4C, 0x4C)
DARK_GREEN = RGBColor(0x0A, 0x52, 0x2E)

W, H = 13.33, 7.5
DATE = "Septembre 2026"
AUTHOR = "Emeline ROBLOT — Data Governance Specialist"


# ── helpers ────────────────────────────────────────────────────────────────

def new_prs():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    return prs


def rect(slide, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE, line=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def bg(slide):
    rect(slide, 0, 0, W, H, DARK_BG)
    rect(slide, 0, 0, W, 0.06, GREEN)


def tb(slide, text, x, y, w, h, size=14, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
       anchor=MSO_ANCHOR.TOP, italic=False):
    t = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = t.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size, r.font.bold, r.font.italic = Pt(size), bold, italic
    r.font.color.rgb = color
    return t


def bullets(slide, items, x, y, w, h, size=12, color=WHITE, gap=3):
    t = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = t.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(gap)
        bold = False
        if isinstance(item, tuple):
            item, bold = item
        r = p.add_run()
        r.text = "•  " + item
        r.font.size, r.font.bold, r.font.color.rgb = Pt(size), bold, color
    return t


def header(slide, title, sub=None):
    tb(slide, title, 0.4, 0.18, 12.5, 0.8, size=28, bold=True, color=GREEN)
    if sub:
        tb(slide, sub, 0.4, 0.88, 12.5, 0.45, size=13, color=GRAY)
    rect(slide, 0.4, 1.32, 12.5, 0.03, GREEN)


def card(slide, x, y, w, h, title=None, color=CARD, bar=GREEN, title_size=14):
    rect(slide, x, y, w, h, color)
    rect(slide, x, y, w, 0.08, bar)
    if title:
        tb(slide, title, x + 0.1, y + 0.12, w - 0.2, 0.45, size=title_size, bold=True, color=bar)


def footer(slide, n, total):
    tb(slide, f"Spotify — Data Governance Framework · {AUTHOR} · {DATE}", 0.4, 7.08, 10, 0.3,
       size=9, color=GRAY)
    tb(slide, f"{n} / {total}", 11.9, 7.08, 1.0, 0.3, size=9, color=GRAY, align=PP_ALIGN.RIGHT)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def table(slide, rows, x, y, w, col_widths, size=10, header_color=GREEN, row_h=0.36):
    nrows, ncols = len(rows), len(rows[0])
    shp = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(w), Inches(row_h * nrows))
    t = shp.table
    for j, cw in enumerate(col_widths):
        t.columns[j].width = Inches(cw)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = DARK_GREEN if i == 0 else (CARD if i % 2 else CARD2)
            c.margin_left = c.margin_right = Inches(0.06)
            c.margin_top = c.margin_bottom = Inches(0.03)
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run()
            r.text = str(val)
            r.font.size = Pt(size)
            r.font.bold = i == 0 or j == 0
            r.font.color.rgb = WHITE if i == 0 else (GREEN if j == 0 else WHITE)
    return shp


# ── organigramme (réutilisé dans les deux decks) ───────────────────────────

def box(slide, x, y, w, h, title, sub=None, color=CARD, border=GREEN, size=11, sub_size=8.5):
    s = rect(slide, x, y, w, h, color, MSO_SHAPE.ROUNDED_RECTANGLE, line=border)
    s.adjustments[0] = 0.12
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = title
    r.font.size, r.font.bold, r.font.color.rgb = Pt(size), True, WHITE
    if sub:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        r2 = p2.add_run()
        r2.text = sub
        r2.font.size, r2.font.color.rgb = Pt(sub_size), GRAY
    return s


def line(slide, x1, y1, x2, y2, color=GRAY, dash=False, width=1.25):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return c


def elbow(slide, x1, y1, x2, y2, color=GRAY):
    """Connecteur en L : descend depuis (x1,y1) jusqu'à mi-hauteur, horizontal, puis descend vers (x2,y2)."""
    ym = (y1 + y2) / 2
    line(slide, x1, y1, x1, ym, color)
    line(slide, x1, ym, x2, ym, color)
    line(slide, x2, ym, x2, y2, color)


def draw_orgchart(slide, x0=0.5, y0=1.5, w=12.3, h=5.4):
    """Organigramme CoE : CEO → CDO / DPO / CTO / Legal ; CoE → 5 stewards ; Committee transverse."""
    bw, bh = 2.3, 0.62          # boîtes niveau 1
    sw, sh = 1.18, 0.6          # boîtes stewards (5 sous le CoE, à gauche de la branche CTO)
    y_ceo, y_l1, y_l2, y_l3, y_com = y0, y0 + 1.0, y0 + 2.0, y0 + 3.05, y0 + 4.15
    cols = [x0 + 0.2, x0 + 3.55, x0 + 6.6, x0 + 9.65]   # x des 4 branches
    cx = lambda x: x + bw / 2

    # CEO
    ceo_x = x0 + w / 2 - bw / 2
    box(slide, ceo_x, y_ceo, bw, bh, "CEO")
    # niveau 1
    l1 = [("CDO", "stratégie data · pilote le CoE"), ("DPO", "indépendant · conformité"),
          ("CTO", "technologie"), ("Legal", "validation juridique")]
    for x, (t, s) in zip(cols, l1):
        box(slide, x, y_l1, bw, bh, t, s, border=GREEN if t in ("CDO", "DPO") else GRAY)
    # bus CEO → niveau 1
    ybus = y_ceo + bh + 0.19
    line(slide, cx(ceo_x), y_ceo + bh, cx(ceo_x), ybus)
    line(slide, cx(cols[0]), ybus, cx(cols[3]), ybus)
    for x in cols:
        line(slide, cx(x), ybus, cx(x), y_l1)
    # niveau 2
    box(slide, cols[0], y_l2, bw, bh, "Data Governance CoE", "4-6 pers. · standards, catalogue, formation, audit")
    box(slide, cols[1], y_l2, bw, bh, "Privacy Team", "2 analystes · droits des personnes", border=GRAY)
    box(slide, cols[2], y_l2, bw, bh, "Head of Engineering", "implémente les contrôles", border=GRAY)
    for x in cols[:3]:
        line(slide, cx(x), y_l1 + bh, cx(x), y_l2)
    # niveau 3 : 5 stewards sous le CoE, Data Engineers sous Head of Eng
    stew = ["User", "Content", "Payments", "Ads", "Marketing"]
    sx0 = x0 + 0.2
    gap = 0.1
    ybus2 = y_l2 + bh + 0.2
    line(slide, cx(cols[0]), y_l2 + bh, cx(cols[0]), ybus2)
    xs = [sx0 + i * (sw + gap) for i in range(5)]
    line(slide, xs[0] + sw / 2, ybus2, xs[-1] + sw / 2, ybus2)
    for x, name in zip(xs, stew):
        line(slide, x + sw / 2, ybus2, x + sw / 2, y_l3)
        box(slide, x, y_l3, sw, sh, f"Steward {name}", "relais BU", size=9, sub_size=7.5)
    box(slide, cols[2], y_l3, bw, sh, "Data Engineers", "pipelines, chiffrement, effacement", border=GRAY)
    line(slide, cx(cols[2]), y_l2 + bh, cx(cols[2]), y_l3)
    # collaboration stewards ↔ engineering (pointillés)
    line(slide, xs[-1] + sw, y_l3 + sh / 2, cols[2], y_l3 + sh / 2, color=GREEN, dash=True)
    # parties prenantes (droite)
    box(slide, cols[3], y_l2, bw, sh + 0.45, "Parties prenantes",
        "Marketing Director · Product Managers · Department Heads · privacy by design", border=GRAY, sub_size=8)
    # committee (bandeau bas)
    box(slide, x0 + 0.2, y_com, w - 0.4, 0.58, "Data Governance Committee — mensuel, présidé par le CDO",
        "CDO · DPO · Head of Engineering · Marketing Director · Legal · 5 Data Stewards · représentant Product — approuve, arbitre, suit les KPIs, Go/No-Go",
        color=DARK_GREEN, border=GREEN, size=11, sub_size=9)
    # légende
    tb(slide, "Gouvernance (définit, audite)", x0 + 0.2, y_com + 0.66, 3, 0.3, size=9, color=GREEN)
    tb(slide, "Data management (implémente) — ligne CTO, séparée", x0 + 3.2, y_com + 0.66, 5, 0.3, size=9, color=GRAY)
    tb(slide, "- - -  collaboration formalisée par le RACI", x0 + 8.4, y_com + 0.66, 4, 0.3, size=9, color=GREEN)


# ── deck principal ─────────────────────────────────────────────────────────

def build_deck():
    prs = new_prs()
    blank = prs.slide_layouts[6]
    TOTAL = 9
    slides = []

    def add():
        s = prs.slides.add_slide(blank)
        bg(s)
        slides.append(s)
        return s

    # 1 — Titre
    s = add()
    tb(s, "Spotify", 0.5, 0.6, 6, 1.0, size=40, bold=True, color=GREEN)
    tb(s, "Data Governance Framework", 0.5, 1.55, 12.3, 1.0, size=36, bold=True)
    tb(s, "Qualité · Conformité · Confiance — à l'échelle mondiale", 0.5, 2.5, 12.3, 0.6, size=18, color=GRAY)
    for i, (val, lbl) in enumerate([("450 M", "utilisateurs actifs"), ("200 M", "abonnés premium"),
                                    ("180+", "pays"), ("3,4 → 4,2", "maturité data /5 (M12)")]):
        cx_ = 0.5 + i * 3.1
        card(s, cx_, 3.4, 2.9, 1.5)
        tb(s, val, cx_, 3.55, 2.9, 0.8, size=30, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
        tb(s, lbl, cx_, 4.3, 2.9, 0.5, size=12, color=GRAY, align=PP_ALIGN.CENTER)
    rect(s, 0.5, 5.2, 12.3, 0.9, DARK_GREEN)
    tb(s, "Un framework fondé sur les 9 principes du Governance Principles Guide · modèle Centre of Excellence · "
          "pilote User Data en 4 mois · 3 décisions à prendre aujourd'hui", 0.65, 5.3, 12.0, 0.7, size=13, color=WHITE,
       anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 0, 6.4, W, 0.8, CARD)
    tb(s, f"Présentation executive — {DATE}  |  {AUTHOR}", 0.5, 6.55, 10, 0.5, size=12, color=GRAY)
    tb(s, "9 slides · 15 min + Q&A", 10, 6.55, 2.9, 0.5, size=12, bold=True, color=GREEN, align=PP_ALIGN.RIGHT)
    notes(s, "Spotify traite les données de 450 millions de personnes dans 180 pays. Ces données alimentent Discover Weekly, "
             "les campagnes marketing, les décisions produit. En 2023, l'autorité suédoise a sanctionné Spotify de 5 millions "
             "d'euros sur un sujet de gouvernance, pas de technologie. Je vous propose un framework pour gouverner ces données "
             "proactivement, avec un pilote en 4 mois et 3 décisions à prendre aujourd'hui.")

    # 2 — Pourquoi maintenant
    s = add()
    header(s, "Pourquoi agir maintenant ?", "3 signaux d'alarme — et un précédent")
    sig = [
        ("Risque réglementaire", RED, [
            "GDPR : jusqu'à 4 % du CA mondial ≈ 530 M€ (CA 2023 : 13,25 Md€)",
            "Notification de violation sous 72 h · CCPA/CPRA · PDPA · LGPD · DSA",
            ("Précédent : IMY, juin 2023 — 58 M SEK (≈ 5 M€) pour un droit d'accès insuffisamment clair", True)]),
        ("Silos qui freinent le business", ORANGE, [
            "Marketing, Product, Engineering, Content gèrent leurs propres datasets",
            "« Utilisateur actif » : définition différente selon les équipes",
            "Parcours découverte → premium impossible à reconstituer"]),
        ("Confiance et éthique", BLUE, [
            "Utilisateurs et régulateurs attendent transparence et contrôle",
            "Recommandations non auditées pour les biais (DSA art. 27)",
            "Concurrence : Apple Music, Amazon Music, YouTube Music"]),
    ]
    for i, (t, c, items) in enumerate(sig):
        y = 1.55 + i * 1.78
        card(s, 0.4, y, 6.6, 1.65, t, bar=c)
        bullets(s, items, 0.5, y + 0.55, 6.4, 1.05, size=11)
    rect(s, 7.2, 1.55, 5.7, 5.3, CARD)
    s.shapes.add_picture(str(ASSETS / "radar-maturite-dark.png"), Inches(7.35), Inches(1.6), height=Inches(4.75))
    tb(s, "Maturité data : 3,4 / 5 — Governance 2 · Compliance 3 · Quality 3", 7.2, 6.4, 5.7, 0.4,
       size=11, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    notes(s, "Le radar montre un paradoxe : architecture et analytics au niveau 5, gouvernance au niveau 2. Spotify a construit "
             "une Formule 1 sans direction de course. Et le précédent de 2023 prouve que le risque est réel : ce n'est pas "
             "l'infrastructure qui a été sanctionnée, c'est la clarté de l'information donnée aux utilisateurs.")

    # 3 — Framework
    s = add()
    header(s, "Le framework : 3 piliers, 9 principes", "Source : Governance Principles Guide — regroupés pour l'action")
    pil = [
        ("Qualité & accessibilité", ["Data Quality", "Accountability", "Continuous Improvement"], [
            "5 domaines (User, Content, Payments, Ads, Marketing), 1 Data Steward chacun",
            "4 critères mesurés : complétude, exactitude, cohérence, fraîcheur",
            "Catalogue unique, accès par classification, données pseudonymisées par défaut"]),
        ("Conformité & sécurité", ["Compliance", "Data Security", "Data Minimization", "User Rights", "Transparency"], [
            "Base légale documentée par finalité (contrat, intérêt légitime, consentement)",
            "7 droits couverts avec SLA, DPIA avant tout traitement à risque",
            "Classification 4 niveaux, chiffrement, SIEM, rétention définie"]),
        ("Culture & éthique", ["Ethical Use", "Continuous Improvement"], [
            "Formation par rôle, > 90 % des employés formés",
            "Audit trimestriel des biais de recommandation, explicabilité",
            "Pas de profilage sur catégories sensibles inférées"]),
    ]
    for i, (t, badges, items) in enumerate(pil):
        x = 0.4 + i * 4.2
        card(s, x, 1.55, 4.05, 4.45, t)
        by = 2.1
        bx = x + 0.15
        for b in badges:
            bw_ = 0.085 * len(b) + 0.3
            if bx + bw_ > x + 3.95:
                bx = x + 0.15
                by += 0.42
            r = rect(s, bx, by, bw_, 0.34, DARK_GREEN, MSO_SHAPE.ROUNDED_RECTANGLE)
            r.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
            run = r.text_frame.paragraphs[0].add_run()
            run.text = b
            run.font.size, run.font.color.rgb = Pt(9), GREEN
            bx += bw_ + 0.1
        bullets(s, items, x + 0.1, by + 0.5, 3.85, 5.9 - by, size=13, gap=10)
    rect(s, 0.4, 6.15, 12.5, 0.7, DARK_GREEN)
    tb(s, "4 objectifs du business case couverts : Qualité · Conformité · Privacy · Accessibilité & intégration  —  "
          "Data Governance Policy v1.0 : 3 pages, 7 sections, RACI, checklist annexée",
       0.55, 6.2, 12.2, 0.6, size=12, anchor=MSO_ANCHOR.MIDDLE)
    notes(s, "Les 9 principes du guide sont regroupés en 3 piliers pour rester lisibles. La politique tient en 3 pages : objet, "
             "principes, qualité, sécurité et accès, conformité, rôles, application.")

    # 4 — Conformité
    s = add()
    header(s, "Conformité réglementaire", "GDPR · CCPA/CPRA · PCI-DSS · réglementations locales et plateformes")
    reg = [
        ("GDPR — Union européenne", ["Base légale par finalité, registre art. 30",
                                     "7 droits couverts, réponse < 1 mois",
                                     "Notification de violation < 72 h",
                                     "DPIA avant tout traitement à risque"]),
        ("CCPA / CPRA — Californie", ["« Do Not Sell or Share » + signal GPC",
                                      "Accès, suppression, correction < 45 j",
                                      "Non-discrimination garantie",
                                      "Opt-out propagé aux partenaires"]),
        ("PCI-DSS — paiements", ["Prestataire certifié, aucun n° de carte stocké",
                                 "SAQ-A annuel, MFA sur consoles",
                                 "Scans trimestriels, pentest annuel",
                                 "Politique de sécurité revue chaque année"]),
        ("Local & plateformes", ["PDPA Singapour · LGPD Brésil (2 % CA local)",
                                 "DSA art. 27 : recommandations explicables + option non profilée",
                                 "AI Act : obligations de transparence",
                                 "Veille DPO + Legal, checklist trimestrielle"]),
    ]
    for i, (t, items) in enumerate(reg):
        x = 0.4 + i * 3.15
        card(s, x, 1.55, 3.0, 4.1, t, title_size=13)
        bullets(s, items, x + 0.08, 2.1, 2.85, 3.5, size=11, gap=6)
    rect(s, 0.4, 5.85, 12.5, 1.0, DARK_GREEN)
    tb(s, "Outils : OneTrust (consentement, registre, DPIA, demandes) · Splunk (SIEM) · Thales/Vormetric (chiffrement)   |   "
          "Compliance Checklist Excel remplie : 14 exigences, statut, owner, échéance (annexe)",
       0.55, 5.9, 12.2, 0.9, size=12, anchor=MSO_ANCHOR.MIDDLE)
    notes(s, "Point d'attention : la recommandation musicale n'est pas « haut risque » au sens de l'AI Act ; l'obligation concrète "
             "vient du DSA, article 27 — expliquer la recommandation et offrir une option non fondée sur le profilage. "
             "C'est déjà dans le framework. La checklist Excel fournie a été remplie ligne par ligne.")

    # 5 — Organisation
    s = add()
    header(s, "Organisation & rôles — Centre of Excellence", "Source : Data Governance Roles Template · la gouvernance définit et audite, l'engineering implémente")
    draw_orgchart(s, 0.5, 1.5, 12.3, 5.4)
    notes(s, "Le CoE est le modèle recommandé par le guide et par le cours : Spotify est trop grand et trop distribué pour un "
             "modèle centralisé, et le modèle embedded, c'est ce qui existe aujourd'hui et qui produit les silos. La couche de "
             "coordination, c'est le Committee mensuel. Le DPO est hors de la ligne du CDO pour garantir son indépendance.")

    # 6 — Plan
    s = add()
    header(s, "Plan d'implémentation", "4 phases · 18 mois · pilote en 4 mois — calendrier aligné sur l'Executive Q&A Guide")
    rect(s, 0.4, 1.5, 12.5, 3.6, CARD)
    pic = s.shapes.add_picture(str(ASSETS / "gantt-plan-dark.png"), Inches(0.5), Inches(1.55), height=Inches(3.5))
    pic.left = int((Inches(W) - pic.width) / 2)
    stack = [("Catalogue", "Collibra ou extension de Lexikon"), ("Qualité", "Great Expectations"),
             ("Conformité", "OneTrust"), ("SIEM", "Splunk"), ("Chiffrement", "Thales / Vormetric"),
             ("Lineage", "OpenLineage"), ("Observabilité", "Monte Carlo (ph. 4)")]
    for i, (k, v) in enumerate(stack):
        x = 0.4 + i * 1.79
        card(s, x, 5.3, 1.72, 1.2, k, title_size=11)
        tb(s, v, x + 0.08, 5.78, 1.6, 0.7, size=10.5, color=GRAY)
    notes(s, "Calendrier aligné sur le Q&A guide : pilote 3 à 6 mois, puis 12 mois de déploiement. Spotify a déjà Lexikon, un "
             "catalogue interne adopté par 95 % des data scientists : la phase 1 audite l'existant avant tout achat. On n'achète "
             "pas un outil pour remplacer ce qui marche, on ajoute la couche stewardship et policy. Un outil par besoin, "
             "choisi sur trois critères : intégration GCP/Airflow, coût, couverture.")

    # 7 — Pilote
    s = add()
    header(s, "Pilote User Data — M3 à M6", "Source : Pilot Implementation Template · périmètre borné, baselines mesurées en semaine 1")
    card(s, 0.4, 1.55, 4.3, 5.3, "Pourquoi User Data ?")
    bullets(s, ["Exposition GDPR maximale — juridiction qui a déjà sanctionné Spotify",
                "Données pouvant révéler des informations sensibles inférées",
                "Alimente Discover Weekly, Daily Mix et la rétention premium",
                ("Périmètre : profils et historiques d'écoute des marchés UE d'abord, extension mondiale en phase 3", True),
                "Équipe : Lead CoE (PM), Steward User, DPO + Privacy Team, Data Engineers, VP Product",
                "Go/No-Go du Committee en M6"], 0.5, 2.1, 4.1, 4.6, size=11.5, gap=8)
    table(s, [["KPI (Pilot Template)", "Cible M6", "Source"],
              ["Data Quality Score", "-10 % de données manquantes (complétude > 98 %)", "Great Expectations"],
              ["Compliance Score", "100 % des traitements avec base légale et consentement valide", "OneTrust"],
              ["Data Access Speed", "-20 % de délai d'accès aux données", "Catalogue"],
              ["Risk Mitigation Score", "100 % des datasets classifiés et chiffrés · 0 incident", "Catalogue, Splunk"],
              ["Droits des personnes", "Effacement < 30 j, 100 % dans les délais légaux", "Privacy Team"]],
          4.9, 1.55, 8.0, [2.2, 4.1, 1.7], size=11, row_h=0.62)
    rect(s, 4.9, 5.4, 8.0, 1.45, DARK_GREEN)
    tb(s, "Livrables : Data Quality Report · Compliance Assessment · Technical Integration Plan · Risk Assessment Report · "
          "Stakeholder Feedback\nRisques : résistance au changement (ateliers dès M1), intégration technique (POC en phase 1), "
          "dérive de périmètre (UE borné)", 5.0, 5.45, 7.8, 1.35, size=11, anchor=MSO_ANCHOR.MIDDLE)
    notes(s, "Toutes les baselines sont mesurées en semaine 1. Un KPI sans baseline n'est pas un KPI. Le périmètre UE permet "
             "d'être réaliste en 4 mois et de traiter d'abord la juridiction qui nous a déjà sanctionnés.")

    # 8 — Impact
    s = add()
    header(s, "Impact business", "≈ 6-7 M€ pour couvrir 530 M€ d'exposition — ordres de grandeur, hypothèses à affiner en phase 1")
    rect(s, 0.4, 1.5, 6.4, 3.9, CARD)
    s.shapes.add_picture(str(ASSETS / "impact-business-dark.png"), Inches(0.5), Inches(1.55), width=Inches(6.2))
    ben = [("Compliance", "Réduction du risque d'amende (jusqu'à 4 % du CA) ; pas de récidive IMY"),
           ("Cost savings", "-20 % de temps d'accès aux données ≈ 25 ETP libérés (hyp. 500 analystes × 2 h/sem.)"),
           ("Trust", "Transparence et contrôle → rétention UE ; différenciation vs Apple, Amazon, YouTube"),
           ("Scalability", "Absorbe la croissance (450 M → 600 M+) et les nouvelles réglementations")]
    for i, (t, d) in enumerate(ben):
        y = 1.5 + i * 0.98
        card(s, 7.0, y, 5.9, 0.9, t, title_size=12)
        tb(s, d, 7.1, y + 0.42, 5.7, 0.45, size=10.5, color=GRAY)
    rect(s, 0.4, 5.55, 12.5, 1.3, DARK_GREEN)
    tb(s, "Coût 18 mois : personnel ≈ 1,9 M€ · licences ≈ 3 M€ · intégration 0,5-1 M€ · formation 0,3 M€. "
          "Phases 1-2 seules ≈ 2,5 M€. Le programme coûte ≈ 1 % de l'exposition maximale et à peine plus que l'amende déjà payée.",
       0.55, 5.6, 12.2, 1.2, size=12.5, anchor=MSO_ANCHOR.MIDDLE)
    notes(s, "Les chiffres de coût sont des ordres de grandeur à affiner en phase 1, je les assume comme hypothèses. Mais l'ordre "
             "de grandeur suffit : le programme coûte environ 1 % de l'exposition maximale, et à peine plus que l'amende déjà payée. "
             "Source CA 2023 : rapport annuel Spotify (13,25 Md€). Source sanction : IMY, juin 2023, confirmée en appel.")

    # 9 — Décisions
    s = add()
    header(s, "3 décisions à prendre aujourd'hui", "Je ne demande pas 18 mois — je demande un CDO, 6 mois de budget et un message au personnel")
    dec = [("1", "Nommer le CDO", "Prérequis bloquant de tout le plan : sans CDO, ni CoE ni stewards.",
            "Action : profil validé et nomination sous 30 jours."),
           ("2", "Approuver le budget phases 1-2", "≈ 2,5 M€ sur 6 mois : CoE + Privacy Team, OneTrust, catalogue pilote, formation.",
            "Action : décision budgétaire ce trimestre."),
           ("3", "Lancer la communication interne", "La résistance au changement est le risque n°1 identifié.",
            "Action : message CEO + webinar CDO en M1.")]
    for i, (n, t, d, a) in enumerate(dec):
        y = 1.6 + i * 1.7
        card(s, 0.4, y, 12.5, 1.55)
        rect(s, 0.4, y, 1.2, 1.55, DARK_GREEN)
        tb(s, n, 0.4, y, 1.2, 1.55, size=40, bold=True, color=GREEN, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, t, 1.8, y + 0.12, 10.9, 0.5, size=18, bold=True)
        tb(s, d, 1.8, y + 0.62, 10.9, 0.45, size=12, color=GRAY)
        tb(s, a, 1.8, y + 1.05, 10.9, 0.45, size=12, bold=True, color=GREEN)
    tb(s, "Le pilote fera la preuve. Résultats présentés au Committee en M6 — Go/No-Go avant toute généralisation.",
       0.4, 6.7, 12.5, 0.35, size=12, color=GRAY, align=PP_ALIGN.CENTER)
    notes(s, "Je ne vous demande pas de valider 18 mois aujourd'hui. Je vous demande un CDO, 6 mois de budget et un message au "
             "personnel. Le pilote fera la preuve.")

    for i, sl in enumerate(slides, 1):
        footer(sl, i, TOTAL)

    # ── Annexes ──
    a = prs.slides.add_slide(blank)
    bg(a)
    tb(a, "Annexes", 0.5, 2.6, 12.3, 1.0, size=40, bold=True, color=GREEN, align=PP_ALIGN.CENTER)
    tb(a, "Q&A anticipé (Executive Q&A Guide) · questions difficiles · références", 0.5, 3.6, 12.3, 0.6, size=16,
       color=GRAY, align=PP_ALIGN.CENTER)

    qa = [
        ("Q1 — Pourquoi maintenant ?", "450 M d'utilisateurs, 180 pays, GDPR/CCPA/DSA, sanction IMY 2023, silos qui freinent l'innovation. Attendre, c'est laisser le risque croître avec l'échelle."),
        ("Q2 — Impact sur les opérations existantes ?", "Le framework s'appuie sur l'existant (GCP, Airflow, Lexikon) : standards, owners et mesures, pas une nouvelle plateforme. Court terme : temps des stewards et formation ; long terme : moins de doublons, conformité fluide."),
        ("Q3 — Valeur business ?", "Compliance (risque jusqu'à 530 M€), cost savings (accès aux données, moins de retraitements), trust (rétention), scalability. Coût ≈ 6-7 M€ sur 18 mois."),
        ("Q4 — Comment garantir la conformité GDPR/CCPA ?", "Base légale documentée par finalité, consentement granulaire, 7 droits avec SLA, Privacy Team, DPO indépendant, DPIA, registre art. 30, checklist tenue à jour."),
        ("Q5 — Pourquoi le CoE ?", "Centralisé = goulot pour 180 pays ; embedded = les silos actuels. Le CoE combine standards communs et relais métier — modèle du guide et du cours pour une entreprise de cette taille."),
        ("Q6 — Comment mesurer le succès ?", "KPIs avec baselines : complétude > 98 %, 100 % des demandes dans les délais, -20 % de délai d'accès, 0 incident critique, catalogue 100 %, > 90 % formés, maturité 3,4 → 4,2."),
        ("Q7 — Combien de temps ?", "Pilote 4 mois (M3-M6), déploiement 12 mois, mode opérationnel à M18. Conforme au guide : pilote 3-6 mois, rollout 12-18 mois."),
        ("Q8 — Quels coûts ?", "Personnel ≈ 1,9 M€, licences ≈ 3 M€, intégration 0,5-1 M€, formation 0,3 M€ → ≈ 6-7 M€ / 18 mois. Phases 1-2 ≈ 2,5 M€. Ordres de grandeur à affiner en phase 1."),
        ("Q9 — Adaptation aux évolutions réglementaires ?", "Veille DPO + Legal, revue annuelle de la politique, checklist trimestrielle, outils multi-juridictions ; DSA et AI Act déjà intégrés."),
        ("Q10 — Sécurité des données sensibles ?", "Classification 4 niveaux, chiffrement, accès nominatif minimal et journalisé, SIEM, PCI-DSS via prestataire certifié + SAQ-A, protocole d'incident 72 h testé chaque année."),
        ("Q11 — Risques principaux ?", "Résistance au changement (ateliers, stewards issus des équipes, quick wins) ; délais (phases bornées, Go/No-Go) ; coûts (budget par phase, licences négociées après audit de l'existant)."),
        ("Q12 — Impact sur l'agilité ?", "Positif : données trouvables et fiables = décisions plus rapides ; privacy by design dès les sprints = moins d'audits correctifs."),
    ]
    for k in range(0, 12, 4):
        s = prs.slides.add_slide(blank)
        bg(s)
        header(s, f"Annexe — Q&A anticipé ({k // 4 + 1}/3)", "Executive Q&A Guide — 12 questions officielles")
        for i, (q, r) in enumerate(qa[k:k + 4]):
            y = 1.55 + i * 1.32
            card(s, 0.4, y, 12.5, 1.2, q, title_size=12)
            tb(s, r, 0.5, y + 0.45, 12.3, 0.72, size=11, color=GRAY)

    hard = [
        ("Spotify a déjà un DPO et une plateforme data de pointe : pourquoi Governance 2/5 ?",
         "Le niveau 2 mesure la gouvernance transverse, pas la technologie : pas de CDO, pas d'ownership par domaine, définitions divergentes, sanction 2023 sur la clarté de l'information. L'architecture est à 5 : c'est le paradoxe."),
        ("Pourquoi pas un data mesh, vu la culture squads ?",
         "Compatible : les stewards par domaine sont les domain owners du mesh, le CoE fournit plateforme et standards fédérés. Le CoE est le nom du cours pour la couche de gouvernance fédérée."),
        ("5 stewards pour 180 pays, suffisant ?",
         "5 stewards par domaine de données, pas par pays. Les spécificités locales (PDPA, LGPD) sont portées par le DPO et Legal ; relais régionaux en phase 3."),
        ("Base légale de la recommandation : consentement ou intérêt légitime ?",
         "Contrat ou intérêt légitime pour la personnalisation du service, avec option non profilée (DSA art. 27) ; consentement pour la publicité ciblée et le partage à des tiers."),
        ("Que faites-vous des données inférées sensibles ?",
         "Interdiction de profiler sur des catégories art. 9 inférées (humeur, religion, orientation), classe « Sensible » avec DPIA, audit des biais trimestriel."),
        ("Et si le pilote échoue ?",
         "≈ 2,5 M€ engagés. Même en No-Go, on garde un catalogue User Data, une baseline qualité, un pipeline de droits testé et une équipe formée : le plan est ajusté, pas perdu."),
    ]
    s = prs.slides.add_slide(blank)
    bg(s)
    header(s, "Annexe — questions difficiles", "Hors guide — préparées pour la soutenance")
    for i, (q, r) in enumerate(hard):
        x = 0.4 + (i % 2) * 6.3
        y = 1.55 + (i // 2) * 1.78
        card(s, x, y, 6.2, 1.65, q, title_size=11)
        tb(s, r, x + 0.1, y + 0.6, 6.0, 1.0, size=10.5, color=GRAY)

    s = prs.slides.add_slide(blank)
    bg(s)
    header(s, "Annexe — références", "Sources publiques utilisées (vérifiées en septembre 2026)")
    bullets(s, [
        "IMY (autorité suédoise), juin 2023 : amende administrative de 58 M SEK contre Spotify AB pour manquement au droit d'accès (art. 15 GDPR) ; confirmée par la cour administrative d'appel — imy.se / noyb.eu",
        "Spotify, rapport annuel 2023 (Form 20-F) : chiffre d'affaires 13,247 Md€ → 4 % ≈ 530 M€",
        "Spotify Engineering, février 2020 : « How We Improved Data Discovery for Data Scientists at Spotify » — catalogue interne Lexikon, migration GCP/BigQuery depuis 2016",
        "Business case Jedha : 450 M d'utilisateurs actifs, 200 M d'abonnés premium, 180+ pays (2023)",
        "Ressources Jedha : Governance Principles Guide, Data Maturity Assessment Template, Roles Template, Organizational Models Overview, Tech Tools Overview, Pilot Implementation Template, Executive Q&A Guide, Compliance Checklist",
        "Hypothèses (à valider en phase 1) : DPO en place, prestataire de paiement certifié PCI-DSS, part de métadonnées incomplètes, coûts du programme, gains d'efficacité",
    ], 0.5, 1.6, 12.3, 5.2, size=13, gap=10)

    path = OUT / "04-presentation-executive.pptx"
    prs.save(path)
    return path


# ── deck organigramme ──────────────────────────────────────────────────────

def build_orgchart():
    prs = new_prs()
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    bg(s)
    header(s, "Organisation & rôles — Spotify Data Governance", "Modèle Centre of Excellence · la gouvernance définit et audite, l'engineering implémente")
    draw_orgchart(s, 0.5, 1.5, 12.3, 5.4)
    footer(s, 1, 2)
    notes(s, "Deux lignes hiérarchiques distinctes : gouvernance (CDO, CoE, stewards) et data management (CTO, Head of Engineering, "
             "Data Engineers), conformément au cours. Le DPO est hors de la ligne du CDO (indépendance, GDPR art. 38). "
             "Le Committee mensuel est la couche de coordination du CoE.")

    s = prs.slides.add_slide(blank)
    bg(s)
    header(s, "Fiches de rôle", "Source : Data Governance Roles Template — responsabilité principale et tâches clés")
    table(s, [["Rôle", "Rattachement", "Responsabilité principale", "Tâches clés"],
              ["Chief Data Officer", "CEO", "Diriger la stratégie et la gouvernance des données",
               "Politiques ; arbitrage inter-domaines ; pilotage du CoE et du Committee ; alignement business ; reporting au comité exécutif"],
              ["Data Protection Officer", "CEO (indépendant)", "Garantir la conformité GDPR, CCPA et réglementations locales",
               "Registre des traitements ; DPIA ; contact des autorités ; incidents et notification 72 h ; Privacy Team ; veille avec Legal"],
              ["Data Governance Committee", "Présidé par le CDO", "Guider le framework et assurer l'alignement transverse",
               "Approuver politiques et standards ; sujets inter-départements ; suivi des KPIs ; Go/No-Go des phases"],
              ["Data Steward (×5)", "CoE + business unit", "Superviser les pratiques data de son domaine",
               "Qualité, classification, rétention ; accès ; catalogue ; application de la politique ; reporting mensuel"],
              ["Head of Engineering", "CTO", "Implémenter les contrôles techniques",
               "Pipelines, chiffrement, SIEM, pipeline d'effacement, scalabilité"],
              ["Legal · Marketing Dir. · Product Managers", "Parties prenantes", "Conformité de leurs périmètres",
               "Validation juridique ; conformité des campagnes ; privacy by design et DPIA sur chaque feature"],
              ["Privacy Team", "DPO", "Traiter les demandes des personnes",
               "2 analystes ; SLA 1 mois GDPR, 45 j CCPA ; journal des demandes"]],
          0.4, 1.5, 12.5, [2.6, 1.9, 3.2, 4.8], size=10.5, row_h=0.6)
    tb(s, "Data Governance Committee — mensuel, 60 min : KPIs qualité par domaine · incidents et demandes des personnes · nouveaux traitements / DPIA · avancement du plan · audits de biais · décisions",
       0.4, 6.45, 12.5, 0.55, size=10.5, color=GRAY)
    footer(s, 2, 2)
    path = OUT / "02-organigramme-roles.pptx"
    prs.save(path)
    return path


# ── export PDF via PowerPoint ──────────────────────────────────────────────

def export_pdf(paths):
    import ctypes
    import ctypes.wintypes as wt
    import pythoncom
    import win32com.client as win32

    user32 = ctypes.windll.user32

    def dismiss(pid, seconds=3.0):
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
                user32.PostMessageW(h, 0x0010, 0, 0)
            time.sleep(0.5)

    pythoncom.CoInitialize()
    app = win32.DispatchEx("PowerPoint.Application")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process POWERPNT).Id"],
                         capture_output=True, text=True).stdout.split()
    pid = max(int(x) for x in out if x.isdigit())
    try:
        for p in paths:
            pres = app.Presentations.Open(str(p), True, False, False)  # ReadOnly, Untitled, WithWindow
            dismiss(pid)
            pres.SaveAs(str(p.with_suffix(".pdf")), 32)  # ppSaveAsPDF
            pres.Close()
            print(f"{p.name}: {pres_count(p)} slides -> PDF")
    finally:
        app.Quit()


def pres_count(p):
    return len(Presentation(str(p)).slides)


if __name__ == "__main__":
    deck = build_deck()
    org = build_orgchart()
    export_pdf([deck, org])
