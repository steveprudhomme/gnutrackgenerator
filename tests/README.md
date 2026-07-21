# Tests

Ce dossier contient les tests isolés du code de production.

## Structure

- `unit/` : tests unitaires rapides et isolés.
- `integration/` : tests couvrant l’interaction entre composants.
- `regression/` : tests ajoutés après correction de bogues pour empêcher leur retour.

## Règles

- Toute nouvelle fonctionnalité doit être accompagnée de tests.
- Tout bogue corrigé devrait ajouter un test de non-régression.
- Les tests doivent être reproductibles localement et en intégration continue.

## Exécuter les tests unitaires actuels

Depuis la racine du projet :

```bash
PYTHONPATH=src python -m unittest discover -s tests/unit -p "test_*.py"
```

Sous PowerShell :

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests/unit -p "test_*.py"
```
