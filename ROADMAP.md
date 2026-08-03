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
- ✅ **Réalisé en v0.5.1** — commande **Rétablir** avec `Ctrl+Y` ou `Ctrl+Maj+Z`.
- ✅ **Réalisé en v0.5.0** — centralisation des modifications dans un historique réversible borné à 100 états.
- ✅ **Vérifié et couvert en v0.6.2** — Annuler/Rétablir pour :
  - ajout et suppression d’une ligne;
  - modification du tempo, de la signature et du nombre de mesures;
  - modification des accords;
  - changement du mode d’accord;
  - réglages d’arpégiateur;
  - duplication et déplacement de lignes;
  - activation ou désactivation globale du click track.
- ✅ **Réalisé en v0.6.2** — validation centralisée du schéma des instantanés et tests empêchant l’oubli silencieux d’un champ éditable.
- ✅ **Réalisé en v0.5.0** — historique limité à 100 états pour maîtriser la mémoire.
- ✅ **Réalisé en v0.5.0** — réinitialisation de l’historique lors de l’ouverture d’un autre projet.
- ✅ **Réalisé en v0.6.3** — limite de l’historique configurable dans **Édition → Options** :
  - `100` conservé comme valeur par défaut;
  - choix de `1` à `10000` états;
  - préférence enregistrée entre les sessions;
  - validation et explication de l’impact potentiel sur la mémoire;
  - réduction immédiate et propre des piles existantes en supprimant les états les plus anciens.

### 2. Menu **Fichier**

- ✅ **Réalisé en v0.6.4** — menu standard regroupant :
  - **Ouvrir…** pour charger un projet `.gen`;
  - **Enregistrer** pour sauvegarder dans le fichier courant;
  - **Enregistrer sous…** pour choisir un nouveau nom ou emplacement;
  - **Exporter…** pour générer les fichiers `.gen`, `.ly`, `.pdf`, `.mid`, `.wav` et les journaux.
- ✅ **Réalisé en v0.6.4** — raccourcis `Ctrl+O`, `Ctrl+S` et `Ctrl+Maj+S`, avec équivalents macOS.
- ✅ **Réalisé en v0.6.4** — mémorisation du fichier courant après ouverture ou enregistrement sous.
- Ajouter la commande **Quitter** à la fin du menu **Fichier** :
  - prévoir le raccourci usuel `Alt+F4` sous Windows/Linux et `Cmd+Q` sur macOS lorsque pertinent;
  - fermer directement lorsque le projet ne contient aucune modification non enregistrée;
  - utiliser exactement la même procédure lorsque l’utilisateur clique sur le bouton de fermeture `X` de la fenêtre.
- Avant toute fermeture d’un projet modifié, afficher une boîte de dialogue proposant :
  - **Enregistrer** : sauvegarder dans le fichier courant, ou ouvrir **Enregistrer sous…** pour un nouveau projet, puis quitter uniquement si la sauvegarde réussit;
  - **Ne pas enregistrer** : quitter sans écrire les changements;
  - **Annuler** : interrompre complètement la fermeture et revenir au projet.
- Empêcher la fermeture si l’utilisateur annule le sélecteur de fichier ou si la sauvegarde échoue.
- Centraliser le traitement de fermeture dans une seule méthode appelée par **Fichier → Quitter**, `Alt+F4`/`Cmd+Q` et le protocole de fenêtre `WM_DELETE_WINDOW`.

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
- Ajouter un réglage **Nombre maximal d’états de l’historique** :
  - valeur par défaut : `100`;
  - valeur persistante entre les sessions;
  - contrôle numérique avec limites raisonnables;
  - indication de l’incidence possible sur l’utilisation de la mémoire.
- Enregistrer les préférences utilisateur dans un fichier de configuration distinct du projet `.gen`.
- Prévoir la même architecture pour les chemins de :
  - LilyPond;
  - TiMidity;
  - FluidSynth;
  - autres outils externes futurs.
- Valider les chemins au moment de leur saisie et afficher un diagnostic compréhensible.

### 5. Menu **Fenêtre → Palette Historique**

Créer une palette d’historique inspirée des logiciels de création comme Photoshop.

- Ajouter un menu **Fenêtre**.
- Ajouter la commande **Palette Historique**.
- Afficher la palette dans une fenêtre flottante ou un panneau pouvant rester ouvert.
- Présenter les états dans l’ordre chronologique, avec :
  - le nom de l’action;
  - un numéro d’étape;
  - l’heure de l’action, lorsque disponible;
  - une indication claire de l’état actuellement actif.
- Permettre de sélectionner directement un état antérieur ou ultérieur.
- Restaurer l’ensemble du projet tel qu’il était à l’état choisi :
  - lignes;
  - tempos et signatures;
  - accords;
  - grilles rythmiques;
  - arpégiateurs;
  - réglages de génération pertinents.
- Prévenir clairement l’utilisateur lorsqu’une nouvelle modification effectuée depuis un ancien état supprimera la branche de rétablissement.
- Permettre de nommer ou de marquer certains états importants comme points de repère.
- Ajouter une option facultative pour sauvegarder l’historique :
  - avec le projet `.gen`; ou
  - dans un fichier compagnon versionné;
  - sans imposer cette sauvegarde aux projets qui doivent demeurer légers.
- Restaurer l’historique sauvegardé lors de la réouverture du projet, lorsque cette option est activée.
- Prévoir une stratégie de migration et de validation afin qu’un historique ancien ou endommagé ne rende jamais le projet principal illisible.
- Respecter la limite d’historique configurée dans **Édition → Options**.
- Permettre de vider l’historique après confirmation.

