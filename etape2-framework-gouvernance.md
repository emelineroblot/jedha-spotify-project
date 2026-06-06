# Étape 2 — Framework de Data Governance : Spotify

**Auteur** : Data Governance Specialist  
**Date** : Mai 2026  
**Version** : 3.0 (intégration Governance Principles Guide + Tech Tools Overview officiels)

---

## 1. Les 9 principes fondateurs (Governance Principles Guide officiel)

| # | Principe | Description | Action concrète chez Spotify |
|---|---|---|---|
| 1 | **Accountability** | Responsabilité claire sur tous les processus data | Désigner Data Stewards et DPO avec fiches de rôle signées |
| 2 | **Transparency** | Toutes les activités de traitement sont transparentes pour les utilisateurs | Privacy notices détaillées, consentement OneTrust sur 180 pays |
| 3 | **Data Security** | Les données sensibles sont chiffrées et protégées selon les plus hauts standards | Chiffrement AES-256, contrôle d'accès RBAC, Splunk SIEM, PCI-DSS via Stripe |
| 4 | **Data Quality** | Les données sont exactes, complètes et fiables | Métriques qualité + audits réguliers via Great Expectations ou Talend |
| 5 | **Compliance** | Conformité avec GDPR, CCPA, PCI-DSS et réglementations locales | Revues de conformité trimestrielles, DPIAs systématiques |
| 6 | **Data Minimization** | Ne collecter que les données nécessaires aux finalités définies | Politiques strictes de collecte, revue annuelle des datasets |
| 7 | **User Rights** | Respecter et faciliter l'exercice des droits des utilisateurs | Pipeline d'effacement <30j, portabilité, opt-out CCPA, Privacy Team dédiée |
| 8 | **Continuous Improvement** | Le framework évolue avec les réglementations, la technologie et les besoins | Révision annuelle du framework, feedback du Governance Committee |
| 9 | **Ethical Use** | Usage éthique des données et des systèmes d'IA | Audits trimestriels des biais algorithmiques, conformité EU AI Act |

---

## 2. Pilier 1 — Qualité des données

### 2.1 Domaines de données et ownership

| Domaine | Données concernées | Data Steward | Criticité |
|---|---|---|---|
| **User Data** | Profils, historiques d'écoute (titres joués, skips, recherches), playlists, localisation, démographie | Data Steward User | Très haute — GDPR + recommandation |
| **Content** | Métadonnées musicales (ISRC, artiste, genre, droits), podcasts (Anchor, Gimlet, Parcast) | Data Steward Content | Haute — qualité recommandation + royalties |
| **Payments** | Abonnements premium, transactions, historique de facturation (PCI-DSS via Stripe) | Data Steward Payments | Très haute — PCI-DSS |
| **Ads** | Campagnes, ciblage, impressions, conversions, segments utilisateurs | Data Steward Ads | Haute — CCPA opt-out |
| **Marketing** | Engagement campagnes, segmentation, métriques conversion free→premium | Data Steward Marketing | Haute — stratégie croissance |

### 2.2 Règles de qualité (4 critères officiels)

| Critère | Définition | Cible | Outil de mesure |
|---|---|---|---|
| **Complétude** | Absence de champs obligatoires vides | >98% | Great Expectations / Talend |
| **Exactitude** | Conformité aux valeurs attendues (ex. ISRC valide) | >99% | Informatica Data Quality |
| **Cohérence** | Même définition d'une métrique sur tous les systèmes | 100% | Collibra (business glossary) |
| **Fraîcheur** | Délai max entre production et disponibilité | <1h temps réel | Monte Carlo / Ataccama ONE |

### 2.3 Stack outils — Data Quality (Tech Tools Overview officiel)

| Outil | Usage | Positionnement |
|---|---|---|
| **Talend** | Data integration, cleansing, déduplication | Principal — intégration GCP |
| **Informatica Data Quality** | Profiling, cleansing, matching temps réel | Complémentaire — domaine Content |
| **Ataccama ONE** | AI-powered data profiling, gouvernance automatisée | Avancé — scalabilité |
| **Great Expectations** | Tests qualité dans les pipelines CI/CD (Airflow) | Open source — intégration existante |

