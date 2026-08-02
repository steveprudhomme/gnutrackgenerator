# Spécification du projet

## Objectif

GNU TrackGenerator génère des pistes de métronome programmables et reproductibles à partir de segments musicaux. Chaque segment définit un tempo, une signature rythmique, un nombre de mesures et, optionnellement, soit un accord répété sur toute la ligne, soit un accord indépendant pour chaque mesure, soit une grille d’accords fondée sur une subdivision rythmique. Chaque champ d’accord peut aussi posséder son propre arpégiateur.

## Hors périmètre actuel

- Édition complète de partitions.
- Station audionumérique intégrée.
- Choix avancé de banques de sons par instrument.
- Support exhaustif de toutes les notations d’accords jazz, classiques ou régionales.

## Exigences fonctionnelles

- `REQ-001` — L’utilisateur peut créer au moins une ligne musicale.
- `REQ-002` — Chaque ligne contient un BPM, une signature rythmique et un nombre de mesures.
- `REQ-003` — Chaque ligne possède un menu `☰`.
- `REQ-004` — Le menu de ligne permet d’activer une zone **Accord au début de chaque ligne**.
- `REQ-005` — L’utilisateur peut saisir un accord selon les fondamentales A, B, C, D, E, F, G, avec accidentels `#` ou `b`.
- `REQ-006` — Le moteur convertit les symboles d’accords supportés en notes LilyPond.
- `REQ-007` — L’utilisateur peut choisir l’instrument de l’accord : Piano, Strings ou Guitare sèche.
- `REQ-008` — Les accords de Guitare sèche sont générés avec un rendu strummé/arpégé.
- `REQ-009` — L’accord d’une ligne se répète à chaque mesure de cette ligne.
- `REQ-010` — La durée de l’accord correspond à la longueur complète de la mesure, par exemple `1*7/8` pour une mesure en 7/8.
- `REQ-011` — Le projet se sauvegarde dans un fichier `.gen` compatible JSON.
- `REQ-012` — Le pipeline produit `.gen`, `.ly`, `.mid` et `.wav`.
- `REQ-013` — Le menu de ligne permet d’activer **Accord au début de chaque mesure**.
- `REQ-014` — Le nombre de cases d’accord correspond au nombre de mesures de la ligne.
- `REQ-015` — Chaque accord par mesure peut être différent et dure une mesure complète.
- `REQ-016` — Une case d’accord vide génère une mesure sans accord.
- `REQ-017` — Une modification du nombre de mesures met à jour les cases visibles sans effacer les valeurs encore applicables.
- `REQ-018` — Le menu permet d’activer une grille d’accords selon une subdivision rythmique.
- `REQ-019` — Les subdivisions disponibles sont la blanche, la blanche pointée, la noire, la noire pointée, la croche et les triolets de rondes, blanches, noires et croches.
- `REQ-020` — Le nombre de cases est calculé automatiquement à partir de la durée totale de la ligne.
- `REQ-021` — Une virgule prolonge l’accord précédent sans nouvelle attaque.
- `REQ-022` — Une case vide représente un silence.
- `REQ-023` — Une prolongation traversant une barre de mesure est liée dans la sortie LilyPond.
- `REQ-024` — Chaque champ d’accord possède un bouton **A** ouvrant ses réglages d’arpégiateur.
- `REQ-025` — L’arpégiateur peut être activé ou désactivé sans désactiver l’accord.
- `REQ-026` — Les motifs disponibles sont descendant-montant, montant-descendant et aléatoire.
- `REQ-027` — L’utilisateur peut choisir de 1 à 8 octaves.
- `REQ-028` — Les valeurs disponibles sont double croche, croche, noire, blanche et ronde, avec une option pointée.
- `REQ-029` — Un N-olet est saisi par un nombre N de 3 à 32. La valeur rythmique sélectionnée représente la durée totale du groupe, dans laquelle exactement N notes sont réparties. Lorsque N vaut `0`, la valeur sélectionnée représente la durée de chaque note.
- `REQ-030` — Le motif aléatoire est reproductible pour une même sauvegarde.
- `REQ-031` — Une virgule de continuation conserve l’arpégiateur de l’accord précédent.

