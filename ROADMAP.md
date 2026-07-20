# ROADMAP — GNU TrackGenerator

Ce document présente les pistes d’évolution envisagées pour GNU TrackGenerator. Il ne constitue pas une promesse contractuelle : les priorités pourront évoluer selon les besoins des utilisateurs, les contributions, la stabilité technique et les décisions de gouvernance du projet.

## v0.1.x — Stabilisation du socle

Objectif : consolider la base fonctionnelle actuelle avant d’ajouter des fonctions musicales plus avancées.

- Maintenir une interface graphique CustomTkinter simple et lisible.
- Garder une séparation claire entre l’interface, les modèles, la sauvegarde et le moteur de génération.
- Améliorer les messages d’erreur pour LilyPond, FluidSynth, TiMidity et les SoundFonts.
- Documenter les chemins système requis pour les outils externes.
- Ajouter des tests unitaires pour la validation des segments et la génération LilyPond.
- Garder la licence, la gouvernance, le support et les modèles de contribution à jour.

## v0.2.0 — Menu de ligne et première gestion des accords

Objectif : ajouter une première interface d’édition harmonique à chaque ligne de séquence, sans complexifier inutilement le flux principal de génération de click track.

### 1. Ajouter un menu de ligne

- Ajouter une icône « trois lignes » ou menu contextuel à l’extrémité de chaque ligne musicale.
- Le menu doit permettre d’activer des options propres à la ligne courante.
- Le menu doit rester compact afin de ne pas surcharger l’interface principale.

### 2. Ajouter l’option « Accord » dans le menu

- Ajouter une entrée **Accord** dans le menu de ligne.
- L’entrée **Accord** doit ouvrir un sous-menu ou un panneau d’options liées aux accords.
- Les options d’accord doivent être désactivables afin que l’utilisateur puisse revenir à une ligne simple de click track.

### 2.1. Sous-menu : accord au début de chaque ligne

Objectif : permettre à l’utilisateur de saisir un accord unique associé à la ligne complète.

- Ajouter l’option **Accord au début de chaque ligne**.
- Lorsqu’elle est activée, afficher sous la ligne principale une zone de saisie dédiée à l’accord.
- Cette zone doit indiquer clairement que l’accord saisi s’applique à toute la ligne.
- L’utilisateur peut saisir l’accord dans cette zone.
- L’accord se répète à chaque mesure de la ligne.
- Chaque accord doit durer l’équivalent d’une mesure complète.
- Les notes générées pour l’accord doivent donc avoir une durée correspondant à la grandeur de la mesure en question.
- L’utilisateur peut fermer ou masquer la zone de saisie grâce à une icône ou un caractère de flèche.

### 2.2. Sous-menu : accord au début de chaque mesure

Objectif : permettre à l’utilisateur de définir un accord différent pour chaque mesure d’une ligne.

- Ajouter l’option **Accord au début de chaque mesure**.
- Lorsqu’elle est activée, afficher sous la ligne principale une série de cases de saisie.
- Le nombre de cases affichées doit correspondre au nombre de mesures défini pour la ligne.
- Chaque case représente l’accord à jouer au début de la mesure correspondante.
- L’utilisateur peut saisir un accord différent dans chaque case.
- Chaque accord doit durer l’équivalent d’une mesure complète.
- Les notes générées pour chaque accord doivent donc avoir une durée correspondant à la grandeur de la mesure en question.
- L’utilisateur peut fermer ou masquer la zone de saisie grâce à une icône ou un caractère de flèche.

### 2.3. Comportement attendu du moteur de génération

- Étendre le format `.gen` afin de sauvegarder les accords associés aux lignes.
- Préserver la compatibilité avec les anciens fichiers `.gen` qui ne contiennent aucun accord.
- Générer le code LilyPond nécessaire pour représenter les accords saisis.
- Déterminer comment les accords doivent cohabiter avec le `DrumStaff` existant : portée séparée, voix parallèle, ou export harmonique optionnel.
- Valider les accords saisis avant la génération.
- Produire des messages d’erreur compréhensibles lorsqu’un accord est invalide.

### 2.4. Points à clarifier avant développement

- Définir la syntaxe d’accord acceptée : noms français, noms anglais, notation LilyPond, ou format interne.
- Déterminer si les accords doivent produire un rendu MIDI/WAV ou seulement une partition LilyPond.
- Déterminer si les accords doivent être visibles dans une portée distincte ou intégrés à la portée existante.
- Définir la règle exacte pour les signatures complexes comme `7/8`, `11/16` ou `27/16`.
- Définir le comportement lorsqu’un nombre de mesures est modifié après la saisie des accords par mesure.

## v0.3.0 — Amélioration musicale du click track

Objectif : enrichir la logique musicale du métronome programmable.

- Choix du son pour le premier temps.
- Choix du son pour les temps secondaires.
- Accentuation configurable par subdivision.
- Patterns personnalisés par mesure.
- Subdivisions internes : croches, doubles croches, triolets, quintuplets.
- Support des mesures composées avec groupements visuels, par exemple `3+2+2/8`.
- Export d’un aperçu textuel du pattern.

## v0.4.0 — Expérience utilisateur

Objectif : rendre l’application plus agréable et plus sûre.

- Prévisualisation de la séquence avant génération.
- Bouton de lecture rapide du WAV généré.
- Barre de progression pendant les appels externes.
- Journal détaillé des commandes exécutées.
- Préférences utilisateur persistantes.
- Détection automatique de SoundFonts courants.
- Meilleure validation en temps réel des champs.
- Panneau de configuration pour les chemins de LilyPond, FluidSynth, TiMidity et SoundFont.

## v0.5.0 — Architecture audio avancée

Objectif : améliorer la production audio.

- Choix du moteur audio : FluidSynth, TiMidity, autre backend.
- Choix de la fréquence d’échantillonnage.
- Choix du format de sortie : WAV, FLAC, AIFF, MP3 via outil externe optionnel.
- Normalisation du volume.
- Génération stéréo ou mono.
- Export séparé par segment.

## v0.6.0 — Édition avancée de projet

Objectif : permettre une écriture plus proche d’une structure de pièce.

- Nommer les segments : intro, couplet, pont, solo, outro.
- Copier/coller des rangées.
- Réordonner les rangées par glisser-déposer.
- Templates de structures courantes.
- Import/export CSV.
- Support des commentaires dans le projet.

## v1.0.0 — Version stable

Objectif : stabiliser l’API interne, le format `.gen` et l’expérience utilisateur.

- Format `.gen` documenté et versionné.
- Suite de tests automatisés.
- Documentation utilisateur complète.
- Paquets d’installation pour Windows, macOS et Linux.
- Publication officielle des binaires.
- Licence, contribution et gouvernance clarifiées.

## Idées futures

- Export MusicXML.
- Export Reaper / DAW markers.
- Export Ableton tempo map.
- Mode ligne de commande sans interface graphique.
- Bibliothèque Python réutilisable indépendamment de la GUI.
- Synchronisation avec des pistes audio existantes.
- Génération de click tracks polymétriques.
- Support de claves, patterns latins et ostinatos de percussion.
- Internationalisation français / anglais.
