![Statut](https://img.shields.io/badge/statut-initialisation-yellow) ![Licence](https://img.shields.io/badge/licence-GPLv3-blue) ![Version](https://img.shields.io/badge/version-0.1.3-blue) **GNU TrackGenerator est un logiciel libre et gratuit : chacun peut l’utiliser, l’étudier, le modifier et le redistribuer selon les conditions de la GNU General Public License version 3.0.**

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

## Installation et démarrage sous Windows / PowerShell

Cette section décrit le démarrage concret de l’application Python actuelle. Les commandes doivent être exécutées à la **racine du projet**, c’est-à-dire dans le dossier qui contient `pyproject.toml`, `requirements.txt` et `README.md`.

Exemple de chemin :

```text
C:\Users\steve\Downloads\Projet GNU TrackGenerator
```

### 1. Se placer à la racine du projet

```powershell
cd "C:\Users\steve\Downloads\Projet GNU TrackGenerator"
```

Ne pas lancer les commandes d’installation depuis :

```text
src\gnu_trackgenerator
```

Ce sous-dossier contient le code du paquet, mais pas le fichier `pyproject.toml` qui décrit le projet installable.

### 2. Créer l’environnement virtuel, au besoin

```powershell
python -m venv .venv
```

### 3. Activer l’environnement virtuel

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloque l’activation des scripts, autoriser temporairement l’exécution pour la session courante :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Installer les dépendances Python

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Installer le projet en mode développement

```powershell
python -m pip install -e .
```

L’option `-e` installe le projet en mode modifiable. Cela permet de modifier le code source localement sans devoir réinstaller le paquet après chaque changement.

### 6. Démarrer l’application

```powershell
python -m gnu_trackgenerator
```

Après l’installation, la commande de script peut aussi être disponible :

```powershell
gnu-trackgenerator
```

### Séquence complète recommandée

```powershell
cd "C:\Users\steve\Downloads\Projet GNU TrackGenerator"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python -m gnu_trackgenerator
```

### Dépendances externes

L’interface peut démarrer avec les dépendances Python seulement. Cependant, la génération complète des fichiers demande aussi des outils externes installés sur le système :

- **LilyPond**, pour produire les fichiers MIDI à partir des fichiers `.ly`;
- **TiMidity** ou **FluidSynth**, pour convertir les fichiers MIDI en fichiers WAV;
- un fichier **SoundFont** `.sf2` ou `.sf3`, utilisé explicitement par TiMidity et FluidSynth lorsque fourni.

Pour vérifier que LilyPond est reconnu par Windows :

```powershell
Get-Command lilypond
lilypond --version
```

Pour vérifier FluidSynth :

```powershell
Get-Command fluidsynth
fluidsynth --version
```

Si une commande est introuvable, il faut ajouter le dossier contenant l’exécutable correspondant au `PATH` de Windows.


## Fonctionnalités de la version 0.1.3

- Génération de click tracks programmables par segments : BPM, signature rythmique et nombre de mesures.
- Menu de ligne `☰` au bout de chaque rangée.
- Option **Accord au début de chaque ligne** dans le menu de ligne.
- Saisie d’accords sous forme de symboles musicaux standard basés sur les notes A, B, C, D, E, F, G.
- Conversion automatique des symboles d’accords en notes LilyPond.
- Instruments disponibles pour la portée d’accords : **Piano**, **Strings** et **Guitare sèche**.
- Pour la **Guitare sèche**, les accords sont générés avec un rendu strummé/arpégé grâce à `\arpeggio`.
- Affichage du symbole d’accord exact au-dessus de la partition PDF, au début de chaque mesure concernée.
- Affichage de diagrammes d’accords de guitare via `FretBoards` lorsque l’instrument est **Guitare sèche** et que LilyPond possède un diagramme prédéfini.
- Sauvegarde des accords et instruments dans le fichier `.gen`.
- Génération d’une portée d’accords séparée lorsque des accords sont définis.
- Conversion MIDI vers WAV avec **TiMidity en priorité**, puis FluidSynth comme solution de repli.
- Affichage en direct des commandes exécutées pendant la génération.
- Création d’un fichier `.commands.txt` contenant le journal complet de génération.
- Diagnostic automatique du fichier WAV généré : taille, durée, fréquence, nombre de canaux et détection d’un fichier silencieux.



### Affichage des accords dans le PDF

Lorsqu’un accord est défini sur une ligne, son symbole exact est imprimé au-dessus de la partition PDF, au début de chaque mesure générée pour cette ligne. Par exemple, une ligne contenant `C7#9` affichera `C7#9` au-dessus du premier coup de click de chaque mesure.

Si l’instrument choisi est **Guitare sèche**, GNU TrackGenerator ajoute aussi une ligne de diagrammes d’accords de guitare avec `FretBoards` lorsque le diagramme est disponible dans les accords prédéfinis de LilyPond. Les accords complexes ou altérés qui n’ont pas de diagramme prédéfini, comme `C7#9`, demeurent affichés comme symboles textuels au-dessus de la partition.

### Journal de génération et dépannage WAV

Lorsqu’on clique sur **Générer**, l’application affiche maintenant un **journal de génération** directement dans l’interface. Ce journal montre les fichiers écrits et les commandes réellement exécutées pour LilyPond, TiMidity et FluidSynth.

Un fichier portant l’extension `.commands.txt` est aussi créé dans le dossier de sortie. Il permet de copier-coller exactement les commandes dans PowerShell pour comprendre ce qui se passe.

Exemple de commandes attendues lorsqu’un SoundFont est sélectionné :

```powershell
lilypond -dno-point-and-click -o nom_du_fichier nom_du_fichier.ly
timidity -c nom_du_fichier.timidity.cfg -A120 -Ow -o nom_du_fichier.wav nom_du_fichier.mid
```

L’application écrit aussi un fichier `nom_du_fichier.timidity.cfg` contenant la ligne `soundfont`, par exemple :

```text
soundfont "C:/SoundFonts/CrisisGeneralMidi301.sf2" order=0 amp=120
```

Si le fichier WAV est généré mais ne contient pas de son, vérifier dans le journal :

- la présence d’avertissements dans `stdout` ou `stderr`;
- la taille du fichier WAV;
- le diagnostic `pic=0`, qui indique un fichier probablement silencieux;
- la configuration de TiMidity;
- la présence d’un fichier `nom_du_fichier.timidity.cfg`;
- la présence d’une ligne `soundfont` pointant vers la banque de sons choisie;
- la présence d’un SoundFont valide, par exemple `CrisisGeneralMidi301.sf2`.

TiMidity peut convertir un MIDI en WAV avec l’option `-Ow`, mais il doit avoir une banque de sons utilisable. Lorsque l’utilisateur sélectionne un SoundFont, GNU TrackGenerator génère maintenant une configuration TiMidity dédiée et l’appelle avec `-c`. Si le rendu TiMidity reste silencieux ou extrêmement faible et que FluidSynth est disponible, l’application tente un rendu de repli avec FluidSynth et le même SoundFont.

### Accords supportés

La saisie d’accord utilise des symboles comme `C`, `Cm`, `C7`, `F#maj7`, `Bb9` ou `C7#9`. Les formes suivantes sont prises en charge pour toutes les fondamentales A à G, avec accidentels `#` ou `b` lorsque nécessaire.

| Notation | Degrés |
|---|---|
| `C5` | `1, 5` |
| `C(b5)` | `1, b5` |
| `C` | `1, 3, 5` |
| `Cm` | `1, b3, 5` |
| `Cdim`, `C°` | `1, b3, b5` |
| `Caug`, `C+` | `1, 3, #5` |
| `Csus2` | `1, 2, 5` |
| `Csus4` | `1, 4, 5` |
| `C7sus4` | `1, 4, 5, b7` |
| `Cadd2`, `Cμ` | `1, 2, 3, 5` |
| `Cadd9` | `1, 3, 5, 9` |
| `C6` | `1, 3, 5, 6` |
| `Cm6` | `1, b3, 5, 6` |
| `Cmaj7` | `1, 3, 5, 7` |
| `C7` | `1, 3, 5, b7` |
| `Cm7` | `1, b3, 5, b7` |
| `Cm7b5`, `Cø` | `1, b3, b5, b7` |
| `Cdim7` | `1, b3, b5, bb7` |
| `CmM7` | `1, b3, 5, 7` |
| `Cmaj9` | `1, 3, 5, 7, 9` |
| `C9` | `1, 3, 5, b7, 9` |
| `Cm9` | `1, b3, 5, b7, 9` |
| `Cm11` | `1, b3, 5, b7, 9, 11` |
| `C13` | `1, 3, 5, b7, 9, 11, 13` |
| `Cmaj13` | `1, 3, 5, 7, 9, 11, 13` |
| `C7#9` | `1, 3, 5, b7, #9` |

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


## Note de correction — Syntaxe LilyPond des diagrammes de guitare

Pour les diagrammes de guitare générés dans `FretBoards`, la durée est placée avant le type d’accord, par exemple `a1*7/4:m`. Cette forme est nécessaire pour éviter l’erreur LilyPond `unexpected '*'` qui survient avec une forme invalide comme `a:m1*7/4`.
