# Démarrage utilisateur

Ce guide explique comment installer, configurer et lancer GNU TrackGenerator dans un environnement local.

## Prérequis

- Python 3.10 ou plus récent.
- `pip`.
- Un terminal PowerShell, Terminal Windows, Bash ou équivalent.
- Pour la génération complète : LilyPond.
- Pour la conversion audio : FluidSynth ou TiMidity.
- Pour TiMidity ou FluidSynth : un fichier SoundFont `.sf2` ou `.sf3` recommandé.

## Démarrage sous Windows / PowerShell

Les commandes doivent être exécutées à la racine du projet. La racine est le dossier qui contient `pyproject.toml`, `requirements.txt` et `README.md`.

```powershell
cd "C:\Users\steve\Downloads\Projet GNU TrackGenerator"
```

Créer l’environnement virtuel :

```powershell
python -m venv .venv
```

Activer l’environnement virtuel :

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloque l’activation :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Installer le projet en mode développement :

```powershell
python -m pip install -e .
```

Démarrer l’application :

```powershell
python -m gnu_trackgenerator
```

Ou, si le script est disponible après installation :

```powershell
gnu-trackgenerator
```

## Séquence complète recommandée

```powershell
cd "C:\Users\steve\Downloads\Projet GNU TrackGenerator"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
python -m gnu_trackgenerator
```

## Erreur courante : `pyproject.toml` introuvable

Si cette erreur apparaît :

```text
does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found
```

Cela signifie généralement que la commande `python -m pip install -e .` a été lancée depuis le mauvais dossier.

Ne pas lancer la commande depuis :

```text
src\gnu_trackgenerator
```

Il faut plutôt revenir à la racine du projet :

```powershell
cd ..\..
python -m pip install -e .
```

## Dépendances externes

L’interface graphique peut démarrer avec les dépendances Python seulement. Pour générer les fichiers `.ly`, `.mid` et `.wav`, le système doit aussi trouver LilyPond et un moteur de conversion MIDI vers WAV.

Vérifier LilyPond :

```powershell
Get-Command lilypond
lilypond --version
```

Vérifier FluidSynth :

```powershell
Get-Command fluidsynth
fluidsynth --version
```

Si Windows ne trouve pas ces commandes, ajouter le dossier contenant `lilypond.exe` ou `fluidsynth.exe` au `PATH`.

## Dépannage

Consulter `SUPPORT.md` avant d’ouvrir un ticket. Pour signaler un bogue, utiliser le modèle de rapport de bogue dans `.github/ISSUE_TEMPLATE/bug_report.md`.

## Utiliser les accords symboliques

Chaque ligne musicale possède un bouton de menu `☰`. Pour ajouter un accord à une ligne :

1. Cliquer sur `☰` au bout de la ligne.
2. Choisir **Accord → Accord au début de chaque ligne**.
3. Saisir un symbole d’accord, par exemple `C`, `Cm`, `C7`, `F#maj7`, `Bb9` ou `C7#9`.
4. Choisir l’instrument : **Piano**, **Strings** ou **Guitare sèche**.
5. Cliquer sur `⌃` pour masquer la zone de saisie, sans effacer l’accord.

L’accord se répète à chaque mesure de la ligne. Sa durée est automatiquement adaptée à la signature rythmique de la ligne. Par exemple, une ligne en `7/8` génère un accord de durée `1*7/8` pour chaque mesure.

Dans le PDF, le symbole exact de l’accord est imprimé au-dessus de la partition, au début de chaque mesure concernée.

Pour la **Guitare sèche**, l’accord est généré avec `\arpeggio` dans LilyPond afin d’obtenir un rendu de type strum/arpège. Lorsque LilyPond possède un diagramme de guitare prédéfini pour l’accord, une ligne `FretBoards` est aussi ajoutée au-dessus de la partition. Les accords plus complexes, comme `C7#9`, restent affichés comme symboles textuels même si aucun diagramme prédéfini n’est disponible.

## Vérifier TiMidity

La conversion MIDI vers WAV utilise maintenant **TiMidity en priorité**. FluidSynth reste disponible comme solution de repli.

```powershell
Get-Command timidity
timidity --version
```

Si TiMidity est installé, il sera essayé en priorité. Lorsqu’un SoundFont est sélectionné dans l’interface, l’application génère automatiquement un fichier `nom_du_fichier.timidity.cfg` pour forcer TiMidity à charger cette banque de sons. Si TiMidity n’est pas installé ou si le rendu demeure trop faible, l’application peut tenter FluidSynth avec le même SoundFont.

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
