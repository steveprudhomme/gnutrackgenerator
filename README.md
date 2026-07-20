![Statut](https://img.shields.io/badge/statut-initialisation-yellow) ![Licence](https://img.shields.io/badge/licence-GPLv3-blue) ![Version](https://img.shields.io/badge/version-0.1.2-blue) **GNU TrackGenerator est un logiciel libre et gratuit : chacun peut l’utiliser, l’étudier, le modifier et le redistribuer selon les conditions de la GNU General Public License version 3.0.**

# GNU TrackGenerator

## Mission

GNU TrackGenerator vise à fournir un outil ouvert, fiable et extensible pour générer des pistes de métronome programmables, tout en servant de dépôt exemplaire pour un projet libre maintenable à long terme.

La proposition de valeur du projet est simple : permettre à des utilisateurs, contributrices et contributeurs de comprendre rapidement le but du logiciel, de l’exécuter localement, de proposer des améliorations et de participer à sa gouvernance sans dépendre de connaissances implicites ou de décisions opaques.

## Projet ouvert à la collaboration

GNU TrackGenerator est conçu comme un projet communautaire. Les contributions sont encouragées, y compris les contributions modestes ou non techniques.

Vous pouvez contribuer de plusieurs manières :

- signaler un bogue reproductible ;
- proposer une amélioration ;
- améliorer la documentation ;
- ajouter ou corriger des tests ;
- traduire une page ;
- relire une demande de tirage ;
- aider à trier les tickets ;
- proposer des exemples musicaux ;
- améliorer l’accessibilité de l’interface ;
- participer aux discussions de conception.

Le projet vise une collaboration saine : décisions publiques, règles claires, respect du temps bénévole et attribution explicite des contributions. Le point d’entrée recommandé est `docs/community/collaboration-guide.md`.

## Comment contribuer en 15 minutes

1. Lire `CONTRIBUTING.md` et `CODE_OF_CONDUCT.md`.
2. Choisir un ticket étiqueté `good first issue`, `documentation`, `test`, `help wanted` ou `triage`.
3. Commenter le ticket pour signaler votre intention de travailler dessus.
4. Créer une petite branche dédiée.
5. Soumettre une demande de tirage courte, testée et signée avec DCO.

Aucune contribution n’est trop petite si elle rend le projet plus clair, plus fiable ou plus accueillant.


## Philosophie du projet

Le projet applique les principes suivants :

- **Accessibilité** : une nouvelle personne doit pouvoir comprendre le projet en quelques minutes.
- **Prévisibilité** : les changements importants sont documentés, versionnés et annoncés.
- **Traçabilité** : les décisions, contributions et incidents sont conservés dans des espaces publics ou documentés.
- **Soutenabilité** : les mainteneurs ne sont pas tenus d’offrir du support illimité ou instantané.
- **Sécurité juridique** : les droits d’auteur, la licence et l’origine des contributions sont explicitement encadrés.

## Quickstart

> Cette section demeure volontairement conceptuelle afin que l’arborescence reste utilisable peu importe le langage ou la pile technique du projet.

### 1. Cloner le dépôt

```bash
git clone https://example.org/organisation/gnu-trackgenerator.git
cd gnu-trackgenerator
```

### 2. Préparer l’environnement local

Créer un environnement isolé selon les conventions de la pile technique utilisée par le projet :

```bash
# Exemple conceptuel — adapter au langage et aux outils retenus
make setup
```

ou :

```bash
# Exemple conceptuel — adapter au gestionnaire de dépendances du projet
./scripts/setup
```

### 3. Exécuter les vérifications

```bash
make test
make lint
make check
```

### 4. Lancer le projet

```bash
make run
```

Si le projet n’utilise pas `make`, consulter `docs/user/getting-started.md` pour la commande officielle équivalente.

## Fonctionnalités prévues

- Génération locale de fichiers de travail reproductibles.
- Séparation nette entre code source, documentation, tests et outils de collaboration.
- Support d’un cycle de contribution ouvert : tickets, demandes de tirage, revue, intégration continue.
- Documentation publique des décisions d’architecture.
- Gouvernance transparente et évolutive.

## Organisation du dépôt

```text
.
├── .github/                     # Collaboration, tickets, PR, automatisation
│   ├── ISSUE_TEMPLATE/           # Modèles de demandes
│   ├── PULL_REQUEST_TEMPLATE.md  # Canevas de revue des contributions
│   └── workflows/                # Exemples CI/CD
├── docs/                         # Documentation séparée du code source
│   ├── architecture/             # Décisions et schémas d’architecture
│   ├── specifications/           # Spécifications fonctionnelles et techniques
│   ├── community/                # Guides de collaboration
│   └── user/                     # Documentation d’utilisation
├── src/                          # Code source de production
├── tests/                        # Tests unitaires, intégration, non-régression
├── README.md                     # Présentation du projet
├── CONTRIBUTORS.md               # Reconnaissance des contributions
├── MAINTAINERS.md                # Liste et rôle des mainteneurs
├── LICENSE                       # Licence choisie et cadre de droits d’auteur
├── CONTRIBUTING.md               # Guide de contribution et DCO
├── CODE_OF_CONDUCT.md            # Règles de participation communautaire
├── CHANGELOG.md                  # Historique des changements
├── SUPPORT.md                    # Politique de support
├── SECURITY.md                   # Divulgation responsable
├── GOVERNANCE.md                 # Gouvernance du projet
└── .gitignore                    # Fichiers ignorés par Git
```

Les fichiers déjà présents du projet GNU TrackGenerator sont conservés dans `src/gnu_trackgenerator/`. Les anciens fichiers de documentation initiaux ont été archivés dans `docs/legacy/` afin de préserver l’historique tout en mettant à jour les fichiers communautaires de la racine.

## Canaux officiels de collaboration et de communication

| Usage | Canal officiel |
|---|---|
| Questions d’utilisation | Discussions communautaires : `[lien à ajouter]` |
| Discussion synchrone | Salon de clavardage : `[Matrix/Discord/IRC à ajouter]` |
| Annonces importantes | Liste de diffusion : `[adresse à ajouter]` |
| Bogues confirmés | Tickets publics du dépôt |
| Vulnérabilités | Signalement privé selon `SECURITY.md` |
| Décisions de gouvernance | `GOVERNANCE.md` et discussions publiques liées |

## Contribuer

Les contributions techniques et non techniques sont les bienvenues : code, documentation, tri des tickets, tests, design, accessibilité, traduction, exemples, soutien aux nouveaux utilisateurs.

Avant de contribuer, lire :

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `GOVERNANCE.md`
- `SECURITY.md`, si la contribution touche à une faille ou à un risque de sécurité

Toutes les contributions doivent respecter le protocole DCO avec une ligne `Signed-off-by` dans chaque commit.

## Licence

Le projet est distribué sous la **GNU General Public License version 3.0** (`GPL-3.0-only`).

Consulter `LICENSE` pour le texte complet de la licence. Les redistributions et modifications doivent respecter les obligations de la GPLv3, notamment la conservation des avis de licence et la mise à disposition du code source correspondant lors de la distribution.

## Crédit d’auteur

Copyright © 2026 Steve Prud'Homme et les contributeurs de GNU TrackGenerator

Les contributions individuelles demeurent attribuées à leurs auteurs respectifs, selon l’historique Git et le protocole DCO.

Identifiant SPDX recommandé : `GPL-3.0-only`.