## Accords supportés

Le parseur prend en charge une logique générique `addX`. Le suffixe peut être appliqué à un accord majeur implicite (`Dadd11`) ou à une qualité déjà reconnue (`Cmadd9`, `C7add13`). Les degrés altérés comme `add#11` et `addb9` sont également acceptés.

Le parseur prend aussi en charge les modifications parenthésées appliquées à une qualité reconnue, par exemple `G#m7(b13)`, `C7(#9)` ou `C7(b9,#11)`. Plusieurs modifications peuvent être séparées par des virgules. Lorsqu’un degré altéré existe déjà sous une autre forme dans l’accord de base, il est remplacé.

Pour tolérer certaines écritures non standard rencontrées dans des progressions importées, `C5m` et `Cm5` sont interprétés comme `Cm`. La quinte explicite est considérée redondante, tandis que le symbole original reste conservé pour l’affichage.

| Notation | Degrés |
|---|---|
| `C5` | `1, 5` |
| `C5m`, `Cm5` | `1, b3, 5` |
| `C(b5)` | `1, b5` |
| `C` | `1, 3, 5` |
| `Cm` | `1, b3, 5` |
| `Cdim`, `C°` | `1, b3, b5` |
| `Caug`, `C+` | `1, 3, #5` |
| `Csus2` | `1, 2, 5` |
| `Csus4` | `1, 4, 5` |
| `C7sus4` | `1, 4, 5, b7` |
| `Cadd2`, `Cμ` | `1, 2, 3, 5` |
| `Cadd9` | `1, 3, 5, 9` |
| `Dadd11` | `1, 3, 5, 11` |
| `G#m7(b13)` | `1, b3, 5, b7, b13` |
| `Fadd#11` | `1, 3, 5, #11` |
| `Cmadd9` | `1, b3, 5, 9` |
| `C7add13` | `1, 3, 5, b7, 13` |
| `C6` | `1, 3, 5, 6` |
| `Cm6` | `1, b3, 5, 6` |
| `Cmaj7` | `1, 3, 5, 7` |
| `C7` | `1, 3, 5, b7` |
| `Cm7` | `1, b3, 5, b7` |
| `Cm7b5`, `Cø` | `1, b3, b5, b7` |
| `Cdim7` | `1, b3, b5, bb7` |
| `CmM7` | `1, b3, 5, 7` |
| `Cmaj9` | `1, 3, 5, 7, 9` |
| `C9` | `1, 3, 5, b7, 9` |
| `Cm9` | `1, b3, 5, b7, 9` |
| `Cm11` | `1, b3, 5, b7, 9, 11` |
| `C13` | `1, 3, 5, b7, 9, 11, 13` |
| `Cmaj13` | `1, 3, 5, 7, 9, 11, 13` |
| `C7#9` | `1, 3, 5, b7, #9` |

## Exigences non fonctionnelles

- Maintenabilité : séparation entre GUI, modèles, génération et conversion d’accords.
- Portabilité : dépendances Python minimales; LilyPond, TiMidity et FluidSynth restent des dépendances système.
- Robustesse : validation des champs avant génération.
- Compatibilité : les anciens fichiers `.gen` sans accord demeurent lisibles.
- Accessibilité : les erreurs doivent être formulées en langage utilisateur.

## Formats de données

Le format `.gen` est un JSON contenant les segments. Les champs `chord_symbol`, `chord_mode`, `measure_chords`, `chord_grid_unit`, `grid_chords` et `chord_instrument` sont optionnels selon le mode harmonique choisi.

