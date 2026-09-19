# Spotify — Data Governance Framework

Projet Jedha (6 h) : concevoir et piloter un framework de Data Governance pour Spotify, conforme GDPR, CCPA/CPRA et PCI-DSS.
Auteur : Emeline ROBLOT — Data Governance Specialist · Septembre 2026.

## Les deux fichiers à déposer

| Livrable attendu | Fichier | Contenu |
|---|---|---|
| **Le plan de gouvernance** (Word) | `livrables/00-plan-de-gouvernance.docx` / `.pdf` | Document unique, 15 pages : synthèse exécutive, Partie 1 maturité, Partie 2 policy, Partie 3 organisation, Partie 4 plan & pilote, annexes checklist et sources |
| **La présentation du plan résumé** (PowerPoint) | `livrables/04-presentation-executive.pptx` / `.pdf` | 9 slides + annexes Q&A, notes orateur |

## Livrables détaillés par étape (`livrables/`)

Les parties du plan de gouvernance existent aussi en fichiers séparés, aux formats et longueurs de l'énoncé détaillé :

| Étape | Livrable énoncé | Fichier | Format |
|---|---|---|---|
| 1 | Data Maturity Assessment (1-2 pages) | `01-data-maturity-assessment.docx` / `.pdf` | Word, 2 pages |
| 2 | Data Governance Policy (2-3 pages) | `02-data-governance-policy.docx` / `.pdf` | Word, 3 pages |
| 2 | Organigramme rôles & responsabilités (1 page) | `02-organigramme-roles.pptx` / `.pdf` | PowerPoint, 2 slides |
| 2 | Compliance Checklist GDPR / CCPA / PCI-DSS | `02-compliance-checklist.xlsx` | Excel, 14 exigences remplies |
| 3 | Implementation Plan (2-3 pages) | `03-implementation-plan.docx` / `.pdf` | Word, 3 pages |
| 4 | Présentation executive (5-10 slides) | `04-presentation-executive.pptx` / `.pdf` | PowerPoint, 9 slides + 6 d'annexes, notes orateur |

## Sources de contenu

Les livrables sont générés depuis les fichiers Markdown à la racine :

- `etape1-data-maturity-assessment.md`
- `etape2-framework-gouvernance.md` (policy)
- `etape2-organigramme-roles.md`
- `etape3-plan-implementation.md`
- `etape4-presentation-executive.md` (contenu des slides, notes orateur, Q&A)

## Régénérer les livrables

```bash
pip install python-pptx python-docx openpyxl matplotlib pywin32
python build/build_all.py
```

Prérequis : `pandoc` dans le PATH, Microsoft Word et PowerPoint installés (export PDF et vérification du nombre de pages via COM).

| Script | Rôle |
|---|---|
| `build/generate_charts.py` | Radar de maturité, Gantt, graphique d'impact → `assets/` |
| `build/generate_checklist.py` | Remplit la Compliance Checklist officielle → `livrables/02-compliance-checklist.xlsx` |
| `build/generate_docx.py` | Markdown → docx (pandoc), mise en forme et pied de page (Word), export PDF, contrôle du nombre de pages |
| `build/generate_pptx.py` | Deck executive + organigramme (python-pptx), export PDF (PowerPoint) |
| `build/generate_plan.py` | Assemble le plan de gouvernance unique (parties depuis les .md, organigramme en image, checklist en annexe), sommaire automatique, PDF |

## Décisions clés

- Modèle organisationnel : **Centre of Excellence** (CoE sous le CDO, 5 Data Stewards relais, Committee mensuel) ; gouvernance et data management séparés.
- Domaine pilote : **User Data**, périmètre UE, M3-M6, Go/No-Go du Committee.
- Plan : 4 phases sur 18 mois (Fondations · Pilote · Généralisation · Industrialisation).
- Outils : Collibra ou extension de Lexikon, Great Expectations, OneTrust, Splunk, Thales/Vormetric, OpenLineage, Monte Carlo.
- Chiffres sourcés : CA 2023 13,25 Md€ (4 % ≈ 530 M€), sanction IMY juin 2023 (58 M SEK ≈ 5 M€), Lexikon (Spotify Engineering, 2020). Les autres chiffres sont des hypothèses signalées comme telles.
