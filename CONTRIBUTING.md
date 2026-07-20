# Guide de contribution

Merci de vouloir contribuer au projet. Ce document explique comment proposer une modification de façon efficace, respectueuse du temps des mainteneurs et juridiquement claire.

Les contributions techniques et non techniques sont bienvenues : code, tests, documentation, design, accessibilité, traduction, tri de tickets, reproduction de bogues, amélioration d’exemples et accompagnement de nouvelles personnes.

## Principes de contribution

Les contributions doivent viser :

- la clarté plutôt que l’astuce ;
- la maintenabilité plutôt que la vitesse immédiate ;
- la discussion publique plutôt que les décisions implicites ;
- des changements petits, testables et réversibles ;
- le respect de la gouvernance, du code de conduite et du DCO.


## Parcours de contribution

Le projet reconnaît plusieurs parcours de contribution. Il n’est pas nécessaire d’être développeur ou développeuse pour participer utilement.

### Première contribution recommandée

Pour une première participation, choisir idéalement un ticket étiqueté :

- `good first issue` ;
- `documentation` ;
- `test` ;
- `triage` ;
- `help wanted`.

Avant de commencer, laisser un court commentaire sur le ticket afin d’éviter le travail en double.

### Contribution documentaire

Une contribution documentaire peut corriger une coquille, clarifier une procédure, ajouter une capture, traduire une page ou rendre un exemple plus facile à suivre. Ces contributions sont pleinement reconnues.

### Contribution de tri

Le tri consiste à reproduire les bogues, demander les informations manquantes, repérer les doublons, proposer des étiquettes ou transformer une demande vague en problème actionnable. C’est une contribution essentielle à la santé du projet.

### Contribution de conception

Les propositions de conception doivent expliquer le problème à résoudre avant la solution. Les changements importants devraient être discutés dans un ticket ou une discussion avant une grosse demande de tirage.

## Étapes rapides

### 1. Créer un fork ou une branche

```bash
git clone https://example.org/organisation/nom-du-projet.git
cd nom-du-projet
git checkout -b feat/description-courte
```

### 2. Préparer un environnement local isolé

Utiliser le mécanisme d’isolation recommandé par la pile technique du projet.

Exemples conceptuels :

```bash
make setup
```

ou :

```bash
./scripts/setup
```

ou encore le gestionnaire de dépendances officiel du projet.

L’environnement local ne doit pas dépendre d’une configuration globale fragile ou non documentée.

### 3. Exécuter la suite de tests

Avant toute modification :

```bash
make test
make lint
make check
```

Après modification, relancer les mêmes vérifications. Une demande de tirage ne devrait pas être soumise si les tests échouent sans explication.

### 4. Commiter avec signature DCO

Tous les commits doivent être signés avec `Signed-off-by` :

```bash
git commit -s -m "feat: ajouter une validation du format de projet"
```

L’option `-s` ajoute automatiquement une ligne semblable à :

```text
Signed-off-by: Prénom Nom <courriel@example.org>
```

### 5. Ouvrir une demande de tirage

La demande de tirage doit :

- expliquer le problème résolu ;
- décrire la solution ;
- mentionner les tests exécutés ;
- signaler les risques ou limites ;
- lier le ticket concerné, s’il existe.

## Developer Certificate of Origin

Le projet utilise le **Developer Certificate of Origin** plutôt qu’un CLA corporatif.

En ajoutant une ligne `Signed-off-by`, vous certifiez que :

1. vous avez créé la contribution vous-même ; ou
2. vous avez le droit de la soumettre selon la licence open source du projet ; ou
3. la contribution provient d’une source compatible avec cette licence ; et
4. vous acceptez que la contribution et la ligne de signature soient conservées publiquement dans l’historique du projet.

Aucune contribution ne sera intégrée sans signature DCO valide.

Pour signer le dernier commit oublié :

```bash
git commit --amend -s --no-edit
```

Pour re-signer plusieurs commits, utiliser un rebase interactif avec prudence :

```bash
git rebase -i origin/main
```

## Normes de qualité du code

### Lisibilité

