# Étape 1 — Data Maturity Assessment : Spotify

**Auteur** : Data Governance Specialist  
**Date** : Mai 2026  
**Périmètre** : Opérations data globales de Spotify  
**Méthodologie** : 9 dimensions officielles (Data Maturity Assessment Template)

---

## 1. Niveau de maturité global

### Échelle de référence (1-5)

| Niveau | Label |
|---|---|
| 1 | Initial — données non structurées, aucun processus |
| 2 | Géré — processus locaux, silos forts |
| 3 | Défini — standards communs, gouvernance partielle |
| 4 | **Optimisé — data-driven, amélioration continue** |
| 5 | Innovant — IA/ML au cœur de chaque décision |

### Verdict global : **Niveau 3,8 — entre Défini et Optimisé**

Spotify est une entreprise data-driven mature (**450 millions d'utilisateurs actifs**, **200 millions d'abonnés premium**, présence dans **180+ pays**) avec une infrastructure sophistiquée (data lakes, GCP, pipelines temps réel Kafka/Dataflow). Cependant, les lacunes en gouvernance formelle, data literacy transversale et intégration inter-domaines maintiennent Spotify sous le niveau 4 sur plusieurs dimensions critiques.

---

## 2. Évaluation par dimension (9 dimensions officielles)

| Dimension | Niveau (1-5) | Forces | Faiblesses | Plan d'action |
|---|---|---|---|---|
| **Data Governance** | 2 | Conscience du besoin, DPO en place | Pas de CDO, pas de CoE, ownership flou entre départements | Nommer le CDO, constituer le CoE, désigner 5 Data Stewards |
| **Data Quality** | 3 | Pipelines de validation sur certains flux | Métadonnées musicales incomplètes (~30% d'ISRC manquants), définitions de métriques incohérentes | Déployer Great Expectations, définir 4 critères qualité par domaine |
| **Data Architecture** | 5 | GCP, Kafka, Dataflow, data lakes, traitement temps réel | Quelques systèmes legacy sur podcasts (Anchor, Gimlet) | Étendre les pipelines standardisés aux acquisitions récentes |
| **Compliance (GDPR, CCPA…)** | 3 | DPO présent, politiques de base existantes | Pas de DPIA systématique, pipeline d'effacement GDPR non automatisé, PDPA/LGPD non couverts | Automatiser pipeline effacement <30j, DPIAs systématiques, OneTrust multi-juridictions |
| **Data Usage & Accessibility** | 3 | Culture A/B testing, accès data pour les squads | Silos entre Marketing, Product, Engineering et Content — pas de catalogue commun | Déployer Collibra/Alation, briser les silos via le CoE |
| **Data Security** | 4 | Chiffrement en transit (TLS 1.2+), contrôle d'accès, délégation PCI-DSS à Stripe | Pas de SIEM centralisé (Splunk), classification des données sensibles incomplète | Déployer Splunk, formaliser la classification (Publique/Interne/Confidentielle/Sensible) |
| **Data Literacy** | 3 | Culture data forte dans les squads produit | Faible maîtrise des principes de gouvernance et conformité dans les équipes non-tech (Marketing, Legal) | Programme de formation par rôle (DPO pour conformité, CoE pour qualité) |
| **Data Integration** | 3 | Airflow, pipelines inter-systèmes opérationnels | Intégration incomplète des données podcasts post-acquisition, pas de data lineage end-to-end | Déployer OpenLineage + Marquez, standardiser les pipelines Anchor/Gimlet/Parcast |
| **Analytics & BI** | 5 | Moteur de recommandation ML avancé (Discover Weekly, Daily Mix), A/B testing massif | Biais algorithmiques non audités, explicabilité des modèles insuffisante | Audits trimestriels des biais, contrôles EU AI Act |

---

## 3. Radar de maturité

```
Data Governance      ██░░░░░░░░  2/5
Data Quality         ███░░░░░░░  3/5
Data Architecture    █████████░  5/5  ✓ Point fort
Compliance           ███░░░░░░░  3/5
Data Usage & Access  ███░░░░░░░  3/5
Data Security        ████░░░░░░  4/5
Data Literacy        ███░░░░░░░  3/5
Data Integration     ███░░░░░░░  3/5
Analytics & BI       █████████░  5/5  ✓ Point fort
```

**Score global : 3,4/5** — Spotify est solide sur l'infrastructure et l'analytics, mais fragile sur la gouvernance formelle, la conformité multi-juridictions et la data literacy.

---

## 4. Challenges prioritaires identifiés

### Challenge 1 — Gouvernance sans structure (priorité URGENTE)
Pas de CDO, pas de CoE, ownership des données flou. Les décisions sont prises département par département sans vision transversale. La définition d'"utilisateur actif" diffère entre Marketing et Product — symptôme direct d'une absence de gouvernance.

### Challenge 2 — Conformité multi-juridictions (priorité URGENTE)
Spotify est exposé simultanément au GDPR (**amende jusqu'à 20 M€ ou 4% du CA mondial**, notification violation sous **72 heures**), CCPA, PDPA Singapour et LGPD Brésil. Aucun pipeline d'effacement automatisé. Pas de DPIA systématique sur les nouveaux traitements.

### Challenge 3 — Qualité des métadonnées (priorité HAUTE)
Les données de contenu issues des labels et distributeurs indépendants sont incomplètes. Des ISRC manquants ou erronés impactent la précision des recommandations et la distribution des royalties.

### Challenge 4 — Silos inter-départements (priorité HAUTE)
Marketing, Product, Engineering et Content gèrent des datasets séparés. Comprendre le parcours complet d'un utilisateur (découverte → conversion premium) nécessite de croiser des données aujourd'hui inaccessibles en temps réel. Cela freine le développement de nouvelles features et nuit à la qualité analytique.

### Challenge 5 — Éthique algorithmique (priorité HAUTE)
Le moteur de recommandation (Discover Weekly, Daily Mix) n'est pas audité pour les biais. Avec l'EU AI Act en vigueur, l'explicabilité et la non-discrimination des modèles ML deviennent des obligations légales.

---

## 5. Synthèse et recommandations

| Dimension | Niveau actuel | Niveau cible (M12) | Priorité |
|---|---|---|---|
| Data Governance | 2 | 4 | **Urgente** |
| Data Quality | 3 | 4 | Haute |
| Data Architecture | 5 | 5 | Maintenir |
| Compliance | 3 | 5 | **Urgente** |
| Data Usage & Accessibility | 3 | 4 | Haute |
| Data Security | 4 | 5 | Moyenne |
| Data Literacy | 3 | 4 | Haute |
| Data Integration | 3 | 4 | Moyenne |
| Analytics & BI | 5 | 5 | Maintenir + Audits biais |

Ce rapport constitue le point de départ du framework de Data Governance (Étape 2). Les trois dimensions les plus urgentes — **Governance, Compliance et Data Quality** — sont adressées en priorité dans le plan d'implémentation.
