from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

SPOTIFY_GREEN  = RGBColor(0x1D, 0xB9, 0x54)
DARK_BG        = RGBColor(0x12, 0x12, 0x12)
DARK_CARD      = RGBColor(0x1E, 0x1E, 0x1E)
WHITE          = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY     = RGBColor(0xB3, 0xB3, 0xB3)
ACCENT_YELLOW  = RGBColor(0xFF, 0xD7, 0x00)
ACCENT_RED     = RGBColor(0xFF, 0x4C, 0x4C)
ACCENT_BLUE    = RGBColor(0x64, 0xB5, 0xF6)
ACCENT_ORANGE  = RGBColor(0xFF, 0x8C, 0x00)
DARK_GREEN     = RGBColor(0x0A, 0x52, 0x2E)
DARK_BLUE      = RGBColor(0x0A, 0x2A, 0x52)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]

# ── helpers ────────────────────────────────────────────────────────────────

def bg(slide, color=DARK_BG):
    s = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()

def rect(slide, x, y, w, h, color):
    s = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background()
    return s

def accent_bar(slide, color=SPOTIFY_GREEN, h=0.06):
    rect(slide, 0, 0, 13.33, h, color)

def tb(slide, text, x, y, w, h, size=14, bold=False,
       color=WHITE, align=PP_ALIGN.LEFT):
    t = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    t.word_wrap = True
    tf = t.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
    return t

def hline(slide, y, color=SPOTIFY_GREEN):
    rect(slide, 0.4, y, 12.5, 0.03, color)

def slide_header(slide, title, sub=None):
    accent_bar(slide)
    tb(slide, title, 0.4, 0.15, 12.5, 0.85, size=30, bold=True, color=SPOTIFY_GREEN)
    if sub:
        tb(slide, sub, 0.4, 0.92, 12.5, 0.45, size=14, color=LIGHT_GRAY)
    hline(slide, 1.3)

def card(slide, x, y, w, h, color=DARK_CARD, bar_color=None, bar_h=0.12):
    rect(slide, x, y, w, h, color)
    if bar_color:
        rect(slide, x, y, w, bar_h, bar_color)

def bullets(slide, items, x, y, w, h, size=11, color=WHITE, prefix="• "):
    t = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    t.word_wrap = True; tf = t.text_frame; tf.word_wrap = True
    first = True
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(2)
        r = p.add_run()
        r.text = (prefix if item and not item.startswith(" ") else "") + item
        r.font.size = Pt(size); r.font.color.rgb = color

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITRE
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s); accent_bar(s)

tb(s, "🎧 Spotify", 0.5, 0.55, 6, 1.1, size=42, bold=True, color=SPOTIFY_GREEN)
tb(s, "Data Governance Framework",
   0.5, 1.6, 12.3, 1.0, size=36, bold=True, color=WHITE)
tb(s, "Qualité · Conformité · Confiance — à l'échelle mondiale",
   0.5, 2.55, 12.3, 0.6, size=19, color=LIGHT_GRAY)

# Chiffres clés
for i, (val, lbl) in enumerate([("450M","utilisateurs actifs"),
                                  ("200M","abonnés premium"),("180+","pays")]):
    cx = 0.5 + i*4.2
    rect(s, cx, 3.4, 3.9, 1.6, DARK_CARD)
    rect(s, cx, 3.4, 3.9, 0.1, SPOTIFY_GREEN)
    tb(s, val, cx, 3.5, 3.9, 0.85, size=36, bold=True,
       color=SPOTIFY_GREEN, align=PP_ALIGN.CENTER)
    tb(s, lbl, cx, 4.3, 3.9, 0.5, size=13, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Bandeau bas
rect(s, 0, 6.35, 13.33, 0.85, DARK_CARD)
tb(s, "Présentation executive — Mai 2026  |  Data Governance Specialist",
   0.5, 6.45, 9, 0.5, size=12, color=LIGHT_GRAY)
tb(s, "9 slides · 20 min", 10.5, 6.45, 2.5, 0.5, size=12,
   bold=True, color=SPOTIFY_GREEN, align=PP_ALIGN.RIGHT)

# Assessment maturity score
rect(s, 0.5, 5.15, 12.3, 0.95, DARK_BLUE)
tb(s, "Score de maturité data actuel : 3,4/5  →  Cible M12 : 4,2/5  |  Dimensions critiques : Governance (2/5) · Compliance (3/5) · Quality (3/5)",
   0.65, 5.25, 12.0, 0.65, size=11, color=ACCENT_BLUE)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 2 — POURQUOI AGIR
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s)
slide_header(s, "Pourquoi agir maintenant ?",
             "3 signaux d'alarme — 9 dimensions de maturité évaluées")

