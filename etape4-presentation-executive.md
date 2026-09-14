---
title: "Présentation executive — Spotify Data Governance Framework"
author: "Emeline ROBLOT — Data Governance Specialist"
date: "Septembre 2026"
---

> Source de contenu du deck `livrables/04-presentation-executive.pptx` (généré par `generate_pptx.py`). 9 slides principales + slide « Annexes » + 3 slides de Q&A en annexe. Les notes orateur ci-dessous sont intégrées dans le fichier PowerPoint.

**Format** : 9 slides · **15 minutes de présentation + 15 minutes de questions** (format Jedha).

| # | Slide | Visuel | Temps |
|---|---|---|---|
| 1 | Titre & chiffres clés | — | 1 min |
| 2 | Pourquoi agir maintenant | Radar de maturité | 2 min |
| 3 | Le framework : 3 piliers, 9 principes | Badges | 2 min |
| 4 | Conformité réglementaire | Tableau 4 colonnes | 2 min |
| 5 | Organisation & rôles | Organigramme | 2 min |
| 6 | Plan d'implémentation | Gantt | 2 min |
| 7 | Pilote User Data | Tableau KPIs | 1,5 min |
| 8 | Impact business | Graphique exposition / coût | 1,5 min |
| 9 | 3 décisions à prendre aujourd'hui | — | 1 min |
| A | Annexes : Q&A (3 slides) | — | — |

---

## Slide 1 — Titre

**Data Governance Framework — Spotify**
Qualité · Conformité · Confiance — à l'échelle mondiale

Chiffres : 450 M utilisateurs actifs · 200 M abonnés premium · 180+ pays · Maturité data actuelle **3,4/5** → cible M12 **4,2/5**

*Notes orateur* : « Spotify traite les données de 450 millions de personnes dans 180 pays. Ces données alimentent Discover Weekly, les campagnes marketing, les décisions produit. En 2023, l'autorité suédoise a sanctionné Spotify de 5 millions d'euros sur un sujet de gouvernance, pas de technologie. Je vous propose un framework pour gouverner ces données proactivement, avec un pilote en 4 mois et 3 décisions à prendre aujourd'hui. »

## Slide 2 — Pourquoi agir maintenant ?

**Titre** : 3 signaux d'alarme — et un précédent

- **Risque réglementaire** : GDPR jusqu'à 4 % du CA mondial (≈ 530 M€ sur 13,25 Md€) · notification 72 h · CCPA/CPRA, PDPA, LGPD, DSA. **Précédent : IMY, juin 2023, 58 M SEK (≈ 5 M€) pour un droit d'accès insuffisamment clair.**
- **Silos qui freinent le business** : Marketing, Product, Engineering, Content gèrent leurs propres datasets ; « utilisateur actif » n'a pas la même définition partout ; parcours découverte → premium impossible à reconstituer.
- **Confiance et éthique** : utilisateurs et régulateurs attendent transparence et contrôle ; recommandations non auditées pour les biais (DSA art. 27).

Visuel : radar de maturité (9 dimensions, actuel 3,4 vs cible 4,2). Dimensions critiques : Governance 2/5 · Compliance 3/5 · Quality 3/5.

*Notes orateur* : « Le radar montre un paradoxe : architecture et analytics au niveau 5, gouvernance au niveau 2. Spotify a construit une Formule 1 sans direction de course. Et le précédent de 2023 prouve que le risque est réel : ce n'est pas l'infrastructure qui a été sanctionnée, c'est la clarté de l'information donnée aux utilisateurs. »

## Slide 3 — Le framework : 3 piliers, 9 principes

| Pilier | Principes (Governance Principles Guide) | Ce que ça change |
|---|---|---|
| **Qualité & accessibilité** | Data Quality · Accountability · Continuous Improvement | 5 domaines, 1 steward chacun ; 4 critères mesurés ; catalogue unique ; accès par classification |
| **Conformité & sécurité** | Compliance · Data Security · Data Minimization · User Rights · Transparency | Base légale par finalité ; droits en libre-service ; DPIA ; classification 4 niveaux ; rétention définie |
| **Culture & éthique** | Ethical Use · Continuous Improvement | Formation par rôle ; audit des biais ; explicabilité des recommandations |

