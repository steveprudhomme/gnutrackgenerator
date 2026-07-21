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

- Correction de la syntaxe LilyPond des diagrammes de guitare pour les mesures complexes : les accords sont maintenant générés sous la forme `a1*7/4:m` au lieu de `a:m1*7/4`.

- Rien pour le moment.

### Sécurité

- Rien pour le moment.

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