cards_data = [
    ("⚠️  Risque financier", ACCENT_RED, [
        "GDPR : amende jusqu'à 20 M€",
        "   ou 4% du CA annuel mondial",
        "Notification violation : 72 h max",
        "CCPA + PDPA + LGPD cumulés",
        "   sur 180 pays",
        "Dimension Compliance : 3/5",
        "→ Chaque incident = exposition directe",
    ]),
    ("🔗  Silos inter-départements", ACCENT_YELLOW, [
        "5 dpts, 5 visions incompatibles",
        "\"Utilisateur actif\" : définition",
        "   différente Marketing vs Product",
        "Parcours user discovery→premium",
        "   impossible à analyser",
        "Dimension Governance : 2/5",
        "→ Les silos coûtent des revenus",
    ]),
    ("🛡️  Réputation & confiance", SPOTIFY_GREEN, [
        "Users sensibles à la privacy",
        "Apple Music, Amazon Music,",
        "   YouTube Music capitalisent",
        "Biais algorithme non audités",
        "EU AI Act en vigueur",
        "Dimension Data Literacy : 3/5",
        "→ La confiance est un avantage",
    ]),
]

for i, (title, color, items) in enumerate(cards_data):
    cx = 0.35 + i*4.3
    card(s, cx, 1.45, 4.1, 5.3, bar_color=color)
    tb(s, title, cx+0.12, 1.6, 3.85, 0.55, size=13, bold=True, color=color)
    t = s.shapes.add_textbox(Inches(cx+0.12), Inches(2.18), Inches(3.85), Inches(4.3))
    t.word_wrap = True; tf = t.text_frame; tf.word_wrap = True; first = True
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(2)
        r = p.add_run(); r.text = item
        r.font.size = Pt(11)
        r.font.color.rgb = color if item.startswith("→") or item.startswith("Dimension") else WHITE
        r.font.bold = item.startswith("→") or item.startswith("Dimension")

tb(s, "« Nous ne choisissons pas entre gouvernance et croissance. Sans gouvernance, la croissance s'arrête. »",
   0.35, 6.85, 12.63, 0.45, size=11, bold=True,
   color=SPOTIFY_GREEN, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 3 — 9 PRINCIPES OFFICIELS
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s)
slide_header(s, "Notre framework : 9 principes officiels",
             "Source : Governance Principles Guide Spotify")

principes = [
    ("1. Accountability", "Data Stewards + DPO\nFiches de rôle signées", SPOTIFY_GREEN),
    ("2. Transparency", "Privacy notices + OneTrust\n180 pays couverts", ACCENT_BLUE),
    ("3. Data Security", "Splunk SIEM + Vormetric\nChiffrement AES-256", ACCENT_RED),
    ("4. Data Quality", "Talend + Great Expectations\nCollibra catalogue", ACCENT_YELLOW),
    ("5. Compliance", "GDPR/CCPA/PCI-DSS\nDPIAs systématiques", ACCENT_ORANGE),
    ("6. Minimization", "Politiques strictes collecte\nRevue annuelle datasets", SPOTIFY_GREEN),
    ("7. User Rights", "Effacement <30j\nPortabilité + opt-out CCPA", ACCENT_BLUE),
    ("8. Continuous\nImprovement", "Révision annuelle\nGovernance Committee", ACCENT_RED),
    ("9. Ethical Use", "Audits biais algo trimestriels\nConformité EU AI Act", ACCENT_YELLOW),
]

cols = 3
for i, (titre, desc, color) in enumerate(principes):
    row, col = divmod(i, cols)
    cx = 0.3 + col*4.35
    cy = 1.5 + row*1.9
    card(s, cx, cy, 4.1, 1.75, bar_color=color)
    tb(s, titre, cx+0.12, cy+0.18, 3.85, 0.65, size=12, bold=True, color=color)
    tb(s, desc, cx+0.12, cy+0.82, 3.85, 0.8, size=11, color=WHITE)