*Notes orateur* : « Les 9 principes du guide sont regroupés en 3 piliers pour rester lisibles. La politique tient en 3 pages : objet, principes, qualité, sécurité et accès, conformité, rôles, application. »

## Slide 4 — Conformité réglementaire

| Réglementation | Engagements concrets |
|---|---|
| **GDPR** (UE) | Base légale par finalité · 7 droits couverts (accès, rectification, effacement, portabilité, opposition, limitation, décision automatisée) · réponse < 1 mois · notification 72 h · DPIA · registre art. 30 |
| **CCPA / CPRA** (Californie) | « Do Not Sell or Share » + signal GPC · accès/suppression < 45 j · correction · non-discrimination |
| **PCI-DSS** (paiements) | Prestataire certifié, aucun numéro de carte stocké · SAQ-A annuel · MFA · scans trimestriels · pentest annuel · politique de sécurité |
| **Local & plateformes** | PDPA Singapour · LGPD Brésil · **DSA art. 27** (transparence des recommandations, option non profilée) · AI Act (transparence) |

Outils : OneTrust (consentement, registre, DPIA, demandes) · Splunk (SIEM) · chiffrement Thales/Vormetric · **Compliance Checklist Excel remplie (14 exigences) en annexe**.

*Notes orateur* : « Point d'attention : la recommandation musicale n'est pas "haut risque" au sens de l'AI Act ; l'obligation concrète vient du DSA, article 27 — expliquer la recommandation et offrir une option non fondée sur le profilage. C'est déjà dans le framework. »

## Slide 5 — Organisation & rôles

**Titre** : Centre of Excellence — des responsabilités nommées

Visuel : organigramme (CEO → CDO/CoE/5 Stewards · DPO/Privacy Team · CTO/Head of Engineering/Data Engineers · Legal ; Committee transverse).

Encadré : « La gouvernance définit et audite (CDO, CoE, stewards). L'engineering implémente (CTO). Le DPO est indépendant. »

*Notes orateur* : « Le CoE est le modèle recommandé par le guide et par le cours : Spotify est trop grand et trop distribué pour un modèle centralisé, et le modèle embedded, c'est ce qui existe aujourd'hui et qui produit les silos. La couche de coordination, c'est le Committee mensuel. »

## Slide 6 — Plan d'implémentation

**Titre** : 4 phases · 18 mois · pilote en 4 mois

Visuel : Gantt — Fondations M1-M2 · Pilote User Data M3-M6 · Généralisation M7-M12 (Content → Marketing → Payments → Ads) · Industrialisation M13-M18.

Stack : Collibra ou extension de Lexikon (catalogue) · Great Expectations (qualité) · OneTrust (conformité) · Splunk (SIEM) · Thales/Vormetric (chiffrement) · OpenLineage (lineage) · Monte Carlo (observabilité, phase 4).

*Notes orateur* : « Calendrier aligné sur le Q&A guide : pilote 3 à 6 mois, puis 12 mois de déploiement. Spotify a déjà Lexikon, un catalogue interne adopté par 95 % des data scientists : la phase 1 audite l'existant avant tout achat. On n'achète pas un outil pour remplacer ce qui marche, on ajoute la couche stewardship et policy. »

## Slide 7 — Pilote User Data (M3-M6)

**Pourquoi User Data** : exposition GDPR maximale · données pouvant révéler des informations sensibles inférées · alimente Discover Weekly et la rétention premium. **Périmètre borné** : profils et historiques d'écoute, marchés UE d'abord.

| KPI (Pilot Template) | Cible M6 |
|---|---|
| Data Quality Score | -10 % de données manquantes (complétude > 98 %) |
| Compliance Score | 100 % des traitements avec base légale et consentement valide |
| Data Access Speed | -20 % de délai d'accès aux données |
| Risk Mitigation Score | 100 % des datasets classifiés et chiffrés · 0 incident |
| Droits des personnes | Effacement < 30 j, 100 % dans les délais |

