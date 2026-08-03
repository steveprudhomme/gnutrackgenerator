![Statut](https://img.shields.io/badge/statut-initialisation-yellow) ![Licence](https://img.shields.io/badge/licence-GPLv3-blue) ![Version](https://img.shields.io/badge/version-0.6.3-blue) **GNU TrackGenerator est un logiciel libre et gratuit : chacun peut l’utiliser, l’étudier, le modifier et le redistribuer selon les conditions de la GNU General Public License version 3.0.**

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


## Fonctionnalités de la version 0.6.3

- Commandes **Annuler** et **Rétablir** accessibles depuis le menu **Édition**, les boutons dédiés et les raccourcis `Ctrl+Z`, `Ctrl+Y` ou `Ctrl+Maj+Z`.
- Limite des piles Annuler/Rétablir configurable dans **Édition → Options**, avec `100` comme valeur par défaut.
- Préférence enregistrée entre les sessions dans un fichier de configuration propre à l’application, distinct des projets `.gen`.
- Une réduction de la limite supprime immédiatement les états les plus anciens tout en conservant les états les plus récents et le projet courant.
- Toute nouvelle modification effectuée après une annulation efface la pile de rétablissement, conformément au comportement habituel des logiciels de bureau.
- Regroupement automatique de la saisie au clavier pour éviter une étape d’annulation par caractère.
- Annulation et rétablissement vérifiés pour l’ajout et la suppression d’une ligne, les changements de tempo, de signature et de nombre de mesures, les accords, les modes d’accord, les réglages d’arpégiateur, la duplication, le déplacement et l’activation globale du click track.
- Validation explicite du schéma des instantanés afin qu’un champ éditable oublié soit détecté par les tests plutôt que silencieusement exclu de l’historique.
- Réinitialisation propre de l’historique lors de l’ouverture d’un autre projet `.gen`.
- Interrupteur global **Click track du projet** permettant d’activer ou de désactiver le métronome pour l’ensemble du projet.
- Lorsque le click track est désactivé, les tempos, signatures, durées, accords et arpégiateurs sont conservés; seules les attaques de grosse caisse et de caisse claire sont supprimées des sorties MIDI/WAV.
- Duplication complète d’une ligne avec le bouton **D**, placé immédiatement à droite du bouton `−`, avec insertion de la copie sous la ligne d’origine.
- Copie indépendante de tous les paramètres : tempo, signature, mesures, accords, grille rythmique, instrument et arpégiateurs.
- Réorganisation des lignes par cliquer-glisser avec la poignée `⠿` située à droite.
- La duplication et le déplacement créent chacun une étape unique dans Annuler/Rétablir.
- L’ordre affiché est aussi l’ordre sauvegardé dans le projet `.gen` et utilisé lors de l’export.
- Génération de click tracks programmables par segments : BPM, signature rythmique et nombre de mesures.
- Menu de ligne `☰` au bout de chaque rangée.
- Option **Accord au début de chaque ligne** dans le menu de ligne.
- Option **Accord au début de chaque mesure**, avec une case distincte pour chaque mesure de la ligne.
- Option **Accords selon une subdivision rythmique**, avec génération automatique du nombre de cases nécessaire pour toute la ligne.
- Subdivisions disponibles : blanche, blanche pointée, noire, noire pointée, croche, triolet de rondes, triolet de blanches, triolet de noires et triolet de croches.
- Une virgule `,` prolonge l’accord précédent sans le rejouer; une case vide crée un silence.
- Chaque champ d’accord possède un petit bouton **A** ouvrant ses réglages d’arpégiateur.
- L’arpégiateur peut être activé ou désactivé indépendamment pour chaque accord.
- Motifs disponibles : descendre puis remonter, monter puis redescendre et notes au hasard.
- Choix de 1 à 8 octaves, des valeurs ronde à double croche, des valeurs pointées et des N-olets configurables par un nombre de 3 à 32. Avec un N-olet, la valeur choisie représente la durée totale du groupe.
- Saisie d’accords sous forme de symboles musicaux standard basés sur les notes A, B, C, D, E, F, G.
- Conversion automatique des symboles d’accords en notes LilyPond.
- Interprétation générique de la notation `addX`, par exemple `Dadd11`, `Cmadd9`, `C7add13`, `Fadd#11` ou `Bbaddb9`.
- Tolérance pour la notation redondante `C5m` ou `Cm5`, interprétée comme `Cm`; le symbole original demeure affiché dans le PDF.
- Instruments disponibles pour la portée d’accords : **Piano**, **Strings** et **Guitare sèche**.
- Pour la **Guitare sèche**, les accords sont générés avec un rendu strummé/arpégé grâce à `\arpeggio`.
- Affichage du symbole d’accord exact au-dessus de la partition PDF, au début de chaque mesure concernée.
- Affichage de diagrammes d’accords de guitare via `FretBoards` lorsque l’instrument est **Guitare sèche** et que LilyPond possède un diagramme prédéfini.
- Sauvegarde du mode d’accord, des accords par mesure et de l’instrument dans le fichier `.gen`.
- Génération d’une portée d’accords séparée lorsque des accords sont définis.
- Conversion MIDI vers WAV avec **TiMidity en priorité**, puis FluidSynth comme solution de repli.
- Affichage en direct des commandes exécutées pendant la génération.
- Création d’un fichier `.commands.txt` contenant le journal complet de génération.
- Diagnostic automatique du fichier WAV généré : taille, durée, fréquence, nombre de canaux et détection d’un fichier silencieux.



### Accords au début de chaque mesure

Pour définir une progression harmonique mesure par mesure :

1. Cliquer sur le bouton `☰` de la ligne.
2. Choisir **Accord → Accord au début de chaque mesure**.
3. Saisir un accord dans chacune des cases affichées sous la ligne.
4. Modifier le nombre de mesures pour ajouter ou retirer automatiquement des cases visibles.
5. Utiliser `⌃` pour masquer la zone sans perdre les valeurs saisies.

Le menu permet aussi de choisir **Accord → Désactiver les accords** afin de revenir à une ligne de click simple tout en conservant temporairement les valeurs saisies dans l’interface.

Chaque case correspond exactement à une mesure. L’accord est généré avec la durée complète de cette mesure, y compris pour des signatures complexes comme `7/8`, `5/4` ou `27/16`. Une case laissée vide produit une mesure sans accord.

### Accords selon une subdivision rythmique

Pour créer des changements d’accords plus fréquents qu’une fois par mesure :

1. Cliquer sur le bouton `☰` de la ligne.
2. Choisir **Accord → Accords selon une subdivision rythmique**.
3. Choisir la valeur de note utilisée pour découper la ligne.
4. Remplir les cases générées automatiquement.
5. Saisir une virgule `,` dans une case pour prolonger l’accord précédent sans nouvelle attaque.
6. Laisser une case vide pour créer un silence pendant cette subdivision.

Exemple : une ligne de quatre mesures en `4/4` divisée en noires affiche **16 cases**. Les triolets utilisent leur durée réelle : un triolet de noires produit 24 cases sur la même ligne et un triolet de croches en produit 48.

Lorsque la subdivision choisie ne divise pas exactement la durée totale de la ligne, la dernière case est raccourcie automatiquement afin que la séquence se termine exactement à la fin de la dernière mesure.

Les accords prolongés par une virgule sont fusionnés dans la sortie MIDI/WAV. Lorsqu’une prolongation traverse une barre de mesure, GNU TrackGenerator divise la notation à la barre et ajoute une liaison LilyPond afin d’éviter une nouvelle attaque sonore.

Exemple de sauvegarde `.gen` :

```json
{
  "bpm": 120,
  "numerator": 4,
  "denominator": 4,
  "measures": 1,
  "chord_mode": "grid",
  "chord_grid_unit": "quarter",
  "grid_chords": ["C", ",", "G", null],
  "grid_arpeggiators": [
    {"enabled": true, "pattern": "up_down", "octaves": 2, "rhythm": "eighth", "dotted": false, "tuplet_count": 0},
    {"enabled": false, "pattern": "up_down", "octaves": 1, "rhythm": "eighth", "dotted": false, "tuplet_count": 0},
    {"enabled": true, "pattern": "random", "octaves": 1, "rhythm": "sixteenth", "dotted": false, "tuplet_count": 5},
    {"enabled": false, "pattern": "up_down", "octaves": 1, "rhythm": "eighth", "dotted": false, "tuplet_count": 0}
  ],
  "chord_instrument": "piano"
}
```

### Arpégiateur par accord

Chaque zone de saisie d’accord possède un bouton **A** placé sous le champ. Le bouton affiche `A✓` lorsque l’arpégiateur de cette case est activé. Les réglages sont propres à la case : un accord par ligne possède un réglage, le mode par mesure en possède un par mesure et la grille rythmique en possède un par case.

Réglages disponibles :

- **Activer l’arpégiateur** : désactivé, l’accord est joué normalement; activé, les notes sont jouées séparément.
- **Mouvement** : descendre puis remonter, monter puis redescendre ou notes au hasard.
- **Octaves** : de 1 à 8 octaves.
- **Valeur rythmique** : double croche, croche, noire, blanche ou ronde.
- **Valeur pointée** : applique le point à la valeur choisie.
- **N-olet** : `0` désactive cette fonction; la valeur rythmique est alors la durée de chaque note de l’arpège. Avec `N` entre 3 et 32, la valeur rythmique devient la durée totale d’un groupe contenant exactement N notes.

Le motif aléatoire est reproductible : la même sauvegarde génère la même séquence. Dans la grille rythmique, une virgule prolonge l’accord précédent avec son arpégiateur sans provoquer une nouvelle attaque.

Exemples de N-olets :

- **Ronde + 7** : sept notes réparties dans une ronde, générées sous la forme LilyPond `\tuplet 7/4` avec sept noires;
- **Blanche + 5** : cinq notes réparties dans une blanche, avec un rapport `5/4`;
- **Noire + 3** : trois notes réparties dans une noire, avec un rapport `3/2`;
- **Croche + 0** : aucune mécanique de N-olet; chaque note de l’arpège dure une croche.

Lorsque la durée d’un accord ne contient pas un nombre entier de groupes complets, un dernier groupe raccourci conserve exactement N attaques et se termine à la frontière de l’accord.

Exemple de sauvegarde `.gen` pour un accord par ligne :

```json
{
  "bpm": 120,
  "numerator": 4,
  "denominator": 4,
  "measures": 2,
  "chord_mode": "line",
  "chord_symbol": "Cmaj7",
  "chord_instrument": "piano",
  "arpeggiator": {
    "enabled": true,
    "pattern": "up_down",
    "octaves": 2,
    "rhythm": "eighth",
    "dotted": false,
    "tuplet_count": 3
  }
}
```

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

La saisie d’accord utilise des symboles comme `C`, `Cm`, `C7`, `F#maj7`, `Bb9`, `C7#9`, `Dadd11` ou `G#m7(b13)`. Les formes suivantes sont prises en charge pour toutes les fondamentales A à G, avec accidentels `#` ou `b` lorsque nécessaire.

La famille `addX` est interprétée de manière générique : le logiciel part de l’accord de base, puis ajoute le degré demandé sans qu’une définition particulière soit nécessaire pour chaque accord. Exemples :

- `Dadd11` → `1, 3, 5, 11`;
- `Cmadd9` → `1, b3, 5, 9`;
- `C7add13` → `1, 3, 5, b7, 13`;
- `Fadd#11` → `1, 3, 5, #11`;
- `Bbaddb9` → `1, 3, 5, b9`.

Les formes parenthésées, comme `D(add11)`, sont également acceptées. Le parseur comprend aussi les extensions et altérations appliquées à une qualité existante :

- `G#m7(b13)` → `1, b3, 5, b7, b13`;
- `C7(#9)` → `1, 3, 5, b7, #9`;
- `C7(b9,#11)` → `1, 3, 5, b7, b9, #11`;
- `Cm7(b5)` → `1, b3, b5, b7`.

Dans une altération parenthésée, un degré altéré remplace la version naturelle du même degré lorsqu’elle existe. Ainsi, `Cm7(b5)` remplace la quinte juste par une quinte diminuée.

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
| `Dadd11` | `1, 3, 5, 11` |
| `Fadd#11` | `1, 3, 5, #11` |
| `Cmadd9` | `1, b3, 5, 9` |
| `C7add13` | `1, 3, 5, b7, 13` |
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
| `C7#9`, `C7(#9)` | `1, 3, 5, b7, #9` |
| `G#m7(b13)` | `1, b3, 5, b7, b13` |

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