### 6. Menu **?**

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
- La limite d’historique configurée est restaurée après redémarrage et appliquée sans corruption des états existants.
- `Ctrl+Z` restaure réellement l’état précédent et `Ctrl+Y` ou `Ctrl+Maj+Z` rétablit l’état suivant sans corrompre les listes d’accords ou d’arpégiateurs.
- La palette Historique permet d’atteindre directement un état choisi et, lorsque l’option est activée, de retrouver l’historique sauvegardé après réouverture du projet.

---

## Priorité 2 — v0.6.0 : édition et organisation de la séquence musicale

**Objectif :** permettre de construire et réorganiser rapidement une séquence sans ressaisir son contenu.

### 1. Dupliquer une ligne

- ✅ **Réalisé en v0.6.0** — bouton **D** de duplication placé directement à droite du bouton `−`.
- ✅ **Réalisé en v0.6.0** — copie intégrale et indépendante du contenu de la ligne :
  - BPM;
  - signature rythmique;
  - nombre de mesures;
  - état du click track;
  - mode d’accord;
  - accords par ligne, par mesure ou par grille;
  - instrument;
  - réglages d’arpégiateur;
  - futurs réglages de strum.
- ✅ **Réalisé en v0.6.0** — insertion de la copie immédiatement sous la ligne d’origine.
- ✅ **Réalisé en v0.6.0** — la copie est indépendante : la modifier ne modifie pas l’original.
- ✅ **Réalisé en v0.6.0** — action compatible avec **Annuler** et **Rétablir**.

### 2. Réordonner les lignes

- ✅ **Réalisé en v0.6.0** — poignée `⠿` à droite de chaque ligne.
- ✅ **Réalisé en v0.6.0** — déplacement par cliquer-glisser vers la position voulue.
- ✅ **Réalisé en v0.6.0** — déplacement de la ligne avec tout son contenu, sans désynchroniser les accords ou les réglages d’arpégiateur.
- ✅ **Réalisé en v0.6.0** — mise à jour de l’ordre sauvegardé dans le fichier `.gen`.
- ✅ **Réalisé en v0.6.0** — un glisser-déposer complet correspond à une seule étape Annuler/Rétablir.
- Prévoir ultérieurement le défilement automatique lorsque le pointeur approche du haut ou du bas d’une longue séquence.
- Prévoir des commandes clavier ou boutons Monter/Descendre pour l’accessibilité.

### 3. Désactiver le click track

- ✅ **Réalisé en v0.6.1** — interrupteur global **Click track du projet**.
- ✅ **Réalisé en v0.6.1** — désactivation de toutes les percussions de métronome pour l’ensemble du projet.
- ✅ **Réalisé en v0.6.1** — conservation des tempos, signatures, mesures, accords et arpégiateurs.
- ✅ **Réalisé en v0.6.1** — sauvegarde de l’état dans le format `.gen` avec rétrocompatibilité des anciens projets.
- ✅ **Réalisé en v0.6.1** — intégration à Annuler et Rétablir.
- Prévoir ultérieurement une automation du click track ou des changements d’état à des points précis de la séquence, si un besoin musical clair est confirmé.

### Critères de réalisation

- Une ligne complexe peut être dupliquée et déplacée sans perte d’information.
- L’ordre affiché correspond exactement à l’ordre exporté.
- La désactivation globale du clic ne modifie pas la durée des accords ni la carte de tempo.
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

## v0.5.0–0.5.1 — Historique d’édition réversible

- Commande **Annuler** dans le menu Édition.
- Commande **Rétablir** dans le menu Édition.
- Raccourcis `Ctrl+Z`, `Ctrl+Y` et `Ctrl+Maj+Z`, avec boutons dédiés.
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

## v0.6.0 — Duplication et réorganisation des lignes

- Duplication complète d’une ligne avec le bouton **D** placé à droite du bouton `−`.
- Copie profonde et indépendante des données imbriquées.
- Déplacement des lignes par cliquer-glisser avec une poignée dédiée.
- Ordre de séquence conservé dans les sauvegardes et les exports.
- Compatibilité complète avec Annuler et Rétablir.

## v0.6.3 — Limite d’historique configurable

- Menu **Édition → Options**.
- Limite configurable de `1` à `10000`, avec `100` par défaut.
- Persistance de la préférence entre les sessions.
- Redimensionnement immédiat des piles en conservant les états les plus récents.
- Information sur l’incidence potentielle d’une grande limite sur la mémoire.

## v0.6.2 — Consolidation Annuler/Rétablir

- Validation explicite des instantanés de projet et de ligne.
- Couverture automatisée de toutes les actions éditables annoncées.
- Vérification du branchement des champs, modes, arpégiateurs et actions structurelles vers l’historique.
- Détection immédiate des instantanés incomplets avant restauration.

## v0.6.1 — Activation globale du click track

- Interrupteur global pour activer ou désactiver le métronome.
- Persistance du réglage dans le projet `.gen`.
- Conservation de la structure temporelle et des parties harmoniques en mode silencieux.
- Intégration à l’historique Annuler/Rétablir.

---

## v0.6.4 — Menu Fichier standard

- Commandes Ouvrir, Enregistrer, Enregistrer sous et Exporter regroupées dans le menu Fichier.
- Raccourcis clavier usuels pour l’ouverture et la sauvegarde.
- Suivi du fichier `.gen` courant et titre de fenêtre mis à jour.
- Suppression des anciens boutons de projet redondants.

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