Go/No-Go par le Committee en M6. Livrables : Data Quality Report · Compliance Assessment · Technical Integration Plan · Risk Assessment · Stakeholder Feedback.

*Notes orateur* : « Toutes les baselines sont mesurées en semaine 1. Un KPI sans baseline n'est pas un KPI. Le périmètre UE permet d'être réaliste en 4 mois et de traiter d'abord la juridiction qui nous a déjà sanctionnés. »

## Slide 8 — Impact business

**Titre** : 6-7 M€ pour couvrir 530 M€ d'exposition

Visuel : barres — exposition max GDPR ≈ 530 M€ · sanction 2023 ≈ 5 M€ · coût programme 18 mois ≈ 6-7 M€ · gain d'efficacité ≈ 3 M€/an (hyp.).

| Dimension (Q&A Q3) | Bénéfice |
|---|---|
| Compliance | Réduction du risque d'amende (jusqu'à 4 % du CA) ; pas de récidive IMY |
| Cost savings | -20 % de temps d'accès aux données ≈ 25 ETP libérés (hyp. 500 analystes × 2 h/sem.) |
| Trust | Transparence et contrôle → rétention sur les marchés UE ; différenciation vs Apple/Amazon/YouTube |
| Scalability | Un framework qui absorbe la croissance (450 M → 600 M+ utilisateurs) et les nouvelles réglementations |

*Notes orateur* : « Les chiffres de coût sont des ordres de grandeur à affiner en phase 1, je les assume comme hypothèses. Mais l'ordre de grandeur suffit : le programme coûte environ 1 % de l'exposition maximale, et à peine plus que l'amende déjà payée. »

## Slide 9 — 3 décisions à prendre aujourd'hui

1. **Nommer le CDO** — prérequis bloquant de tout le plan. Action : profil validé et nomination sous 30 jours.
2. **Approuver le budget phases 1-2** (≈ 2,5 M€ sur 6 mois : équipe CoE + Privacy Team, OneTrust, catalogue pilote). Action : décision budgétaire ce trimestre.
3. **Lancer la communication interne** — la résistance au changement est le risque n°1. Action : message CEO + webinar CDO en M1.

*Notes orateur* : « Je ne vous demande pas de valider 18 mois aujourd'hui. Je vous demande un CDO, 6 mois de budget et un message au personnel. Le pilote fera la preuve. »

---

## Annexes — Q&A

### Les 12 questions de l'Executive Q&A Guide

**Q1 — Pourquoi maintenant ?** 450 M d'utilisateurs, 180 pays, exigences GDPR/CCPA/DSA croissantes, sanction IMY 2023, silos qui freinent l'innovation. Attendre, c'est laisser le risque et l'inefficacité croître avec l'échelle.

**Q2 — Impact sur les opérations existantes ?** Le framework s'appuie sur l'existant (GCP, Airflow, Lexikon). Il ajoute des standards, des owners et des mesures, pas une nouvelle plateforme. Impact court terme : temps des stewards et formation ; long terme : moins de doublons, données plus fiables, conformité fluide.

**Q3 — Valeur business ?** Compliance (risque jusqu'à 530 M€), cost savings (temps d'accès aux données, moins de retraitements), trust (rétention), scalability. Coût ≈ 6-7 M€ sur 18 mois.

**Q4 — Comment garantir la conformité GDPR/CCPA ?** Base légale documentée par finalité, consentement granulaire (OneTrust), 7 droits couverts avec SLA, Privacy Team, DPO indépendant, DPIA avant tout traitement à risque, registre art. 30, checklist tenue à jour.

**Q5 — Pourquoi le CoE ?** Centralisé = goulot d'étranglement pour 180 pays ; embedded = les silos actuels. Le CoE combine standards communs et relais métier ; c'est le modèle du guide et du cours pour une entreprise de cette taille.

**Q6 — Comment mesurer le succès ?** KPIs avec baselines : complétude > 98 %, 100 % des demandes dans les délais légaux, -20 % de délai d'accès, 0 incident critique, 100 % du catalogue couvert, > 90 % formés, maturité 3,4 → 4,2.