# Bande objectifs officiels
rect(s, 0.3, 7.2, 12.73, 0.55, DARK_GREEN)
for i, g in enumerate(["✓ Qualité des données","✓ Conformité réglementaire",
                        "✓ Protection privacy","✓ Accessibilité & Intégration"]):
    tb(s, g, 0.45+i*3.18, 7.27, 3.1, 0.42, size=11, bold=True, color=SPOTIFY_GREEN)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 4 — CONFORMITÉ RÉGLEMENTAIRE
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s)
slide_header(s, "Conformité réglementaire mondiale",
             "5 réglementations couvertes — stack officielle : OneTrust · Splunk · Vormetric")

regs = [
    ("GDPR","Union Européenne", ACCENT_RED,
     ["Consentement explicite","Effacement <30 jours",
      "Portabilité JSON/CSV","Notification violation 72h",
      "DPIA systématique","Amende : 20M€ / 4% CA"]),
    ("CCPA","Californie (USA)", ACCENT_ORANGE,
     ["Opt-out 'Do Not Sell'","Accès données <45j",
      "Non-discrimination","Transparence collecte","",""]),
    ("PCI-DSS","Global — Paiements", ACCENT_YELLOW,
     ["Délégation Stripe","TLS 1.2+ sur flux",
      "Audit annuel","Logs accès 12 mois","",""]),
    ("PDPA / LGPD","Singapour · Brésil", SPOTIFY_GREEN,
     ["Consentement local","Notification violations",
      "Base légale explicite","LGPD : 2% CA Brésil","",""]),
]

for i,(name,zone,color,items) in enumerate(regs):
    cx = 0.3 + i*3.2
    card(s, cx, 1.45, 3.05, 4.3, bar_color=color)
    tb(s, name, cx+0.1, 1.6, 2.85, 0.5, size=18, bold=True, color=color)
    tb(s, zone, cx+0.1, 2.05, 2.85, 0.38, size=10, color=LIGHT_GRAY)
    t = s.shapes.add_textbox(Inches(cx+0.1), Inches(2.45), Inches(2.85), Inches(3.1))
    t.word_wrap = True; tf = t.text_frame; tf.word_wrap = True; first = True
    for item in [x for x in items if x]:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False; p.space_before = Pt(2)
        r = p.add_run(); r.text = "→ " + item
        r.font.size = Pt(11); r.font.color.rgb = WHITE

# Deux encarts outils
rect(s, 0.3, 5.85, 6.2, 1.1, DARK_BLUE)
tb(s, "🔒 Stack Compliance — Tech Tools Overview",
   0.45, 5.9, 5.9, 0.42, size=12, bold=True, color=ACCENT_BLUE)
tb(s, "OneTrust (GDPR/CCPA 180 pays)  ·  TrustArc (inventory/consent)  ·  VeraSafe (audits/incidents)",
   0.45, 6.3, 5.9, 0.55, size=10, color=WHITE)

rect(s, 6.8, 5.85, 6.23, 1.1, DARK_BLUE)
tb(s, "🛡️ Stack Security — Tech Tools Overview",
   6.95, 5.9, 5.9, 0.42, size=12, bold=True, color=ACCENT_RED)
tb(s, "Splunk SIEM (temps réel)  ·  DataGuard (automation GDPR)  ·  Vormetric (chiffrement BDD/fichiers)",
   6.95, 6.3, 5.9, 0.55, size=10, color=WHITE)

rect(s, 0.3, 7.0, 12.73, 0.75, RGBColor(0x15, 0x15, 0x15))
tb(s, "🤖  EU AI Act : Discover Weekly & Daily Mix soumis aux exigences d'explicabilité et non-discrimination — audits biais algorithmiques trimestriels",
   0.5, 7.07, 12.3, 0.6, size=11, color=ACCENT_BLUE)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 5 — ORGANISATION & RÔLES
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s)
slide_header(s, "Organisation & rôles",
             "Source : Data Governance Roles Template officiel — modèle CoE")

