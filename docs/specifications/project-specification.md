# Spécification du projet

## Objectif

GNU TrackGenerator génère des pistes de métronome programmables et reproductibles à partir de segments musicaux. Chaque segment définit un tempo, une signature rythmique, un nombre de mesures et, optionnellement, un accord harmonique répété à chaque mesure.

## Hors périmètre actuel

- Édition complète de partitions.
- Station audionumérique intégrée.
- Choix avancé de banques de sons par instrument.
- Accords différents pour chaque mesure d’une même ligne, prévu pour une version ultérieure.
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

## Accords supportés

| Notation | Degrés |
|---|---|
| `C5` | `1, 5` |
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

Le format `.gen` est un JSON contenant les segments. Les champs `chord_symbol` et `chord_instrument` sont optionnels.

```json
{
  "app": "GNU TrackGenerator",
  "version": "0.1.3",
  "soundfont_path": null,
  "segments": [
    {
      "bpm": 120,
      "numerator": 4,
      "denominator": 4,
      "measures": 8,
      "chord_symbol": "C7#9",
      "chord_instrument": "acoustic_guitar"
    }
  ]
}
```

## Critères d’acceptation

- Un accord `C7#9` est converti en `<c e g bes ees'>`.
- Une ligne en `7/8` avec accord produit des accords de durée `1*7/8`.
- Une ligne en Guitare sèche produit un accord avec `\arpeggio`.
- Un projet sans accord continue de générer seulement la portée de click.
- La conversion MIDI vers WAV tente TiMidity avant FluidSynth.


## Affichage PDF des accords

- Tout accord défini sur une ligne doit être imprimé au-dessus de la partition PDF sous forme de symbole textuel exact.
- Le symbole est placé sur le premier coup de click de chaque mesure répétée par la ligne.
- La portée d’accords continue de produire le rendu MIDI/WAV selon l’instrument choisi.
- Si l’instrument choisi est `acoustic_guitar`, le fichier LilyPond inclut `predefined-guitar-fretboards.ly` et ajoute une ligne `FretBoards` lorsque le symbole d’accord peut être converti en diagramme prédéfini.
- Si le diagramme de guitare n’est pas disponible, la génération ne doit pas échouer : le symbole textuel demeure visible au-dessus de la partition.
