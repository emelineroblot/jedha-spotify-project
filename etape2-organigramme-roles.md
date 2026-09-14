---
title: "Organisation & Rôles — Spotify Data Governance"
author: "Emeline ROBLOT — Data Governance Specialist"
date: "Septembre 2026"
---

> Livrable PowerPoint (2 slides) : `livrables/02-organigramme-roles.pptx`, généré par `generate_pptx.py`. Ce fichier est la source de contenu.

## Slide 1 — Organigramme (modèle Centre of Excellence)

```
                                   CEO
          ┌──────────────────┬──────┴───────┬──────────────────┐
         CDO                DPO            CTO               Legal
   (stratégie data,    (indépendant,   (technologie)     (validation
    pilote le CoE)     conformité)          │             juridique)
          │                 │               │
   Data Governance     Privacy Team    Head of Engineering
   CoE (4-6 pers.)     (2 analystes)        │
          │                             Data Engineers
   ┌──────┼──────┬──────┬──────┐   (implémentent les contrôles)
 Steward Steward Steward Steward Steward
  USER   CONTENT  PAY.   ADS   MKTG
   └── chacun rattaché fonctionnellement à sa business unit ──┘

 Transverse : Data Governance Committee (mensuel, présidé par le CDO)
 Parties prenantes : Marketing Director · Product Managers · Department Heads
```

**Principe de séparation (cours Jedha)** : la **gouvernance** (CDO, CoE, stewards) définit les standards et audite ; le **data management** (CTO, Head of Engineering, Data Engineers) implémente. Deux lignes hiérarchiques distinctes, une collaboration formalisée par le RACI. Le DPO est hors de la ligne du CDO pour garantir son indépendance (GDPR art. 38).

## Slide 2 — Fiches de rôle (Data Governance Roles Template)

| Rôle | Rattachement | Responsabilité principale | Tâches clés |
|---|---|---|---|
| **Chief Data Officer** | CEO | Diriger la stratégie et la gouvernance des données | Définir les politiques ; arbitrer les conflits inter-domaines ; piloter le CoE et le Committee ; aligner avec les priorités business ; rendre compte au comité exécutif |
| **Data Protection Officer** | CEO (indépendant) | Garantir la conformité GDPR, CCPA et réglementations locales | Registre des traitements ; DPIA ; contact des autorités ; pilotage des incidents et notification 72 h ; direction de la Privacy Team ; veille réglementaire avec Legal |
| **Data Governance Committee** | Présidé par le CDO | Guider le framework et assurer l'alignement transverse | Approuver politiques et standards ; traiter les sujets inter-départements ; suivre les KPIs ; valider les Go/No-Go du plan |
| **Data Steward** (×5 : User, Content, Payments, Ads, Marketing) | CoE + business unit | Superviser les pratiques data de son domaine | Qualité, classification et durées de conservation ; accorder et revoir les accès ; alimenter le catalogue ; faire appliquer la politique ; reporting mensuel |

**Parties prenantes** (business case) :

| Rôle | Contribution à la gouvernance |
|---|---|
| Head of Engineering (sous le CTO) | Implémentation technique : pipelines, chiffrement, SIEM, pipeline d'effacement, scalabilité |
| Legal Team | Validation juridique des politiques, contrats fournisseurs, litiges |
| Marketing Director | Conformité des campagnes (consentement, opt-out), qualité des données marketing |
| Product Managers | Privacy by design, DPIA sur chaque nouvelle feature, qualité des données produit |
| Privacy Team (DPO + 2 analystes) | Traitement des demandes des personnes dans les délais légaux (1 mois GDPR, 45 j CCPA) |

**Data Governance Committee — composition et ordre du jour type (mensuel, 60 min)** : CDO (président), DPO, Head of Engineering, Marketing Director, Legal, 5 Data Stewards, 1 représentant Product. Ordre du jour : KPIs qualité par domaine · incidents et demandes des personnes · nouveaux traitements / DPIA · avancement du plan · audits de biais · décisions.