---

## 3. Pilier 2 — Sécurité et conformité réglementaire

### 3.1 GDPR (Union Européenne) — Risque : 20 M€ ou 4% du CA mondial

| Exigence | Mise en œuvre | Responsable |
|---|---|---|
| Base légale (consentement) | Consentement explicite via OneTrust à l'inscription | DPO + Legal |
| Droit à l'effacement | Pipeline automatisé déclenché sous **30 jours** | Engineering + DPO |
| Droit à la portabilité | Export JSON/CSV depuis les paramètres du compte | Engineering |
| Notification violation | Signalement autorités sous **72 heures** | DPO + Legal |
| Privacy by design | Pseudonymisation dans les pipelines analytiques, data minimization | Data Engineers |
| DPIA | Obligatoire avant tout nouveau traitement à risque élevé | DPO |

### 3.2 CCPA (Californie)

| Exigence | Mise en œuvre |
|---|---|
| Opt-out | Lien "Do Not Sell My Personal Information" visible sur site et app |
| Droit d'accès | Réponse sous 45 jours (Privacy Team dédiée) |
| Non-discrimination | Aucun service dégradé pour les utilisateurs ayant exercé leurs droits |

### 3.3 PCI-DSS

Données de paiement traitées exclusivement par Stripe (certifié PCI-DSS). Obligations Spotify : TLS 1.2+, audit annuel, logs d'accès 12 mois minimum.

### 3.4 Réglementations régionales

| Pays | Réglementation | Point de vigilance |
|---|---|---|
| UE | GDPR | Transferts hors UE (clauses contractuelles types) |
| USA/CA | CCPA | Opt-out publicité ciblée |
| Singapour | PDPA | Consentement + notification violations |
| Brésil | LGPD | Base légale explicite, amende 2% CA Brésil |

### 3.5 Stack outils — Compliance (Tech Tools Overview officiel)

| Outil | Usage |
|---|---|
| **OneTrust** | Gestion consentements (180 pays), data mapping, DPIAs, reporting GDPR/CCPA |
| **TrustArc** | Inventaire des données, gestion complémentaire de la conformité |
| **VeraSafe** | Audits de conformité GDPR/CCPA, gestion des incidents |

### 3.6 Stack outils — Data Security (Tech Tools Overview officiel)

| Outil | Usage |
|---|---|
| **Splunk** | SIEM — visibilité temps réel sur les risques et incidents de sécurité |
| **DataGuard** | Automation de la protection des données, reporting GDPR/CCPA |
| **Vormetric** | Chiffrement des données sensibles dans les bases, fichiers et applications |

### 3.7 Classification des données

| Classe | Exemples Spotify | Protection |
|---|---|---|
| Publique | Métadonnées musicales catalogue | Aucune restriction |
| Interne | Métriques business, rapports campagnes | Accès employés uniquement |
| Confidentielle | Historiques d'écoute, comportements utilisateurs | Chiffrement AES-256, RBAC |
| Sensible | Paiements, données révélant opinions/santé implicite | Chiffrement renforcé (Vormetric), accès minimal, logs Splunk obligatoires |

### 3.8 Éthique algorithmique (Principe 9 — Ethical Use)

Conformément au Governance Principles Guide et à l'EU AI Act :
- Audits trimestriels des biais du moteur de recommandation (Discover Weekly, Daily Mix)
- Explicabilité des recommandations disponible sur demande utilisateur
- Lignes directrices éthiques intégrées à tous les projets de développement IA
- Surveillance des systèmes de décision automatisée pour prévenir les discriminations

---

## 4. Pilier 3 — Rôles et responsabilités

### 4.1 Rôles officiels (Data Governance Roles Template)

**Data Steward** (×5 — un par domaine)
- Garantir l'exactitude, la cohérence et la fiabilité des données du domaine
- Collaborer avec les équipes techniques pour implémenter les améliorations qualité
- Faire respecter les politiques de gouvernance et gérer les accès données

**Data Protection Officer (DPO)**
- Assurer la conformité avec GDPR, CCPA et toutes réglementations applicables
- Point de contact avec les autorités de protection des données (CNIL, etc.)
- Conseiller sur les DPIAs
- Superviser les processus de réponse aux violations et de notification

