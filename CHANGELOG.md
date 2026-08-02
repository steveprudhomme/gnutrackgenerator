# Changelog

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur **Keep a Changelog** et le projet suit le **Versionnage Sémantique**.

## [Unreleased]

### Ajouté

- Rien pour le moment.

### Changé

- Rien pour le moment.

### Déprécié

- Rien pour le moment.

### Retiré

- Rien pour le moment.

### Corrigé

- Rien pour le moment.

### Sécurité

- Rien pour le moment.

## [0.5.0] - 2026-08-02

### Ajouté

- Commande **Annuler** dans le menu **Édition** avec l’accélérateur `Ctrl+Z`.
- Bouton **Annuler (Ctrl+Z)** dans la barre d’actions principale.
- Module indépendant `history.py` fournissant une pile d’annulation bornée à 100 états.
- Historique des valeurs brutes de l’interface, y compris les saisies temporairement invalides.
- Prise en charge de l’annulation pour les champs principaux, le SoundFont, les accords, les modes d’accord, les réglages d’arpégiateur ainsi que l’ajout et la suppression de lignes.
- Tests unitaires du gestionnaire d’historique.

### Changé

- Les frappes rapprochées sont regroupées dans une seule étape d’annulation grâce à un délai de stabilisation.
- L’ouverture d’un projet `.gen` réinitialise l’historique afin d’éviter de revenir accidentellement au projet précédent.
- Passage de la version du projet à `0.5.0`.

### Corrigé

- La restauration reconstruit les champs dynamiques d’accords et leurs réglages d’arpégiateur sans exiger que l’état intermédiaire soit déjà valide.

## [0.4.2] - 2026-08-02

### Changé

- Le parseur tolère maintenant les notations redondantes `C5m` et `Cm5`, interprétées comme un accord mineur complet.
- Les extensions suivant cette écriture sont conservées, par exemple `C5m7` est interprété comme `Cm7`.
- Passage de la version du projet à `0.4.2`.

### Corrigé

- La progression `E5 B5 E5 C5m F#5(b5) B5` peut maintenant être générée sans rejet de `C5m`.
- Ajout de tests de non-régression pour les accords de quinte, les accords mineurs à quinte explicite et les quintes diminuées parenthésées.

## [0.4.1] - 2026-08-01

### Changé

- La figure rythmique sélectionnée représente maintenant la durée totale du groupe lorsque le champ N-olet contient une valeur de 3 à 32.
- Le moteur choisit automatiquement une unité écrite et un rapport LilyPond adaptés afin de produire exactement N attaques dans la durée demandée.
- Passage de la version du projet à `0.4.1`.

### Corrigé

- Correction de la mécanique des N-olets de l’arpégiateur : `Ronde + 7` génère désormais exactement sept notes réparties dans une ronde.
- Correction du calcul des rapports usuels, notamment `3/2`, `5/4`, `7/4` et `9/8`, selon la durée totale du groupe.
- Correction des groupes successifs et du dernier groupe raccourci afin de conserver exactement N attaques sans dépasser la durée de l’accord.

## [0.4.0] - 2026-08-01

### Ajouté

- Bouton **A** sous chaque champ d’accord des modes par ligne, par mesure et grille rythmique.
- Fenêtre de configuration propre à chaque accord avec activation indépendante.
- Motifs d’arpège montant-descendant, descendant-montant et aléatoire reproductible.
- Choix de 1 à 8 octaves.
- Valeurs rythmiques : double croche, croche, noire, blanche et ronde, avec option pointée.
- N-olets génériques configurables de 3 à 32.
- Module `arpeggiator.py` et sérialisation `.gen` des réglages par accord.
- Tests unitaires pour les motifs, durées, N-olets, sauvegardes et sortie LilyPond.

### Changé

- La portée harmonique peut maintenant contenir de véritables notes arpégées plutôt qu’un accord vertical.
- Une virgule dans la grille conserve les réglages d’arpégiateur de l’accord prolongé.
- Passage de la version du projet à `0.4.0`.

### Corrigé