**Q7 — Combien de temps ?** Pilote 4 mois (M3-M6), déploiement 12 mois, mode opérationnel à M18. Conforme au guide (pilote 3-6 mois, rollout 12-18 mois).

**Q8 — Quels coûts ?** Personnel ≈ 1,9 M€, licences ≈ 3 M€, intégration 0,5-1 M€, formation 0,3 M€ → ≈ 6-7 M€ sur 18 mois. Phases 1-2 ≈ 2,5 M€. Ordres de grandeur à affiner en phase 1.

**Q9 — Adaptation aux évolutions réglementaires ?** Veille DPO + Legal, revue annuelle de la politique, checklist trimestrielle, outils multi-juridictions ; DSA et AI Act déjà intégrés.

**Q10 — Sécurité des données sensibles ?** Classification 4 niveaux, chiffrement au repos et en transit, accès nominatif minimal et journalisé pour la classe Sensible, SIEM, PCI-DSS via prestataire certifié + SAQ-A, protocole d'incident 72 h testé annuellement.

**Q11 — Risques principaux ?** Résistance au changement (ateliers, stewards issus des équipes, quick wins) ; délais (phases bornées, Go/No-Go) ; coûts (budget par phase, licences négociées après audit de l'existant).

**Q12 — Impact sur l'agilité ?** Positif : données trouvables et fiables = décisions plus rapides ; privacy by design dès les sprints = moins d'audits correctifs. La gouvernance enlève de la friction, elle n'en ajoute pas.

### 6 questions difficiles hors guide

**« Spotify a déjà un DPO et une plateforme data de pointe : pourquoi Governance 2/5 ? »** Le niveau 2 mesure la gouvernance transverse, pas la technologie : pas de CDO, pas d'ownership par domaine, définitions divergentes, et une sanction 2023 sur la clarté de l'information. L'architecture est à 5, c'est justement le paradoxe.

**« Pourquoi pas un data mesh, vu la culture squads ? »** Le data mesh est compatible avec le CoE : les stewards par domaine sont les « domain owners » du mesh, le CoE fournit la plateforme et les standards fédérés. Le CoE est le nom du cours pour la couche de gouvernance fédérée du mesh.

**« 5 stewards pour 180 pays, c'est suffisant ? »** 5 stewards par domaine de données, pas par pays. Les spécificités locales (PDPA, LGPD) sont portées par le DPO et Legal ; les stewards s'appuient sur des relais dans les équipes régionales en phase 3.

**« Quelle base légale pour la recommandation : consentement ou intérêt légitime ? »** Contrat ou intérêt légitime pour la personnalisation du service, avec option non profilée (DSA art. 27) ; consentement uniquement pour la publicité ciblée et le partage à des tiers. Le consentement pour tout serait ni exigé ni tenable.

**« Que faites-vous des données inférées sensibles ? »** Interdiction de profiler sur des catégories art. 9 inférées (humeur, religion, orientation), classification « Sensible » avec DPIA, audit des biais trimestriel.

**« Combien ça coûte et qu'est-ce qui se passe si le pilote échoue ? »** ≈ 2,5 M€ pour les phases 1-2. Si le Go/No-Go est négatif, on a quand même un catalogue User Data, une baseline de qualité, un pipeline de droits testé et une équipe formée : le coût n'est pas perdu, le plan est ajusté.

### Réponses clés en anglais (si le jury bascule)

- *Why now?* — 450M users across 180 countries, GDPR fines up to 4% of global revenue, and Spotify was already fined SEK 58M in 2023 for an unclear right of access. Silos slow innovation. The cost of waiting grows with scale.
- *Why a CoE?* — Centralized creates bottlenecks; embedded is what exists today and produces silos. The CoE keeps common standards with stewards embedded in each business unit.
- *Business value?* — Program cost ≈ €6-7M over 18 months versus a maximum GDPR exposure of ≈ €530M, plus efficiency gains from faster data access and user trust.
- *How do you measure success?* — Baselined KPIs: completeness above 98%, 100% of data subject requests within legal deadlines, 20% faster data access, zero critical incidents, maturity score from 3.4 to 4.2.
