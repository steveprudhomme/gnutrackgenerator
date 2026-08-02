# ROADMAP — GNU TrackGenerator

Ce document présente les orientations de développement envisagées pour GNU TrackGenerator. Il ne constitue pas une promesse contractuelle : les priorités peuvent évoluer selon les besoins des utilisateurs, les contributions, la stabilité technique et les décisions de gouvernance.

## Principes de priorisation

Les fonctionnalités sont classées selon quatre critères :

1. **Fondations techniques** : gestion fiable de l’état du projet, de l’historique et des préférences.
2. **Productivité d’édition** : réduction des manipulations répétitives et prévention des pertes de données.
3. **Valeur musicale** : enrichissement des possibilités de composition et d’interprétation.
4. **Dépendances** : une fonctionnalité est placée après les mécanismes dont elle dépend.

Les versions et leur contenu restent indicatifs. Une fonctionnalité peut être déplacée si sa complexité ou ses dépendances l’exigent.

---

# Priorités à venir

## Priorité 1 — v0.5.x : navigation, persistance et historique d’édition

**Objectif :** rendre l’application plus sûre et plus conforme aux conventions d’un logiciel de bureau avant d’ajouter d’autres outils d’édition.

### 1. Historique d’édition

- ✅ **Réalisé en v0.5.0** — commande **Annuler** avec le raccourci `Ctrl+Z`.
- Prévoir également **Rétablir** avec `Ctrl+Y` ou `Ctrl+Maj+Z`.
- ✅ **Réalisé en v0.5.0** — centralisation des modifications dans un historique réversible borné à 100 états.
- Couvrir progressivement les actions suivantes :
  - ajout et suppression d’une ligne;
  - modification du tempo, de la signature et du nombre de mesures;
  - modification des accords;
  - changement du mode d’accord;
  - réglages d’arpégiateur;
  - duplication et déplacement de lignes;
  - activation ou désactivation du click track.
- ✅ **Réalisé en v0.5.0** — historique limité à 100 états pour maîtriser la mémoire.
- ✅ **Réalisé en v0.5.0** — réinitialisation de l’historique lors de l’ouverture d’un autre projet.

### 2. Menu **Fichier**

Regrouper les commandes de projet dans un menu standard :

- **Ouvrir…** : charger un projet `.gen`;
- **Enregistrer** : sauvegarder dans le fichier courant;
- **Enregistrer sous…** : choisir un nouveau nom ou emplacement;
- **Exporter…** : générer les fichiers `.ly`, `.pdf`, `.mid`, `.wav` et les journaux;
- prévoir les raccourcis habituels lorsque pertinents :
  - `Ctrl+O`;
  - `Ctrl+S`;
  - `Ctrl+Maj+S`.

### 3. Nom du projet dans la barre de titre

- Afficher le nom du fichier `.gen` actuellement ouvert dans la barre de titre.
- Utiliser un libellé du type :

```text
GNU TrackGenerator — MonProjet.gen
```

- Ajouter un indicateur visuel lorsque le projet contient des modifications non enregistrées, par exemple :

```text
GNU TrackGenerator — MonProjet.gen *
```

- Afficher **Nouveau projet** tant qu’aucun fichier `.gen` n’a été associé.

### 4. Menu **Édition → Options**

- Déplacer la configuration du SoundFont dans **Édition → Options**.
- Conserver le chemin du SoundFont après la fermeture de l’application.
- Enregistrer les préférences utilisateur dans un fichier de configuration distinct du projet `.gen`.
- Prévoir la même architecture pour les chemins de :
  - LilyPond;
  - TiMidity;
  - FluidSynth;
  - autres outils externes futurs.
- Valider les chemins au moment de leur saisie et afficher un diagnostic compréhensible.

### 5. Menu **?**

- Ajouter un menu **?** ou **Aide**.
- Ajouter une commande **Aide** ouvrant un fichier d’aide intégré.
- Ajouter une commande **À propos** indiquant :
  - le nom du logiciel;
  - la version;
  - la licence GNU GPLv3;
  - les crédits;
  - le lien du dépôt GitHub.
- Créer une documentation d’aide dédiée, par exemple `docs/user/help.md`.

### Critères de réalisation

- Les commandes du menu fonctionnent sans dupliquer la logique déjà présente dans l’interface.
- Le nom et l’état modifié du projet sont toujours cohérents avec le fichier courant.
- Le SoundFont choisi est restauré après redémarrage.
- `Ctrl+Z` restaure réellement l’état précédent sans corrompre les listes d’accords ou d’arpégiateurs.

---