- Utiliser des noms explicites pour les variables, fonctions, classes, modules et fichiers.
- Éviter les abréviations obscures.
- Préférer de petites unités cohérentes à de longs blocs multifonctions.
- Documenter les décisions non évidentes, pas les évidences.

### Modularité

- Séparer les responsabilités : interface, logique métier, accès disque, réseau, sécurité, configuration.
- Éviter les dépendances circulaires.
- Favoriser des interfaces stables et testables.
- Minimiser l’état global mutable.

### Tests

Toute nouvelle fonctionnalité doit inclure des tests pertinents :

- tests unitaires pour la logique isolée ;
- tests d’intégration pour les interactions entre composants ;
- tests de non-régression pour les bogues corrigés ;
- exemples reproductibles lorsque le comportement est subtil.

Un changement qui réduit la couverture ou retire un test doit expliquer pourquoi.

### Erreurs et diagnostics

- Les erreurs doivent être compréhensibles par une personne utilisatrice.
- Les journaux doivent aider à diagnostiquer sans exposer de secrets.
- Les exceptions ou erreurs système ne doivent pas être avalées silencieusement.

### Sécurité

- Ne jamais commiter de secrets, jetons, mots de passe ou clés privées.
- Ne pas publier de preuve d’exploitation critique dans un ticket public.
- Suivre `SECURITY.md` pour toute vulnérabilité.

## Conventions de branches

Branches recommandées :

```text
main                  # branche stable ou intégrable
feat/sujet-court      # nouvelle fonctionnalité
fix/sujet-court       # correction de bogue
docs/sujet-court      # documentation
refactor/sujet-court  # refactorisation sans changement fonctionnel
test/sujet-court      # tests uniquement
chore/sujet-court     # maintenance, outillage, configuration
```

Les branches doivent rester courtes et ciblées. Une grosse modification doit être découpée en plusieurs demandes de tirage si possible.

## Messages de commit

Le projet suit le style **Conventional Commits**.

Format :

```text
type(scope optionnel): description courte

Corps optionnel expliquant le pourquoi.

Signed-off-by: Prénom Nom <courriel@example.org>
```

Types usuels :

```text
feat      # nouvelle fonctionnalité
fix       # correction de bogue
docs      # documentation
style     # formatage sans changement logique
refactor  # changement interne sans nouvelle fonctionnalité
perf      # performance
test      # tests
build     # système de build ou dépendances
ci        # intégration continue
chore     # maintenance courante
security  # correction liée à la sécurité
```

Exemples :

```text
feat(config): ajouter la résolution des chemins externes
fix(parser): refuser les fichiers de projet incomplets
docs(readme): clarifier le démarrage rapide
test(generator): couvrir les métriques asymétriques
```

## Demandes de tirage

Une demande de tirage doit être prête à examiner :

- changement limité et cohérent ;
- description claire ;
- tests ajoutés ou justification de leur absence ;
- documentation mise à jour si nécessaire ;
- aucun fichier généré inutile ;
- aucune information sensible.

Les mainteneurs peuvent demander des modifications. Les commentaires de revue doivent porter sur le code, la conception, la sécurité, la documentation ou la maintenabilité, jamais sur la personne.

## Contributions non techniques

Les contributions non techniques ont la même valeur communautaire que le code. Sont notamment utiles :

- améliorer la documentation utilisateur ;
- corriger la terminologie ;
- traduire des documents ;
- reproduire et clarifier des bogues ;
- trier des tickets ;
- proposer des parcours d’utilisation ;
- améliorer l’accessibilité ;
- créer des exemples, tutoriels ou captures d’écran ;
- aider les nouvelles personnes à s’orienter.

## Avant de proposer une grande orientation

Pour une modification majeure, ouvrir d’abord une discussion ou un ticket de conception. Décrire :

- le problème ;
- les personnes concernées ;
- les solutions envisagées ;
- les impacts sur la compatibilité ;
- les risques de maintenance ;
- le plan de migration.

## Licence des contributions

En contribuant, vous acceptez que votre contribution soit distribuée sous la GNU General Public License version 3.0 (`GPL-3.0-only`), selon les conditions décrites dans `LICENSE` et certifiées par le DCO.
