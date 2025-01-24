### TODO :

#### **BUILD**

- une balise peut être passée en paramètre d'une autre balise
- gestion des dépendences

---

#### **Tests**

#### 1. **Créer un buffer pour GPT**

- Mettre en place un mécanisme de buffer pour gérer les interactions avec GPT.
- Permettre d'accumuler et de traiter les données en lot pour améliorer l'efficacité et réduire les appels redondants.

#### 2. **Implémenter un contrôle de débit (rate limit)**

- Ajouter une gestion de débit pour limiter le nombre de requêtes ou d'appels simultanés à GPT.
- S'assurer que les limites imposées par l'API sont respectées tout en maintenant des performances optimales.

#### 3. **Créer un GPT spécifique qui fournit les fichiers de sortie**

- Développer un flux où GPT génère directement les fichiers de sortie basés sur les spécifications données.
- **Définir un exemple d'output** : Proposer un exemple clair et documenté du résultat attendu, aligné sur le template.

#### 4. **Créer un template de test automatique**

- **Générer un test automatique** : Automatiser la création de tests unitaires pour valider les templates.
- Développer un template générique (Jinja2) pour générer des fichiers de tests récursifs automatisés en fonction des spécifications XML.

#### 5. **Lancer les tests avec des fichiers cibles vides**

- Préparer des tests unitaires ou d'intégration avec des fichiers cibles (outputs) initialement vides.
- Vérifier que les fichiers sont générés correctement après l'exécution des tests.

#### 6. **Créer un GPT spécifique qui génère les templates Jinja**

- Mettre en place un pipeline où GPT produit automatiquement des templates Jinja adaptés aux besoins des fichiers XML ou de la logique métier.
- **Valider les templates générés** avec des exemples concrets.

#### 7. **Récupérer les erreurs**

- Mettre en place un mécanisme pour détecter et capturer les erreurs lors de la génération ou de l'exécution des tests.
- Générer des rapports détaillés sur les erreurs détectées, y compris leur contexte (données d'entrée, output attendu).

#### 8. **Mettre à jour les fichiers Jinja**

- Modifier automatiquement ou semi-automatiquement les templates Jinja pour corriger les erreurs détectées.
- Adapter les templates aux changements de spécifications ou aux nouvelles contraintes détectées.

---

#### **5. Auto-correction des erreurs**

- **Réfléchir à la récupération des erreurs** : Détecter et capturer les erreurs dans les templates ou les fichiers générés.
- **Ajouter les fichiers concernés par l'erreur au contexte du prompt** : Inclure les informations pertinentes dans les messages ou les prompts pour faciliter les corrections.
- **Mettre à jour les templates pour corriger les erreurs** : Modifier automatiquement ou semi-automatiquement les templates pour résoudre les problèmes identifiés.

---

#### **6. Ordre de conception**

- **Créer un graphe orienté acyclique des dépendances entre les balises** : Modéliser les relations entre les balises XML pour identifier les dépendances.
- **Commencer par les tests, qui sont des nœuds terminaux** : Prioriser les tests, car ils n'ont pas de dépendances en aval et valident les fonctionnalités de manière isolée.

#### création d'une CI / CD

- compiler le fichier xml
- générer l'arboraissance yaml
- build le docker compose
- deploy le docker compose