## Priorité 2 — v0.6.0 : édition et organisation de la séquence musicale

**Objectif :** permettre de construire et réorganiser rapidement une séquence sans ressaisir son contenu.

### 1. Dupliquer une ligne

- Ajouter une commande **Dupliquer la ligne**.
- Copier l’intégralité du contenu de la ligne :
  - BPM;
  - signature rythmique;
  - nombre de mesures;
  - état du click track;
  - mode d’accord;
  - accords par ligne, par mesure ou par grille;
  - instrument;
  - réglages d’arpégiateur;
  - futurs réglages de strum.
- Insérer la copie immédiatement sous la ligne d’origine.
- Créer une copie indépendante : modifier la copie ne doit pas modifier l’original.
- Rendre l’action compatible avec **Annuler**.

### 2. Réordonner les lignes

- Ajouter à droite de chaque ligne des commandes permettant de la déplacer.
- Première implémentation recommandée :
  - bouton **Monter**;
  - bouton **Descendre**.
- Une évolution ultérieure pourra ajouter le glisser-déposer.
- Déplacer la ligne avec tout son contenu, sans désynchroniser les accords ou les réglages d’arpégiateur.
- Mettre à jour l’ordre sauvegardé dans le fichier `.gen`.
- Rendre chaque déplacement compatible avec **Annuler**.

### 3. Désactiver le click track

- Ajouter une option permettant de désactiver le click track pour une ligne.
- Lorsque le clic est désactivé :
  - la ligne demeure dans la séquence;
  - les accords, arpèges ou strums peuvent continuer à être générés;
  - la durée et la structure de la ligne demeurent inchangées;
  - aucune percussion de métronome n’est produite pour cette ligne.
- Sauvegarder l’état dans le format `.gen`.
- Afficher clairement l’état désactivé dans l’interface.
- Prévoir éventuellement une commande globale pour désactiver ou réactiver tous les clics.

### Critères de réalisation

- Une ligne complexe peut être dupliquée et déplacée sans perte d’information.
- L’ordre affiché correspond exactement à l’ordre exporté.
- La désactivation du clic ne modifie pas la durée des accords ni la carte de tempo.
- Toutes ces opérations participent à l’historique `Ctrl+Z`.

---

## Priorité 3 — v0.7.0 : contrôles harmoniques globaux et moteur de strumming

**Objectif :** séparer clairement le choix de l’instrument du mode d’interprétation et permettre l’application rapide de réglages à une ligne entière.

### 1. Arpégiateur applicable à toute la ligne

Pour chacun des modes d’accord :

- accord pour toute la ligne;
- accord au début de chaque mesure;
- grille d’accords selon une subdivision rythmique;

ajouter un bouton ou une commande permettant d’appliquer un même réglage d’arpégiateur à tous les accords de la ligne.

Le dialogue devra permettre de choisir :

- activation ou désactivation globale;
- motif;
- nombre d’octaves;
- figure rythmique;
- valeur pointée;
- N-olet;
- portée de l’application :
  - tous les accords;
  - seulement les accords sans réglage personnalisé;
  - seulement les cases sélectionnées, si une sélection multiple est ajoutée.

Les réglages propres à chaque case doivent rester modifiables après l’application globale.

### 2. Bouton **S** et patterns de strum

- Ajouter un bouton **S** sous chaque champ d’accord, à côté du bouton **A**.
- Permettre de choisir entre trois modes d’interprétation mutuellement exclusifs :
  - accord plaqué;
  - arpégiateur;
  - pattern de strum.
- Créer un éditeur de patterns de strum pour guitare, incluant progressivement :
  - coup vers le bas;
  - coup vers le haut;
  - silence;
  - coup étouffé ou percussif;
  - accent;
  - prolongation;
  - répétition du pattern.
- Permettre de choisir la valeur rythmique du pattern.
- Prévoir une représentation compacte, par exemple :

```text
D - D U - U D U
```

où `D` signifie *downstroke*, `U` *upstroke* et `-` une absence d’attaque.

### 3. Séparer l’instrument de l’articulation

- Retirer l’hypothèse selon laquelle choisir **Guitare sèche** implique automatiquement un accord strummé.
- Séparer explicitement :
  - **instrument** : piano, cordes, guitare sèche, etc.;
  - **interprétation** : accord plaqué, arpège ou strum.
- Permettre à une guitare sèche de jouer :
  - un accord plaqué;
  - un arpège;
  - un pattern de strum.
- Permettre éventuellement à d’autres instruments d’utiliser les modes compatibles.

### 4. Sauvegarde et génération