roles = [
    ("CDO","Chief Data Officer","Stratégie data globale\nPilotage du CoE\nArbitrage conflits",SPOTIFY_GREEN),
    ("DPO","Data Protection Officer","Conformité GDPR/CCPA/PDPA\nDPIAs + autorités\nBreach notification 72h",ACCENT_RED),
    ("Head\nEng.","Head of Engineering","Infrastructure GCP\nSplunk + Vormetric\nPipelines scalables",ACCENT_YELLOW),
    ("Mktg\nDir.","Marketing Director","Conformité campagnes\nQualité données mktg\nSegmentation CCPA",ACCENT_ORANGE),
    ("Legal","Legal Team","Validation juridique\nGestion litiges data\nContrats fournisseurs",ACCENT_BLUE),
    ("PM","Product Managers","Privacy by design\nConformité features\nQualité données produit",RGBColor(0xCE,0x93,0xD8)),
]

for i,(abbr,full,desc,color) in enumerate(roles):
    row, col = divmod(i, 3)
    cx = 0.3 + col*4.35
    cy = 1.45 + row*2.7
    card(s, cx, cy, 4.1, 2.5, bar_color=color)
    tb(s, abbr, cx+0.12, cy+0.17, 1.0, 0.65, size=20, bold=True, color=color)
    tb(s, full, cx+0.12, cy+0.78, 3.85, 0.42, size=10, color=LIGHT_GRAY)
    tb(s, desc, cx+0.12, cy+1.18, 3.85, 1.15, size=11, color=WHITE)

# Bande CoE + Committee
rect(s, 0.3, 6.95, 12.73, 0.85, DARK_GREEN)
tb(s, "Data Governance CoE → 5 Data Stewards (User · Content · Payments · Ads · Marketing)  +  Privacy Team (DPO + 2 analystes)",
   0.5, 7.0, 12.3, 0.42, size=11, bold=True, color=SPOTIFY_GREEN)
tb(s, "Data Governance Committee mensuel : CDO + DPO + Head Eng. + Mktg Dir. + Legal + 5 Stewards + représentant Product",
   0.5, 7.38, 12.3, 0.38, size=10, color=WHITE)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 6 — PLAN D'IMPLÉMENTATION
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s)
slide_header(s, "Plan d'implémentation",
             "4 phases · 12 mois · timeline validée par l'Executive Q&A Guide")

phases = [
    ("M1-M2","FONDATIONS",SPOTIFY_GREEN,
     ["CDO nommé","CoE + Privacy Team","OneTrust 180 pays",
      "Collibra pilote","Splunk + Vormetric","Formation M1"]),
    ("M3-M4","PILOTE\nUSER DATA",ACCENT_YELLOW,
     ["Talend + Great Exp.","Pipeline GDPR <30j",
      "DPIA validée","Audit biais algo v1","Go/No-Go M4",""]),
    ("M5-M8","GÉNÉRALISATION",ACCENT_ORANGE,
     ["Content + Payments","Marketing + Ads",
      "5 domaines Collibra","VeraSafe (Payments)","OneTrust étendu",""]),
    ("M9-M12","INDUSTRIALISATION",ACCENT_RED,
     ["Monte Carlo déployé","OpenLineage actif",
      "Ataccama ONE (AI quality)","Audit conformité complet",
      "Audit biais algo complet","Dashboard exécutif"]),
]

for i,(period,name,color,items) in enumerate(phases):
    cx = 0.3 + i*3.2
    rect(s, cx, 1.45, 3.05, 0.8, color)
    tb(s, period, cx+0.1, 1.48, 2.85, 0.32, size=12, bold=True,
       color=DARK_BG, align=PP_ALIGN.CENTER)
    tb(s, name, cx+0.1, 1.76, 2.85, 0.48, size=11, bold=True,
       color=DARK_BG, align=PP_ALIGN.CENTER)
    card(s, cx, 2.25, 3.05, 3.4)
    bullets(s, items, cx+0.12, 2.35, 2.85, 3.2, size=11)
    if i < 3:
        tb(s, "►", cx+3.05, 3.4, 0.2, 0.45, size=16, bold=True, color=color)

