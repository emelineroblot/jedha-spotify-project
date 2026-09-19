"""Assemble le document Word unique « Plan de gouvernance » demandé par Jedha :
page de garde, sommaire, synthèse, les 4 parties (depuis les .md existants), l'organigramme
(image exportée du pptx) et la checklist (depuis le xlsx) en annexes.
Sortie : livrables/00-plan-de-gouvernance.docx + .pdf. Ne réécrit aucun contenu."""
import os
import re
import time
from pathlib import Path

import openpyxl
import pythoncom
import win32com.client as win32

import generate_docx as gd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "livrables"
ASSETS = ROOT / "assets"
SRC_MD = ROOT / "build" / "_plan-de-gouvernance.md"   # intermédiaire, non versionné

PAGE_BREAK = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'


def body(md_path: Path) -> str:
    """Contenu d'un .md sans son en-tête YAML."""
    s = md_path.read_text(encoding="utf8")
    s = re.sub(r"\A---\n.*?\n---\n", "", s, flags=re.S)
    return s.strip()


def export_orgchart_png() -> Path:
    """Exporte la slide 1 du deck organigramme en PNG (PowerPoint COM)."""
    png = ASSETS / "organigramme.png"
    pythoncom.CoInitialize()
    app = win32.DispatchEx("PowerPoint.Application")
    try:
        pres = app.Presentations.Open(str(OUT / "02-organigramme-roles.pptx"), True, False, False)
        time.sleep(1)
        pres.Slides(1).Export(str(png), "PNG", 2400, 1350)
        pres.Close()
    finally:
        app.Quit()
    # retirer le bandeau de titre et le pied de page de la slide : ne garder que le schéma
    from PIL import Image
    im = Image.open(png)
    w, h = im.size
    im.crop((0, int(h * 0.19), w, int(h * 0.93))).save(png)
    return png


def checklist_table() -> str:
    ws = openpyxl.load_workbook(OUT / "02-compliance-checklist.xlsx")["Checklist"]
    rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    out = ["| Exigence | Statut | Action plan | Owner | Échéance |",
           "|----------------------|---------|--------------------------------------------|------------|-----------|"]
    for area, req, status, plan, owner, due in rows:
        cell = lambda v: str(v or "").replace("|", "/").replace("\n", " ")
        out.append(f"| **{cell(area)}** — {cell(req)} | {cell(status)} | {cell(plan)} | {cell(owner)} | {cell(due)} |")
    return "\n".join(out)