- Étendre le format `.gen` avec des réglages de strum explicites et rétrocompatibles.
- Générer les attaques MIDI correspondant au sens et au rythme des coups.
- Adapter la sortie LilyPond afin de représenter le rythme de strum de façon compréhensible.
- Documenter les limites liées aux SoundFonts, qui ne distinguent pas toujours les coups vers le haut et vers le bas.

### Critères de réalisation

- Un réglage d’arpégiateur peut être propagé à toute une ligne sans éditer chaque case.
- Le bouton **S** n’active pas simultanément l’arpégiateur.
- Le choix **Guitare sèche** n’impose plus automatiquement une articulation.
- Les anciens projets restent lisibles avec un mode d’interprétation par défaut cohérent.

---

## Priorité 4 — v0.8.0 : prévisualisation et expérience audio

**Objectif :** faciliter la vérification du résultat sans quitter l’application.

- Prévisualisation de la séquence avant export.
- Lecture rapide du WAV généré.
- Contrôles lecture, pause et arrêt.
- Barre de progression pendant les appels externes.
- Affichage amélioré du journal de génération.
- Validation en temps réel des accords et des paramètres rythmiques.
- Détection automatique des SoundFonts courants.
- Diagnostic plus précis des fichiers WAV silencieux ou trop faibles.

---

## Priorité 5 — v0.9.0 : audio avancé et formats d’export

**Objectif :** améliorer la qualité et l’interopérabilité des fichiers produits.

- Sélection explicite du moteur audio : TiMidity, FluidSynth ou autre backend.
- Choix de la fréquence d’échantillonnage.
- Sortie mono ou stéréo.
- Normalisation et contrôle du niveau.
- Export WAV, FLAC et AIFF.
- Export MP3 via un outil externe optionnel.
- Export séparé par ligne ou par famille d’instruments.
- Export MusicXML.
- Export de marqueurs ou de cartes de tempo pour les DAW.

---

## v1.0.0 — Version stable

**Objectif :** stabiliser le format de projet, l’expérience utilisateur et la distribution.

- Format `.gen` documenté et versionné.
- Migrations automatiques entre versions du format.
- Suite complète de tests automatisés.
- Documentation utilisateur et fichier d’aide complets.
- Paquets d’installation pour Windows, macOS et Linux.
- Publication officielle des binaires.
- Processus de publication reproductible.
- Licence, contribution et gouvernance maintenues à jour.

---

# Jalons réalisés

## v0.1.x — Socle fonctionnel

- Interface CustomTkinter.
- Segments dynamiques avec tempo, signature et nombre de mesures.
- Pipeline LilyPond, MIDI et WAV.
- Sauvegarde et chargement `.gen`.
- Journal des commandes et diagnostic WAV.
- Accords symboliques et instruments harmoniques.

## v0.2.0 — Accords par mesure et logique `addX`

- Accord distinct pour chaque mesure.
- Durée d’accord adaptée à la signature.
- Affichage des symboles au-dessus de la partition.
- Interprétation générique des accords `addX`.
- Compatibilité ascendante du format `.gen`.

## v0.3.0 — Grille rythmique d’accords

- Changements d’accords à l’intérieur des mesures.
- Calcul exact des cases par subdivision.
- Virgule pour prolonger un accord sans nouvelle attaque.
- Silences par case vide.
- Accords complexes avec altérations parenthésées.

## v0.5.0 — Première commande d’édition réversible

- Commande **Annuler** dans le menu Édition.
- Raccourci `Ctrl+Z` et bouton dédié.
- Historique borné à 100 états.
- Saisie au clavier regroupée en étapes cohérentes.
- Restauration des lignes, accords, champs dynamiques et arpégiateurs.
- Réinitialisation de l’historique à l’ouverture d’un projet.

## v0.4.x — Arpégiateur et stabilisation du parseur

- Arpégiateur configurable par accord.
- Motifs ascendants, descendants et aléatoires.
- Octaves, valeurs pointées et N-olets.
- Correction de la durée totale des groupes N-olets.
- Tolérance de notations comme `C5m`.
- Tests de non-régression pour les progressions complexes.

---

# Idées à plus long terme

- Nommer les segments : intro, couplet, pont, solo, outro.
- Modèles de structures musicales.
- Import et export CSV.
- Commentaires associés aux lignes.
- Mode ligne de commande sans interface graphique.
- Bibliothèque Python réutilisable indépendamment de la GUI.
- Synchronisation avec des pistes audio existantes.
- Click tracks polymétriques.
- Claves, patterns latins et ostinatos de percussion.
- Internationalisation français et anglais.