# Stack outils — tableau 2 colonnes
rect(s, 0.3, 5.75, 12.73, 1.55, DARK_CARD)
tb(s, "Stack officielle (Tech Tools Overview)", 0.5, 5.8, 12.3, 0.38,
   size=12, bold=True, color=SPOTIFY_GREEN)

col1 = [("Catalogue","Collibra  /  Alation  /  Apache Atlas"),
        ("Qualité","Talend  /  Informatica  /  Ataccama ONE  /  Great Expectations")]
col2 = [("Compliance","OneTrust  /  TrustArc  /  VeraSafe"),
        ("Security","Splunk (SIEM)  /  DataGuard  /  Vormetric (chiffrement)")]

for i,(label,val) in enumerate(col1):
    cy = 6.2 + i*0.5
    tb(s, label+":", 0.5, cy, 1.3, 0.42, size=10, bold=True, color=SPOTIFY_GREEN)
    tb(s, val, 1.8, cy, 4.5, 0.42, size=10, color=WHITE)
for i,(label,val) in enumerate(col2):
    cy = 6.2 + i*0.5
    tb(s, label+":", 6.8, cy, 1.3, 0.42, size=10, bold=True, color=SPOTIFY_GREEN)
    tb(s, val, 8.1, cy, 5.1, 0.42, size=10, color=WHITE)

tb(s, "Pilote : 2 mois (M3-M4)  ·  Rollout complet : 12 mois  ·  Audit conformité : M10  |  Conforme Executive Q&A Guide (3-6 mois pilote, 12-18 mois rollout)",
   0.3, 7.3, 12.73, 0.42, size=9, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 7 — PILOTE USER DATA + KPIs OFFICIELS
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s)
slide_header(s, "Pilote User Data — KPIs officiels",
             "Source : Pilot Implementation Template — M3-M4")

# Justification (gauche)
card(s, 0.3, 1.45, 5.9, 4.2)
tb(s, "Pourquoi User Data en premier ?", 0.45, 1.55, 5.6, 0.5,
   size=14, bold=True, color=SPOTIFY_GREEN)
justifs = [
    "450M utilisateurs concernés par le GDPR",
    "Données révélant des infos sensibles",
    "  (état émotionnel, convictions implicites)",
    "Risque : jusqu'à 4% du CA mondial",
    "  si incident de données",
    "Alimente Discover Weekly, Daily Mix,",
    "  toutes les playlists personnalisées",
    "Impact direct sur la rétention premium",
]
t = s.shapes.add_textbox(Inches(0.45), Inches(2.1), Inches(5.6), Inches(3.3))
t.word_wrap = True; tf = t.text_frame; tf.word_wrap = True; first = True
for item in justifs:
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    first = False; p.space_before = Pt(3)
    r = p.add_run(); r.text = ("→ " if not item.startswith(" ") else "") + item
    r.font.size = Pt(12)
    r.font.color.rgb = SPOTIFY_GREEN if r.text.startswith("→") else WHITE
    r.font.bold = r.text.startswith("→")

# KPIs officiels (droite)
card(s, 6.5, 1.45, 6.53, 4.2)
tb(s, "KPIs officiels (Pilot Template)", 6.65, 1.55, 6.3, 0.5,
   size=14, bold=True, color=ACCENT_YELLOW)

kpis = [
    ("Data Quality Score","-10% données manquantes → >98%","Talend + Great Exp."),
    ("Compliance Score","100% consentements valides","OneTrust"),
    ("Data Access Speed","+20% amélioration accès data","Avant/après Collibra"),
    ("Risk Mitigation","0 brèche pendant le pilote","Splunk SIEM"),
    ("Pipeline GDPR","Effacement <30 jours opérationnel","Test end-to-end"),
    ("Biais algorithmiques","0 biais critique Discover Weekly","Audit DPO"),
]

for i,(label,val,tool) in enumerate(kpis):
    cy = 2.1 + i*0.59
    rect(s, 6.5, cy, 6.53, 0.54, RGBColor(0x28,0x28,0x28))
    tb(s, "✓ " + label, 6.65, cy+0.03, 2.4, 0.48, size=10, bold=True, color=WHITE)
    tb(s, val, 9.05, cy+0.03, 2.5, 0.48, size=10, bold=True, color=ACCENT_YELLOW)
    tb(s, tool, 11.6, cy+0.03, 1.2, 0.48, size=8, color=LIGHT_GRAY)

