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
- Maintenir la compatibilité du format `.gen` avec les projets contenant des accords symboliques.

### Éléments déjà intégrés dans 0.1.3

- Icône de menu `☰` au bout de chaque ligne.
- Option **Accord au début de chaque ligne**.
- Saisie d’accords selon la notation A, B, C, D, E, F, G.
- Conversion automatique des accords vers LilyPond.
- Choix d’instrument : Piano, Strings et Guitare sèche.
- Rendu strummé/arpégé pour la Guitare sèche.

## v0.2.0 — Accords par mesure et enrichissement harmonique — réalisé

Objectif : permettre à l’utilisateur de définir une progression harmonique différente dans chaque mesure d’une ligne.

### Éléments intégrés

- Ajout de l’option **Accord au début de chaque mesure** dans le menu `☰`.
- Affichage dynamique d’une case de saisie par mesure.
- Mise à jour automatique du nombre de cases lorsque le nombre de mesures change.
- Conservation des valeurs saisies lorsque la zone est simplement masquée avec `⌃`.
- Saisie d’un accord différent dans chaque case.
- Interprétation d’une case vide comme une mesure sans accord.
- Durée automatique de chaque accord égale à une mesure complète, y compris pour les signatures asymétriques.
- Affichage de chaque symbole au-dessus de la mesure correspondante dans le PDF.
- Génération audio mesure par mesure sur la portée harmonique.
- Génération de diagrammes de guitare mesure par mesure lorsque disponibles.
- Extension rétrocompatible du format `.gen` avec `chord_mode` et `measure_chords`.
- Tests unitaires et de non-régression pour la sauvegarde et la génération LilyPond.

### Interprétation générique des accords `addX`

- Compréhension de `add2`, `add4`, `add6`, `add9`, `add11`, `add13` et d’autres degrés positifs.
- Prise en charge des degrés altérés comme `addb9`, `add#9`, `add#11` et `addb13`.
- Application d’un ajout à une qualité existante, par exemple `Cmadd9` ou `C7add13`.
- Acceptation des formes parenthésées comme `D(add11)`.
- Calcul algorithmique des intervalles au lieu d’une table exhaustive d’accords.
- Tests unitaires et messages d’erreur dédiés.


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
