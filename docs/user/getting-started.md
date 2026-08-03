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

## Annuler ou rétablir une modification

La version 0.6.2 propose les deux directions de l’historique d’édition et l’organisation interactive de la séquence.

Pour **annuler** :

- menu **Édition → Annuler**;
- bouton **Annuler (Ctrl+Z)** au bas de la fenêtre;
- raccourci clavier `Ctrl+Z`.

Pour **rétablir** une action annulée :

- menu **Édition → Rétablir**;
- bouton **Rétablir (Ctrl+Y)** au bas de la fenêtre;
- raccourci clavier `Ctrl+Y` ou `Ctrl+Maj+Z`.

L’historique couvre explicitement :

- l’ajout et la suppression d’une ligne;
- le tempo, la signature et le nombre de mesures;
- les accords et le mode d’accord;
- les réglages d’arpégiateur;
- la duplication et le déplacement des lignes;
- l’activation ou la désactivation globale du click track;
- le SoundFont.

Les frappes rapprochées sont regroupées pour qu’un mot ou une valeur puisse être annulé en une seule étape plutôt qu’un caractère à la fois.

Après une annulation, toute nouvelle modification efface les états qui auraient pu être rétablis. Lorsqu’un autre projet `.gen` est ouvert, les deux piles sont réinitialisées afin d’éviter de restaurer accidentellement le projet précédent.

## Activer ou désactiver le click track du projet

Utiliser l’interrupteur **Click track du projet**, situé sous la configuration du SoundFont.

- **Activé** : la grosse caisse marque le premier temps et la caisse claire les autres subdivisions.
- **Désactivé** : aucun coup de métronome n’est produit dans le MIDI ou le WAV.

La désactivation ne retire pas les tempos, signatures, mesures, accords ni arpégiateurs. Le réglage est sauvegardé dans le fichier `.gen` et peut être annulé ou rétabli avec `Ctrl+Z` et `Ctrl+Y`.

## Utiliser les accords symboliques

Chaque ligne musicale possède un bouton de menu `☰`. Pour ajouter un accord à une ligne :

1. Cliquer sur `☰` au bout de la ligne.
2. Choisir **Accord → Accord au début de chaque ligne**.
3. Saisir un symbole d’accord, par exemple `C`, `Cm`, `C7`, `F#maj7`, `Bb9`, `C7#9`, `Dadd11` ou `G#m7(b13)`.
4. Choisir l’instrument : **Piano**, **Strings** ou **Guitare sèche**.
5. Cliquer sur `⌃` pour masquer la zone de saisie, sans effacer l’accord.

L’accord se répète à chaque mesure de la ligne. Sa durée est automatiquement adaptée à la signature rythmique de la ligne. Par exemple, une ligne en `7/8` génère un accord de durée `1*7/8` pour chaque mesure.

La notation `addX` est comprise de manière générique. Il est possible d’utiliser notamment `Dadd11`, `Cmadd9`, `C7add13`, `Fadd#11`, `Bbaddb9` ou la forme parenthésée `D(add11)`. Le degré ajouté est calculé automatiquement à partir de la gamme majeure et combiné à la qualité de l’accord de base.

Les extensions ou altérations entre parenthèses sont également reconnues sur une qualité existante. Par exemple, `G#m7(b13)` ajoute une treizième bémol à l’accord mineur septième, `C7(#9)` ajoute une neuvième augmentée, et `C7(b9,#11)` applique plusieurs modifications séparées par une virgule.

Pour utiliser un accord différent à chaque mesure :

1. Cliquer sur `☰` au bout de la ligne.
2. Choisir **Accord → Accord au début de chaque mesure**.
3. Remplir les cases `Mesure 1`, `Mesure 2`, etc.
4. Choisir l’instrument commun à la ligne.
5. Cliquer sur `⌃` pour masquer les cases sans effacer les accords.

Le nombre de cases suit automatiquement le nombre de mesures indiqué dans la ligne. Chaque accord dure une mesure complète. Une case vide génère une mesure de silence sur la portée d’accords.

### Utiliser une grille rythmique d’accords

1. Cliquer sur `☰` au bout de la ligne.
2. Choisir **Accord → Accords selon une subdivision rythmique**.
3. Choisir une subdivision : blanche, blanche pointée, noire, noire pointée, croche ou l’un des quatre triolets proposés.
4. Remplir les cases générées automatiquement.

Une ligne de quatre mesures en `4/4` produit 16 cases avec la subdivision **Noire**. Une virgule `,` prolonge l’accord précédent sans nouvelle attaque. Une case vide produit un silence. Les cases sont recalculées automatiquement lorsque la signature, le nombre de mesures ou la subdivision change.

Si la subdivision ne remplit pas exactement la ligne, la dernière case est raccourcie pour terminer précisément à la fin de la dernière mesure.

Pour revenir à une ligne sans harmonie, ouvrir le menu `☰` et choisir **Accord → Désactiver les accords**.

Dans le PDF, le symbole exact de l’accord est imprimé au-dessus de la partition, au début de chaque mesure concernée.

Pour la **Guitare sèche**, l’accord est généré avec `\arpeggio` dans LilyPond afin d’obtenir un rendu de type strum/arpège. Lorsque LilyPond possède un diagramme de guitare prédéfini pour l’accord, une ligne `FretBoards` est aussi ajoutée au-dessus de la partition. Les accords plus complexes, comme `C7#9`, restent affichés comme symboles textuels même si aucun diagramme prédéfini n’est disponible.

## Configurer un arpégiateur

Sous chaque champ d’accord se trouve un bouton **A**. `A✓` indique que l’arpégiateur de cette case est actif.

1. Saisir l’accord dans la case.
2. Cliquer sur **A**.
3. Activer l’arpégiateur.
4. Choisir le mouvement, le nombre d’octaves et la valeur rythmique.
5. Activer au besoin la valeur pointée.
6. Saisir `0` pour que la valeur soit la durée de chaque note, ou un nombre de `3` à `32` pour répartir exactement ce nombre de notes dans la durée totale choisie.
7. Cliquer sur **Enregistrer**.

Les trois mouvements disponibles sont :

- descendre puis remonter;
- monter puis redescendre;
- jouer les notes au hasard.

Le motif aléatoire est reproductible. Avec **Ronde + 7**, l’arpégiateur génère exactement sept notes pendant une ronde; avec **Noire + 5**, il génère exactement cinq notes pendant une noire. Dans une grille, une virgule prolonge l’accord précédent et conserve son arpégiateur; le bouton A de la case contenant la virgule n’est donc pas utilisé.

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

## Dupliquer une ligne

1. Repérer le bouton **D**, placé immédiatement à droite du bouton `−`.
2. Cliquer sur **D**.
3. La copie apparaît immédiatement sous l’original.

La copie comprend tous les champs, les accords, les grilles rythmiques, l’instrument et les réglages d’arpégiateur. Elle est indépendante de l’original. La duplication constitue une seule étape dans l’historique Annuler/Rétablir.

## Déplacer une ligne par cliquer-glisser

1. Repérer la poignée `⠿` à droite de la ligne.
2. Maintenir le bouton principal de la souris sur la poignée.
3. Déplacer la ligne vers sa nouvelle position.
4. Relâcher le bouton.

Le déplacement entier correspond à une seule étape dans l’historique. Utiliser `Ctrl+Z` pour revenir à l’ordre précédent, puis `Ctrl+Y` ou `Ctrl+Maj+Z` pour rétablir le déplacement.