- La durée de la dernière note d’un arpège est ajustée afin de terminer exactement à la fin de l’accord.
- Les anciens fichiers `.gen` sans réglages d’arpégiateur restent compatibles et utilisent des réglages désactivés par défaut.

## [0.3.0] - 2026-08-01

### Ajouté

- Nouveau mode **Accords selon une subdivision rythmique** dans le menu de ligne `☰`.
- Subdivisions : blanche, blanche pointée, noire, noire pointée, croche et triolets de rondes, blanches, noires et croches.
- Calcul dynamique du nombre de cases selon la signature et le nombre de mesures.
- Champs `.gen` `chord_grid_unit` et `grid_chords`.
- Module `rhythm.py` fondé sur des fractions exactes.
- Tests unitaires pour les grilles rythmiques, les triolets et la sérialisation.

### Changé

- Les symboles d’accord sont maintenant portés par une piste de silences invisibles, ce qui permet leur placement exact à l’intérieur des mesures.
- Les accords sont générés à partir d’une chronologie commune aux modes par ligne, par mesure et par subdivision.

### Corrigé

- Une virgule `,` prolonge l’accord précédent sans le rejouer.
- Les prolongations traversant une barre de mesure sont divisées et liées dans la sortie LilyPond.
- La dernière case est raccourcie lorsque la subdivision ne divise pas exactement la durée totale de la ligne.
- Les accords avec extensions ou altérations parenthésées, notamment `G#m7(b13)`, `C7(#9)` et `C7(b9,#11)`, sont maintenant reconnus par le parseur.

## [0.2.0] - 2026-07-21

### Ajouté

- Ajout d’un parseur générique pour les accords contenant `addX`.
- Ajout de la prise en charge de formes comme `Dadd11`, `Cmadd9`, `C7add13`, `Fadd#11`, `Bbaddb9` et `D(add11)`.
- Ajout du calcul algorithmique des degrés composés et altérés à partir de la gamme majeure.
- Ajout de tests unitaires couvrant les accords `add`, les qualités de base et les degrés altérés.
- Ajout de l’option **Accord au début de chaque mesure** dans le menu de ligne `☰`.
- Ajout d’une série dynamique de cases d’accord correspondant exactement au nombre de mesures de la ligne.
- Ajout de la possibilité de saisir un accord différent pour chaque mesure.
- Ajout d’un bouton `⌃` pour masquer la zone d’accords par mesure sans effacer les valeurs.
- Ajout des champs `chord_mode` et `measure_chords` au format `.gen`.
- Ajout de tests de sauvegarde, de compatibilité ascendante et de génération LilyPond mesure par mesure.

### Changé

- Le logiciel n’exige plus une définition codée séparément pour chaque nouvel accord `addX`.
- Chaque accord par mesure dure désormais exactement une mesure complète selon la signature rythmique.
- Les symboles d’accord sont affichés au-dessus de la mesure correspondante dans le PDF.
- Les portées d’accords et les diagrammes de guitare suivent désormais les progressions mesure par mesure.
- Les anciens projets utilisant seulement `chord_symbol` restent compatibles et sont interprétés comme des accords par ligne.
- Passage de la version du projet à `0.2.0`.

### Corrigé

- `Dadd11` et les accords similaires ne sont plus rejetés comme types d’accord inconnus.

## [0.1.3] - 2026-07-20

### Ajouté

