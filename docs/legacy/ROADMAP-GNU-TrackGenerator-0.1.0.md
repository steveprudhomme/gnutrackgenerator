# ROADMAP — GNU TrackGenerator

Ce document présente les pistes d'évolution envisagées pour GNU TrackGenerator. Il ne constitue pas une promesse contractuelle : les priorités pourront évoluer selon les besoins des utilisateurs, les contributions et la stabilité technique.

## v0.1.0 — Base fonctionnelle

Objectif : fournir une première application utilisable localement.

- Interface graphique CustomTkinter.
- Rangées dynamiques de segments musicaux.
- Champs BPM, signature rythmique et nombre de mesures.
- Sauvegarde et chargement `.gen`.
- Génération `.ly`, `.mid`, `.wav`.
- Pipeline LilyPond + FluidSynth / TiMidity.
- Gestion des erreurs de base.

## v0.2.0 — Amélioration musicale

Objectif : enrichir la logique de click track.

- Choix du son pour le premier temps.
- Choix du son pour les temps secondaires.
- Accentuation configurable par subdivision.
- Patterns personnalisés par mesure.
- Subdivisions internes : croches, doubles croches, triolets, quintuplets.
- Support des mesures composées avec groupements visuels, par exemple `3+2+2/8`.
- Export d'un aperçu textuel du pattern.

## v0.3.0 — Expérience utilisateur

Objectif : rendre l'application plus agréable et plus sûre.

- Prévisualisation de la séquence avant génération.
- Bouton de lecture rapide du WAV généré.
- Barre de progression pendant les appels externes.
- Journal détaillé des commandes exécutées.
- Préférences utilisateur persistantes.
- Détection automatique de SoundFonts courants.
- Meilleure validation en temps réel des champs.

## v0.4.0 — Architecture audio avancée

Objectif : améliorer la production audio.

- Choix du moteur audio : FluidSynth, TiMidity, autre backend.
- Choix de la fréquence d'échantillonnage.
- Choix du format de sortie : WAV, FLAC, AIFF, MP3 via outil externe optionnel.
- Normalisation du volume.
- Génération stéréo ou mono.
- Export séparé par segment.

## v0.5.0 — Édition avancée de projet

Objectif : permettre une écriture plus proche d'une structure de pièce.

- Nommer les segments : intro, couplet, pont, solo, outro.
- Copier/coller des rangées.
- Réordonner les rangées par glisser-déposer.
- Templates de structures courantes.
- Import/export CSV.
- Support des commentaires dans le projet.

## v1.0.0 — Version stable

Objectif : stabiliser l'API interne, le format `.gen` et l'expérience utilisateur.

- Format `.gen` documenté et versionné.
- Suite de tests automatisés.
- Documentation utilisateur complète.
- Paquets d'installation pour Windows, macOS et Linux.
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
