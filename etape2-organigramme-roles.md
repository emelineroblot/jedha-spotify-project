# Étape 2 — Organigramme des Rôles : Spotify Data Governance

**Auteur** : Data Governance Specialist  
**Date** : Mai 2026  
**Version** : 2.0 (mise à jour sur base du Business Case officiel)

---

## Organigramme

```
                            ┌─────────────────┐
                            │      CEO        │
                            └───────┬─────────┘
                                    │
          ┌─────────────────────────┼──────────────────────────┐
          │                         │                          │
 ┌────────▼────────┐      ┌─────────▼──────┐        ┌─────────▼──────┐
 │  Chief Data     │      │     Data       │        │   Legal Team   │
 │  Officer (CDO)  │      │  Protection    │        │                │
 │                 │      │ Officer (DPO)  │        │                │
 └────────┬────────┘      └────────────────┘        └────────────────┘
          │
  ┌───────┴────────────────────────────────────┐
  │          Data Governance CoE               │
  │   (Centre of Excellence — standards,       │
  │    catalogue, qualité, formation)          │
  └──┬──────┬──────┬──────┬──────┬─────────────┘
     │      │      │      │      │
 ┌───▼──┐ ┌─▼────┐ ┌▼────┐ ┌▼───┐ ┌▼──────────┐
 │Data  │ │Data  │ │Data │ │Data│ │Data       │
 │Stew. │ │Stew. │ │Stew.│ │St. │ │Steward    │
 │USER  │ │CONT. │ │PAY. │ │ADS │ │MARKETING  │
 └──────┘ └──────┘ └─────┘ └────┘ └───────────┘
     │         │       │      │         │
     └─────────┴───────┴──────┴─────────┘
                        │
         ┌──────────────▼──────────────┐
         │      Head of Engineering    │
         │   (infrastructure, pipelines│
         │    sécurité, scalabilité)   │
         └──────────────┬──────────────┘
                        │
         ┌──────────────▼──────────────┐
         │       Data Engineers        │
         │  (implémentation technique, │
         │   Great Expectations, GCP)  │
         └─────────────────────────────┘

 Autres parties prenantes transversales :
 ┌──────────────────┐    ┌────────────────────┐
 │ Marketing        │    │ Product Managers   │
 │ Director         │    │ (conformité des    │
 │ (données campag. │    │  nouvelles         │
 │  conformité ads) │    │  fonctionnalités)  │
 └──────────────────┘    └────────────────────┘
```

---

## Fiches synthétiques

| Rôle | Rattachement | Périmètre | Responsabilité governance |
|---|---|---|---|
| **CDO** | CEO | Stratégie data globale | Définit la politique, arbitre les conflits, pilote le CoE |
| **DPO** | Board (indépendant) | Conformité GDPR/CCPA/PDPA | DPIAs, audits, point de contact CNIL et autorités |
| **Legal Team** | CEO | Conformité juridique globale | Valide les politiques, gère les risques légaux et litiges data |
| **Head of Engineering** | CDO | Infrastructure data | Scalabilité, sécurité, implémentation technique des contrôles |
| **Marketing Director** | CDO / CMO | Données campagnes & segmentation | Conformité des pratiques marketing, qualité des données ads |
| **Product Managers** | Head of Product | Données produit | Conformité des nouvelles features, qualité des données produit |
| **Data Governance CoE** | CDO | Standards, catalogue, formation | Maintient le catalogue Collibra, les standards, forme les équipes |
| **Data Steward — User Data** | CoE + BU Users | Comportements d'écoute, profils | Ownership qualité, règles Great Expectations, pipeline GDPR |
| **Data Steward — Content** | CoE + BU Content | Métadonnées musicales & podcasts | Qualité ISRC, cohérence métadonnées labels |
| **Data Steward — Payments** | CoE + Finance | Transactions, facturation | Conformité PCI-DSS, audit annuel |
| **Data Steward — Ads** | CoE + BU Ads | Ciblage, impressions, conversions | Conformité CCPA opt-out, qualité segments |
| **Data Steward — Marketing** | CoE + Marketing | Campagnes, segmentation, conversion | Cohérence métriques, conformité données marketing |
| **Data Engineers** | Head of Engineering | Pipelines GCP, Airflow | Implémentation Great Expectations, pseudonymisation, chiffrement |

---

## Privacy Team dédiée

Conformément aux recommandations du business case, une **Privacy Team** est rattachée au DPO :

| Membre | Rôle |
|---|---|
| DPO | Responsable de la Privacy Team |
| Privacy Analysts (x2) | Traitement des demandes utilisateurs (GDPR/CCPA) |
| Data Stewards concernés | Support sur les domaines impliqués |

**Volume estimé** : Spotify reçoit des milliers de demandes d'effacement et d'accès par mois à l'échelle mondiale — la Privacy Team garantit le respect des délais légaux (30j pour effacement, 45j pour accès CCPA, 72h pour notification de violation).

---

## Interactions clés

```
CDO ──────────────────► Définit politique, arbitre conflits cross-domaines
 │
 └──► CoE ────────────► Maintient le catalogue Collibra, les standards et la formation
       │
       └──► Stewards ──► Garantissent qualité et conformité dans leur domaine
             │
             └──► Head of Engineering ► Implémente les contrôles dans les pipelines

DPO ──────────────────► Valide tous nouveaux traitements (DPIA obligatoire)
 │                       Point de contact CNIL/autorités — 72h breach notification
 ├──► Legal ───────────► Base légale, contrats fournisseurs data, litiges
 └──► Privacy Team ───► Demandes utilisateurs GDPR/CCPA, conformité continue

Marketing Director ───► Garantit que les campagnes respectent CCPA/GDPR
Product Managers ─────► S'assurent que chaque nouvelle feature est privacy-by-design
```

---

## Data Governance Committee

Réunion mensuelle présidée par le CDO :

| Participant | Rôle dans le comité |
|---|---|
| CDO | Président |
| DPO | Conformité & risques réglementaires |
| Head of Engineering | Avancement technique & incidents |
| Marketing Director | Reporting qualité données marketing |
| Legal Team | Veille réglementaire (GDPR, AI Act, etc.) |
| Data Stewards (x5) | Reporting qualité par domaine |
| Product Managers (représentant) | Nouvelles features à valider |

**Ordre du jour type** :
1. Métriques qualité par domaine — Great Expectations (10 min)
2. Incidents data et violations du mois (10 min)
3. Nouveaux traitements à valider (DPIAs) (15 min)
4. Avancement plan d'implémentation (10 min)
5. Audits algorithmes / biais IA (10 min)
6. Décisions & arbitrages (5 min)