- Ajout du module `chords.py` pour convertir les symboles d’accords en notes LilyPond.
- Ajout de la saisie d’accords par symboles musicaux : `C`, `Cm`, `C7`, `F#maj7`, `Bb9`, `C7#9`, etc.
- Ajout du bouton de menu `☰` au bout de chaque ligne.
- Ajout de l’option `Accord → Accord au début de chaque ligne` dans le menu de ligne.
- Ajout d’une zone de saisie d’accord sous la ligne, masquable avec l’icône `⌃`.
- Ajout du choix d’instrument pour les accords : Piano, Strings et Guitare sèche.
- Ajout d’un rendu strummé/arpégé pour la Guitare sèche avec `\arpeggio`.
- Ajout de l’affichage du symbole d’accord exact au-dessus de la partition PDF.
- Ajout de diagrammes d’accords de guitare dans le PDF avec `FretBoards` et `predefined-guitar-fretboards.ly` lorsque disponibles.
- Ajout de tests unitaires pour vérifier la génération LilyPond des symboles d’accords et des diagrammes de guitare.
- Ajout de la sauvegarde des symboles d’accords et instruments dans les fichiers `.gen`.
- Ajout de tests unitaires pour les conversions d’accords.
- Ajout d’une section `Installation et démarrage sous Windows / PowerShell` dans `README.md`.
- Ajout d’instructions concrètes pour créer et activer l’environnement virtuel, installer les dépendances et lancer l’application.
- Ajout d’une explication de l’erreur courante liée à l’exécution de `pip install -e .` depuis le mauvais dossier.
- Mise à jour de `docs/user/getting-started.md` avec les mêmes consignes pratiques.
- Ajout d’un journal visible dans l’interface pendant la génération.
- Ajout d’un fichier `.commands.txt` contenant les commandes exécutées, les sorties `stdout`/`stderr` et les diagnostics.
- Ajout d’un diagnostic automatique du WAV généré pour repérer un fichier vide, silencieux ou très faible.
- Ajout de la génération automatique d’un fichier `nom_du_fichier.timidity.cfg` lorsque l’utilisateur sélectionne un SoundFont.
- Ajout d’un test unitaire pour vérifier la génération de la configuration TiMidity avec SoundFont.

### Corrigé

- Correction de la syntaxe LilyPond des diagrammes de guitare pour les mesures complexes : les accords sont générés sous la forme `a1*7/4:m` plutôt que `a:m1*7/4`.

### Changé

- La conversion MIDI vers WAV utilise maintenant TiMidity en priorité, avec FluidSynth comme solution de repli.
- La commande TiMidity est maintenant affichée et exécutée avec configuration SoundFont explicite lorsque disponible : `timidity -c fichier.timidity.cfg -A120 -Ow -o fichier.wav fichier.mid`.
- Si le rendu TiMidity demeure extrêmement faible, l’application tente FluidSynth en repli avec le même SoundFont lorsque possible.
- La génération LilyPond ajoute une portée d’accords distincte lorsque des accords sont définis.
- Passage de la version du projet à `0.1.3`.

## [0.1.2] - 2026-07-20

### Ajouté

- Ajout d’une feuille de route enrichie dans `ROADMAP.md`.
- Ajout d’une orientation de développement pour un menu de ligne avec icône « trois lignes ».
- Ajout des scénarios futurs d’accords au début de chaque ligne et au début de chaque mesure.
- Ajout de points à clarifier avant le développement de la gestion harmonique.

### Changé

- Réorganisation de la feuille de route afin de prioriser la gestion des accords en `v0.2.0`.
- Passage de la version du projet à `0.1.2`.

## [0.1.1] - 2026-07-20

### Ajouté

- Ajout d’une orientation explicite d’ouverture à la collaboration communautaire.
- Ajout de `CONTRIBUTORS.md` pour reconnaître les contributions techniques et non techniques.
- Ajout de `MAINTAINERS.md` pour clarifier les responsabilités de maintenance.
- Ajout de `docs/community/collaboration-guide.md` comme porte d’entrée pour les nouveaux contributeurs.
- Ajout de modèles de tickets pour les questions et les améliorations de documentation.
- Ajout d’une configuration GitHub d’orientation des demandes.

### Changé

- Mise à jour du `README.md` avec une section “Projet ouvert à la collaboration”.
- Mise à jour de `CONTRIBUTING.md` pour mieux distinguer les parcours de contribution.
- Mise à jour de `GOVERNANCE.md` pour préciser la trajectoire d’accueil des contributeurs réguliers.
- Passage de la version du projet à `0.1.1`.

## [0.1.0] - 2026-07-01

### Ajouté

- Première structure de projet.
- Première documentation initiale.
- Premier code source conservé dans `src/`.