# Livrables officiels
rect(s, 0.3, 5.72, 12.73, 0.72, DARK_BLUE)
tb(s, "Livrables officiels (Pilot Template) :",
   0.5, 5.77, 3, 0.35, size=11, bold=True, color=ACCENT_BLUE)
tb(s, "Data Quality Report  ·  Compliance Assessment  ·  Technical Integration Plan  ·  Risk Assessment Report  ·  Stakeholder Feedback",
   3.6, 5.77, 9.2, 0.35, size=10, color=WHITE)

tb(s, "« Si nous protégeons bien les données les plus sensibles, nous pouvons tout gouverner. »",
   0.3, 6.52, 12.73, 0.42, size=12, bold=True,
   color=SPOTIFY_GREEN, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 8 — ROI & BÉNÉFICES
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s)
slide_header(s, "ROI & bénéfices attendus",
             "Source : Executive Q&A Guide — Q3 · Business value en 4 dimensions")

# 4 dimensions officielles (Q3 Executive Q&A)
dims = [
    ("💰 Cost Savings", SPOTIFY_GREEN,
     ["Qualité améliorée → moins d'inefficacités","Données fiables → décisions plus rapides",
      "Moins d'audits correctifs a posteriori","Time-to-market réduit (privacy by design)"]),
    ("⚖️ Compliance", ACCENT_RED,
     ["0 amende GDPR/CCPA/PDPA","Éviter jusqu'à 4% du CA mondial","0 pénalité CCPA (class action)",
      "EU AI Act : 0 risque retrait de marché"]),
    ("🤝 Trust", ACCENT_BLUE,
     ["Transparence → fidélité utilisateurs","Contrôle data → churn réduit UE",
      "Éthique algo → avantage pub","Différenciateur vs Apple Music/Amazon"]),
    ("📈 Scalability", ACCENT_YELLOW,
     ["Infrastructure scalable 200M→300M+","Framework adaptable nouvelles réglementations",
      "Outils évolutifs (Talend, Collibra)","Expansion nouveaux marchés facilitée"]),
]

for i,(title,color,items) in enumerate(dims):
    cx = 0.3 + i*3.25
    card(s, cx, 1.45, 3.1, 4.3, bar_color=color)
    tb(s, title, cx+0.12, 1.62, 2.86, 0.55, size=13, bold=True, color=color)
    bullets(s, items, cx+0.12, 2.2, 2.86, 3.4, size=11, prefix="→ ")

# Tableau risques financiers évités
rect(s, 0.3, 5.85, 12.73, 1.45, DARK_CARD)
tb(s, "Risques financiers évités", 0.5, 5.9, 4, 0.42,
   size=12, bold=True, color=ACCENT_RED)
