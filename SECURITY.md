# Politique de sécurité

La sécurité du projet dépend d’une divulgation responsable, coordonnée et respectueuse des utilisateurs.

## Ne pas publier de vulnérabilité critique dans un ticket public

Si vous pensez avoir découvert une faille de sécurité, ne créez pas de ticket public et ne publiez pas de preuve d’exploitation détaillée dans les discussions, demandes de tirage ou réseaux sociaux.

Cela inclut notamment :

- exécution de code non autorisée ;
- élévation de privilèges ;
- fuite de secrets ou de données personnelles ;
- contournement d’authentification ou d’autorisation ;
- corruption de données ;
- vulnérabilité exploitable à distance ;
- preuve d’exploitation permettant de reproduire immédiatement l’attaque.

## Signalement privé

Envoyer le rapport à : `[security@example.org]`

Si disponible, chiffrer le message avec la clé PGP suivante :

```text
[Coller ici la clé publique PGP ou indiquer le lien officiel]
```

Objet recommandé :

```text
[SECURITY] Rapport privé — description courte
```

## Informations à inclure

Un bon rapport de sécurité inclut :

- version ou commit concerné ;
- environnement utilisé ;
- description claire du risque ;
- étapes de reproduction minimales ;
- impact potentiel ;
- preuve de concept limitée, si nécessaire ;
- correctif suggéré, si disponible ;
- coordonnées pour suivi ;
- préférence de reconnaissance publique ou d’anonymat.

Ne joignez pas de données personnelles ou de secrets réels. Utilisez des exemples synthétiques lorsque possible.

## Cycle de traitement

Le cycle habituel est :

1. Accusé de réception privé lorsque possible.
2. Évaluation initiale de la portée et de la gravité.
3. Reproduction ou demande d’informations supplémentaires.
4. Préparation d’un correctif dans un espace privé ou discret si nécessaire.
5. Publication d’une version corrigée.
6. Publication d’un avis de sécurité avec crédits appropriés, si applicable.
7. Fermeture coordonnée du rapport.

## Délais

Les mainteneurs font un effort raisonnable pour traiter les signalements sérieux rapidement, mais le projet ne garantit pas de délai contractuel.

Les vulnérabilités activement exploitées ou à impact élevé sont priorisées.

## Versions supportées

| Version | Support sécurité |
|---|---|
| `main` | Support raisonnable, selon capacité mainteneurs |
| Dernière version stable | Support prioritaire |
| Anciennes versions | Meilleur effort seulement |

## Publication responsable

Merci de laisser aux mainteneurs un délai raisonnable pour analyser et corriger la vulnérabilité avant toute divulgation publique.

Si vous avez l’intention de publier vos recherches, coordonnez la date de publication avec l’équipe de maintenance afin de protéger les utilisateurs.

## Hors périmètre

Sont généralement hors périmètre :

- attaques nécessitant un accès administrateur complet à la machine ;
- vulnérabilités dans des dépendances déjà documentées sans impact démontré sur le projet ;
- déni de service purement théorique ;
- rapports automatisés sans reproduction ;
- divulgation de chemins locaux non sensibles ;
- problèmes déjà publiquement corrigés dans la dernière version.