**Chief Data Officer (CDO)**
- Diriger la stratégie de gouvernance data de Spotify
- Définir les politiques data et s'assurer de leur application
- Aligner la gouvernance avec les priorités business (CEO, Board)
- Piloter le Data Governance CoE

**Data Governance Committee** (mensuel)
- Réviser et approuver les politiques et processus data
- Traiter les challenges de gouvernance cross-départementaux
- Assurer l'alignement avec les objectifs légaux, de conformité et opérationnels

### 4.2 Parties prenantes étendues

| Rôle | Responsabilité dans la gouvernance |
|---|---|
| **Head of Engineering** | Infrastructure data, sécurité technique, pipelines, scalabilité GCP |
| **Marketing Director** | Conformité des pratiques marketing, qualité données campagnes |
| **Legal Team** | Validation juridique des politiques, gestion des risques légaux |
| **Product Managers** | Privacy by design sur chaque nouvelle feature |

### 4.3 Matrice RACI

| Activité | CDO | DPO | Head Eng. | Mktg Dir. | Legal | PM | Steward | Engineer |
|---|---|---|---|---|---|---|---|---|
| Définir la politique de gouvernance | R | C | C | C | C | I | C | I |
| Valider les traitements / DPIAs | I | R | I | C | C | I | C | I |
| Garantir la qualité par domaine | C | I | C | C | I | C | R | C |
| Implémenter pipelines & sécurité | I | I | R | I | I | I | C | R |
| Traiter demandes utilisateurs GDPR | I | R | C | I | C | I | C | C |
| Audits algorithmes / biais IA | C | C | R | I | C | C | C | R |
| Formation & culture data | R | C | C | C | I | C | C | I |
| Répondre aux incidents data | R | C | R | I | C | I | C | R |

*R = Responsable, C = Consulté, I = Informé*

---

## 5. Pilier transversal — Culture data et formation (Principe 8)

Conformément au Governance Principles Guide (Continuous Improvement) :
- **Programme de formation par rôle** : DPO → conformité GDPR/CCPA ; CoE → qualité data ; Product → privacy by design
- **Data Governance Committee mensuel** : CDO + DPO + Head of Engineering + Marketing Director + Legal + 5 Stewards + représentant Product
- **Privacy Team dédiée** (rattachée au DPO) : 1 DPO + 2 Privacy Analysts pour traiter les demandes utilisateurs dans les délais légaux
- **Newsletter data mensuelle** : métriques qualité, incidents, veille réglementaire
- **Revue annuelle du framework** : intégration des nouvelles réglementations et feedbacks terrain

---

## 6. Stack catalogue — Data Cataloging (Tech Tools Overview officiel)

| Outil | Usage | Recommandation |
|---|---|---|
| **Collibra** | Data stewardship, cataloging, qualité — interface métier | **Retenu** — meilleure intégration GCP et interface non-tech |
| **Alation** | Data discovery, collaboration, catalogue | Alternative si budget contraint |
| **Apache Atlas** | Open source, tracking et cataloging metadata | Backup open source |

---

## 7. Synthèse du framework

```
┌──────────────────────────────────────────────────────────────────┐
│              DATA GOVERNANCE FRAMEWORK — SPOTIFY v3.0            │
├──────────────┬───────────────────┬────────────┬──────────────────┤
│  QUALITÉ     │   CONFORMITÉ      │   RÔLES    │  CULTURE         │
│              │                   │            │                  │
│ 5 domaines   │ GDPR 20M€ max     │ CDO        │ 9 principes      │
│ 4 critères   │ CCPA · PCI-DSS    │ DPO        │ Formation rôles  │
│ Talend       │ PDPA · LGPD       │ 5 Stewards │ Committee mensuel│
│ Informatica  │ EU AI Act         │ Head Eng.  │ Privacy Team     │
│ Great Exp.   │ OneTrust          │ Legal      │ Révision annuelle│
│              │ Splunk · Vormetric│ Product    │                  │
└──────────────┴───────────────────┴────────────┴──────────────────┘
```

Déploiement prioritaire sur le domaine **User Data** (voir Étape 3 — Plan d'implémentation).