risks = [
    ("GDPR (violation majeure)","Jusqu'à 20 M€ ou 4% CA mondial"),
    ("CCPA + PDPA + LGPD","Plusieurs M€ cumulés"),
    ("EU AI Act (biais algo)","Retrait de marché possible"),
    ("Class action utilisateurs","Coûts juridiques + réputation"),
]
for i,(risk,expo) in enumerate(risks):
    cy = 6.35 + (i // 2)*0.42
    cx_off = (i % 2)*6.3
    tb(s, "▸ "+risk, 0.5+cx_off, cy, 3.5, 0.38, size=10, color=WHITE)
    tb(s, expo, 4.0+cx_off, cy, 2.7, 0.38, size=10, bold=True, color=ACCENT_RED)

tb(s, "« La gouvernance n'est pas un coût. C'est une assurance et un accélérateur de croissance. »",
   0.3, 7.35, 12.73, 0.42, size=11, bold=True,
   color=SPOTIFY_GREEN, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════════════
# SLIDE 9 — PROCHAINES ÉTAPES + Q&A
# ══════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(blank)
bg(s)
slide_header(s, "Prochaines étapes & Q&A anticipé",
             "3 décisions aujourd'hui — 12 questions officielles (Executive Q&A Guide)")

# 3 décisions
decisions = [
    ("1","Nommer le CDO",SPOTIFY_GREEN,
     "Condition sine qua non — sans CDO, le CoE ne peut pas être constitué.",
     "→ Valider profil et nommer avant fin du mois."),
    ("2","Valider le budget Phases 1-2",ACCENT_YELLOW,
     "Outils (Collibra, OneTrust, Splunk, Vormetric) + CoE + formation. Offset par réduction risque.",
     "→ Approuver le budget Phases 1-2."),
    ("3","Lancer la communication interne",ACCENT_RED,
     "Le change management est le risque #1. Plus tôt les équipes sont informées, moins la résistance est forte.",
     "→ Planifier webinar CEO/CDO pour le Mois 1."),
]

for i,(num,title,color,desc,action) in enumerate(decisions):
    cy = 1.42 + i*1.55
    card(s, 0.3, cy, 7.8, 1.42, bar_color=color, bar_h=0.08)
    rect(s, 0.45, cy+0.18, 0.65, 0.65, color)
    tb(s, num, 0.45, cy+0.18, 0.65, 0.65, size=20, bold=True,
       color=DARK_BG, align=PP_ALIGN.CENTER)
    tb(s, title, 1.25, cy+0.14, 4, 0.48, size=15, bold=True, color=color)
    tb(s, desc, 1.25, cy+0.62, 6.6, 0.42, size=10, color=LIGHT_GRAY)
    tb(s, action, 1.25, cy+1.02, 6.6, 0.35, size=11, bold=True, color=WHITE)

# Q&A 6 questions clés (droite)
card(s, 8.35, 1.42, 4.68, 4.65)
tb(s, "Q&A — 12 questions officielles", 8.5, 1.52, 4.4, 0.45,
   size=12, bold=True, color=ACCENT_BLUE)
qa_short = [
    ("Q1","Pourquoi maintenant ?","450M users, GDPR 4% CA, silos coûteux"),
    ("Q5","Pourquoi le CoE ?","Équilibre gouvernance/autonomie squads"),
    ("Q6","Comment mesurer le succès ?","-10% missing, +20% accès, 100% consent"),
    ("Q7","Combien de temps ?","Pilote M3-M4 · Rollout complet M12"),
    ("Q8","Quels coûts ?","Outils + formation + CoE → offset long terme"),
    ("Q12","Impact sur l'innovation ?","Non — données fiables = innovation plus rapide"),
]
for i,(q,short,rep) in enumerate(qa_short):
    cy = 2.0 + i*0.67
    rect(s, 8.35, cy, 4.68, 0.62, RGBColor(0x28,0x28,0x28))
    tb(s, q, 8.5, cy+0.04, 0.5, 0.52, size=10, bold=True, color=ACCENT_BLUE)
    tb(s, short, 9.0, cy+0.04, 2.2, 0.28, size=10, bold=True, color=WHITE)
    tb(s, rep, 9.0, cy+0.32, 3.8, 0.26, size=9, color=LIGHT_GRAY)

# Timeline décision
rect(s, 0.3, 6.12, 7.8, 0.6, DARK_BLUE)
milestones = [("Aujourd'hui\nGO/NO-GO",0.45),("Fin du mois\nCDO nommé",2.15),
              ("Mois 1\nKick-off",3.85),("Mois 3\nPilote démarre",5.55)]
for label,x in milestones:
    tb(s, label, x, 6.14, 1.6, 0.55, size=9, bold=True,
       color=SPOTIFY_GREEN, align=PP_ALIGN.CENTER)

rect(s, 0.3, 6.75, 12.73, 0.62, DARK_GREEN)
tb(s, "Full rollout M12  ·  Audit conformité M10  ·  ROI positif attendu dès M6  |  Conforme Executive Q&A Guide : pilote 3-6 mois · rollout 12-18 mois",
   0.5, 6.82, 12.3, 0.48, size=11, bold=True, color=SPOTIFY_GREEN, align=PP_ALIGN.CENTER)

# ── Sauvegarde ─────────────────────────────────────────────────────────────
out = r"D:\##__PROJETS__##\_Projets en cours\00 - 2025 - Jedha\spotify-data-governance\spotify-data-governance-presentation.pptx"
prs.save(out)
print(f"PPTX v3.0 généré : {out}")
