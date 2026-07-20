# GNU TrackGenerator

**Version : 0.1.0**

GNU TrackGenerator est une application de bureau open-source permettant de générer des *click tracks* programmables à partir de segments musicaux successifs. Chaque segment peut définir son propre tempo, sa signature rythmique et son nombre de mesures.

Le projet vise à offrir un outil simple, robuste et extensible pour les musiciens, pédagogues, compositeurs, répétiteurs, techniciens audio et développeurs qui veulent produire rapidement des pistes de métronome structurées.

## Philosophie générale

GNU TrackGenerator repose sur trois principes :

1. **Lisibilité** : les projets sont sauvegardés dans un format JSON `.gen`, facile à inspecter, versionner et modifier.
2. **Interopérabilité** : la génération musicale passe par LilyPond, MIDI et WAV, des formats et outils largement utilisés dans les écosystèmes libres.
3. **Modularité** : l'interface graphique est séparée du moteur de génération afin de faciliter les tests, les contributions et les futures interfaces possibles.

## Principe de fonctionnement

Le pipeline local de génération est le suivant :

1. L'utilisateur programme une séquence de segments dans l'interface.
2. L'application sauvegarde l'état du projet dans un fichier `.gen`.
3. L'application génère un fichier LilyPond `.ly` en mode `DrumStaff`.
4. LilyPond compile le fichier `.ly` en fichier MIDI.
5. FluidSynth ou TiMidity convertit le MIDI en fichier WAV.

Dans la version 0.1.0, chaque mesure suit une règle volontairement simple :

- la première subdivision de la mesure est jouée à la grosse caisse (`bd`) ;
- toutes les autres subdivisions sont jouées à la caisse claire (`sn`).

Exemples :

- `4/4` produit : `bd4 sn4 sn4 sn4`
- `7/8` produit : `bd8 sn8 sn8 sn8 sn8 sn8 sn8`
- `27/16` produit : `bd16` suivi de 26 coups de caisse claire `sn16`

## Fonctionnalités principales

- Interface graphique moderne avec CustomTkinter.
- Ajout et suppression dynamique de segments.
- Gestion des signatures asymétriques ou complexes, par exemple `5/4`, `7/8`, `11/16`, `27/16`.
- Sauvegarde et chargement de projets `.gen`.
- Génération automatique de fichiers `.ly`, `.mid` et `.wav`.
- Détection de base des erreurs : champs invalides, LilyPond manquant, moteur audio manquant, SoundFont absent.
- Architecture Python modulaire.

## Organisation du projet

```text
gnu-trackgenerator/
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── requirements.txt
├── pyproject.toml
└── src/
    └── gnu_trackgenerator/
        ├── __init__.py
        ├── __main__.py
        ├── main.py
        ├── gui.py
        ├── generator.py
        ├── models.py
        └── project_io.py
```

## Prérequis système

GNU TrackGenerator utilise des outils externes installés sur le système :

- Python 3.10 ou plus récent.
- LilyPond disponible sur le `PATH` du système.
- FluidSynth ou TiMidity disponible sur le `PATH` du système.
- Un fichier SoundFont `.sf2` ou `.sf3` si FluidSynth est utilisé.

Exemples de SoundFonts compatibles :

- `FluidR3_GM.sf2`
- `FluidR3_GS.sf2`
- toute banque General MIDI compatible avec FluidSynth

La variable d'environnement suivante peut aussi être utilisée :

```bash
TRACKGENERATOR_SOUNDFONT=/chemin/vers/votre/soundfont.sf2
```

## Installation

Cloner le dépôt :

```bash
git clone https://example.org/gnu-trackgenerator.git
cd gnu-trackgenerator
```

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement virtuel :

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

Installation en mode développement :

```bash
pip install -e .
```

## Utilisation / Exécution

Lancer l'application depuis le dépôt :

```bash
python -m gnu_trackgenerator
```

Ou, après installation en mode développement :

```bash
gnu-trackgenerator
```

Étapes dans l'interface :

1. Remplir les segments musicaux : BPM, numérateur, dénominateur et nombre de mesures.
2. Ajouter ou supprimer des rangées selon la structure de la pièce.
3. Sélectionner un SoundFont si FluidSynth est utilisé.
4. Cliquer sur **Générer**.
5. Choisir un dossier de sortie et un nom de base pour les fichiers.

L'application générera :

```text
nom_du_projet.gen
nom_du_projet.ly
nom_du_projet.mid
nom_du_projet.wav
```

## Exemple de projet `.gen`

```json
{
  "app": "GNU TrackGenerator",
  "version": "0.1.0",
  "soundfont_path": "/chemin/vers/FluidR3_GM.sf2",
  "segments": [
    {
      "bpm": 120,
      "numerator": 4,
      "denominator": 4,
      "measures": 8
    },
    {
      "bpm": 140,
      "numerator": 7,
      "denominator": 8,
      "measures": 4
    }
  ]
}
```

## Licence

GNU TrackGenerator est distribué sous licence **GNU General Public License v3.0** (`GPL-3.0-only`).

Voir le fichier `LICENSE` du dépôt pour le texte complet de la licence.

## Crédits d'auteur

Auteur initial : **Steve Prud'Homme**  
Contributions : ouvertes à la communauté.

GNU TrackGenerator utilise l'écosystème LilyPond, FluidSynth / TiMidity et CustomTkinter.