def build_markdown() -> str:
    e1 = body(ROOT / "etape1-data-maturity-assessment.md")
    e2 = body(ROOT / "etape2-framework-gouvernance.md").replace(
        "l'organigramme et les fiches détaillées font l'objet d'un livrable séparé",
        "l'organigramme et les fiches détaillées sont en Partie 3")
    e3 = body(ROOT / "etape3-plan-implementation.md")
    org = body(ROOT / "etape2-organigramme-roles.md")
    # fiches de rôle : tout ce qui suit le titre « Slide 2 » du md organigramme
    fiches = org.split("## Slide 2 — Fiches de rôle (Data Governance Roles Template)", 1)[1].strip()
    # le paragraphe Committee remonte sous le schéma, avant les tableaux
    marker = "**Data Governance Committee — composition"
    committee = fiches[fiches.index(marker):].strip()
    fiches = fiches[:fiches.index(marker)].strip()

    md = f"""---
title: "Plan de Data Governance — Spotify"
subtitle: "Diagnostic de maturité · Politique de gouvernance · Organisation & rôles · Plan d'implémentation et pilote"
author: "Emeline ROBLOT — Data Governance Specialist"
date: "Septembre 2026 · Version 1.0"
---

| Rôle joué | Livrable | Périmètre | Conformités visées |
|--------------|------------------------|--------------------------------|------------------------|
| Data Governance Specialist, Spotify | Plan de gouvernance (document unique) et présentation executive associée | Opérations data globales — 450 M d'utilisateurs, 200 M d'abonnés premium, 180+ pays | GDPR · CCPA/CPRA · PCI-DSS · PDPA · LGPD · DSA |

Ce document rassemble les quatre étapes du projet en un plan de gouvernance unique. Chaque partie est lisible seule ; les annexes contiennent la checklist de conformité remplie et les sources. Les chiffres sourcés et les hypothèses de travail sont distingués explicitement (annexe B).
{PAGE_BREAK}
**Sommaire**

[[TOC]]
{PAGE_BREAK}
# Synthèse exécutive

**Le constat.** Spotify est un leader technologique — architecture et analytics au niveau 5 sur 5 — sans gouvernance transverse des données : pas de Chief Data Officer, pas d'ownership par domaine, des définitions de métriques qui divergent entre Marketing, Product, Engineering et Content. Score de maturité global : **3,4 / 5**, avec la dimension Data Governance à **2**. Le risque n'est pas théorique : en juin 2023, l'autorité suédoise (IMY) a sanctionné Spotify de **58 M SEK (≈ 5 M€)** pour un droit d'accès GDPR insuffisamment clair — une défaillance de gouvernance, pas d'infrastructure. L'exposition maximale GDPR représente 4 % du CA mondial, soit **≈ 530 M€** sur le CA 2023.

**Le framework.** Une Data Governance Policy de trois pages fondée sur les neuf principes du Governance Principles Guide, structurée en trois piliers : qualité et accessibilité (cinq domaines de données, un Data Steward chacun, quatre critères mesurés, un catalogue unique) ; conformité et sécurité (base légale documentée par finalité, sept droits des personnes couverts, DPIA, classification en quatre niveaux, durées de conservation) ; culture et éthique (formation par rôle, audit trimestriel des biais de recommandation, interdiction de profiler sur des catégories sensibles inférées).

**L'organisation.** Un **Centre of Excellence** sous le CDO, avec cinq Data Stewards relais dans les business units, un DPO indépendant et sa Privacy Team, et un Data Governance Committee mensuel. La gouvernance définit et audite ; l'engineering, sous le CTO, implémente.

**Le plan.** Quatre phases sur 18 mois : fondations (M1-M2), **pilote User Data sur les marchés UE (M3-M6)** avec Go/No-Go du Committee, généralisation aux quatre autres domaines (M7-M12), industrialisation (M13-M18). Un outil par besoin, en s'appuyant sur l'existant (GCP, Airflow, catalogue Lexikon). Cible de maturité à 12 mois : **4,2 / 5**.

**L'impact.** Programme estimé à **6-7 M€ sur 18 mois** (ordres de grandeur, hypothèses à affiner en phase 1), soit environ 1 % de l'exposition maximale et à peine plus que la sanction déjà subie ; gains d'efficacité estimés à ≈ 3 M€/an sur le seul accès aux données. **Trois décisions demandées au comité exécutif** : nommer le CDO sous 30 jours, approuver le budget des phases 1-2 (≈ 2,5 M€), lancer la communication interne en M1.

# Partie 1 — Data Maturity Assessment

{e1}

# Partie 2 — Data Governance Policy

{e2}

# Partie 3 — Organisation & rôles

Modèle **Centre of Excellence** : la gouvernance (CDO, CoE, Data Stewards) définit les standards et audite ; le data management (CTO, Head of Engineering, Data Engineers) implémente. Deux lignes hiérarchiques distinctes, une collaboration formalisée par le RACI (Partie 2, §6). Le DPO est hors de la ligne du CDO pour garantir son indépendance (GDPR art. 38).

![](assets/organigramme.png){{width=15cm}}

{committee}

{fiches}

# Partie 4 — Implementation Plan & pilote

{e3}

# Annexe A — Compliance Checklist (GDPR · CCPA/CPRA · PCI-DSS)

Checklist officielle du projet, complétée. Statut = état actuel estimé à l'issue du Data Maturity Assessment (hypothèse, sans accès aux données internes) ; action plan = mesures de la politique (Partie 2) ; échéance = mois du plan d'implémentation (Partie 4). Fichier de travail : `02-compliance-checklist.xlsx`.

{checklist_table()}

# Annexe B — Sources et hypothèses

**Chiffres sourcés (sources publiques, vérifiées en septembre 2026).**

- **Sanction IMY** : autorité suédoise de protection des données, juin 2023 — amende administrative de 58 M SEK contre Spotify AB pour manquement au droit d'accès (GDPR art. 15 : information insuffisante sur les finalités, durées de conservation et transferts) ; confirmée par la cour administrative d'appel. Sources : imy.se, noyb.eu.
- **Chiffre d'affaires 2023** : 13,247 Md€ (Spotify Technology S.A., rapport annuel Form 20-F 2023) → 4 % ≈ 530 M€.
- **Catalogue interne Lexikon** et migration GCP/BigQuery depuis 2016 : Spotify Engineering, « How We Improved Data Discovery for Data Scientists at Spotify », février 2020 (adoption par 95 % des data scientists).
- **Contexte** : business case Jedha (450 M d'utilisateurs actifs, 200 M d'abonnés premium, 180+ pays, 2023).

**Ressources Jedha utilisées.** Data Maturity Assessment Template (9 dimensions) · Governance Principles Guide (9 principes) · Data Governance Roles Template (4 rôles) · Compliance Checklist (14 exigences, annexe A) · Organizational Models Overview (Centralisé / Embedded / CoE) · Tech Tools Overview · Pilot Implementation Template (10 sections) · Executive Q&A Guide (12 questions, traitées dans la présentation).

**Hypothèses de travail (à valider en phase 1 — audit de l'existant).** Existence d'un DPO en place ; délégation des paiements à un prestataire certifié PCI-DSS (aucun numéro de carte stocké) ; part de métadonnées de contenu incomplètes côté labels et distributeurs indépendants ; absence de SIEM unifié ; coûts du programme (10,5 ETP à 120 k€ chargés, licences 1,5-2,5 M€/an, intégration 0,5-1 M€, formation 0,3 M€) ; gain d'efficacité (500 analystes × 2 h/semaine) ; durées de conservation initiales. Chaque hypothèse est signalée « (hyp.) » à l'endroit où elle est utilisée.

**Réglementations citées.** GDPR (UE 2016/679) · CCPA (2018) et CPRA (2023) · PCI-DSS v4.0 · PDPA Singapour · LGPD Brésil · DSA (UE 2022/2065, art. 27 et 38) · AI Act (UE 2024/1689).
"""
    return md


def main():
    export_orgchart_png()
    SRC_MD.write_text(build_markdown(), encoding="utf8")
    dst = OUT / "00-plan-de-gouvernance.docx"
    gd.pandoc(SRC_MD, dst)
    pythoncom.CoInitialize()
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    pid = gd._word_pid()
    try:
        pages = gd.polish(word, pid, dst, max_pages=99, toc=True)
    finally:
        word.Quit()
    print(f"{dst.name}: {pages} pages -> PDF")


if __name__ == "__main__":
    os.chdir(ROOT)
    main()