```json
{
  "app": "GNU TrackGenerator",
  "version": "0.4.2",
  "soundfont_path": null,
  "segments": [
    {
      "bpm": 120,
      "numerator": 4,
      "denominator": 4,
      "measures": 4,
      "chord_mode": "measure",
      "measure_chords": ["C", "Am7", "F", "G7"],
      "measure_arpeggiators": [
        {"enabled": true, "pattern": "up_down", "octaves": 2, "rhythm": "eighth", "dotted": false, "tuplet_count": 3},
        {"enabled": false, "pattern": "up_down", "octaves": 1, "rhythm": "eighth", "dotted": false, "tuplet_count": 0},
        {"enabled": true, "pattern": "down_up", "octaves": 1, "rhythm": "sixteenth", "dotted": false, "tuplet_count": 0},
        {"enabled": true, "pattern": "random", "octaves": 2, "rhythm": "quarter", "dotted": true, "tuplet_count": 5}
      ],
      "chord_instrument": "acoustic_guitar"
    }
  ]
}
```



Exemple du mode rythmique :

```json
{
  "bpm": 120,
  "numerator": 4,
  "denominator": 4,
  "measures": 1,
  "chord_mode": "grid",
  "chord_grid_unit": "quarter",
  "grid_chords": ["C", ",", "G", null],
  "grid_arpeggiators": [
    {"enabled": true, "pattern": "up_down", "octaves": 2, "rhythm": "eighth", "dotted": false, "tuplet_count": 0},
    {"enabled": false, "pattern": "up_down", "octaves": 1, "rhythm": "eighth", "dotted": false, "tuplet_count": 0},
    {"enabled": true, "pattern": "random", "octaves": 1, "rhythm": "sixteenth", "dotted": false, "tuplet_count": 5},
    {"enabled": false, "pattern": "up_down", "octaves": 1, "rhythm": "eighth", "dotted": false, "tuplet_count": 0}
  ],
  "chord_instrument": "piano"
}
```

## Critères d’acceptation

- Un accord `C7#9` est converti en `<c e g bes ees'>`.
- La progression `E5 B5 E5 C5m F#5(b5) B5` est entièrement acceptée; `C5m` est interprété comme `Cm`.
- Une ligne en `7/8` avec accord produit des accords de durée `1*7/8`.
- Une ligne en Guitare sèche produit un accord avec `\arpeggio`.
- Une ligne de quatre mesures en mode par mesure sauvegarde exactement quatre entrées dans `measure_chords`.
- Une progression `C`, `Am7`, `F`, `G7` génère quatre accords distincts, chacun avec la durée complète de sa mesure.
- Un projet sans accord continue de générer seulement la portée de click.
- La conversion MIDI vers WAV tente TiMidity avant FluidSynth.
- Quatre mesures en `4/4` divisées en noires produisent 16 cases.
- La séquence `["C", ",", "G", null]` produit un accord C prolongé sur une blanche, un accord G sur une noire et un silence sur une noire.
- Un arpégiateur de croches en `4/4` génère huit attaques par mesure.
- Un triolet de croches génère douze attaques par mesure avec `\tuplet 3/2`.
- Une configuration absente dans un ancien fichier `.gen` est chargée comme arpégiateur désactivé.


## Affichage PDF des accords

- Tout accord défini sur une ligne doit être imprimé au-dessus de la partition PDF sous forme de symbole textuel exact.
- Le symbole est placé sur le premier coup de click de chaque mesure répétée par la ligne.
- La portée d’accords continue de produire le rendu MIDI/WAV selon l’instrument choisi.
- Si l’instrument choisi est `acoustic_guitar`, le fichier LilyPond inclut `predefined-guitar-fretboards.ly` et ajoute une ligne `FretBoards` lorsque le symbole d’accord peut être converti en diagramme prédéfini.
- Si le diagramme de guitare n’est pas disponible, la génération ne doit pas échouer : le symbole textuel demeure visible au-dessus de la partition.
