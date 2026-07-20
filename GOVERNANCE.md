# Gouvernance du projet

Ce document décrit comment les décisions sont prises, comment les rôles évoluent et comment les droits d’écriture sont accordés.

La gouvernance vise trois objectifs :

1. rendre les décisions compréhensibles ;
2. permettre la participation sans chaos ;
3. protéger la viabilité du projet et de ses mainteneurs.


## Principe d’ouverture

Le projet est ouvert à la collaboration publique. Les décisions significatives doivent être discutées dans des lieux accessibles aux contributeurs, sauf exception liée à la sécurité, à la vie privée ou à l’application du code de conduite.

Les mainteneurs doivent favoriser l’intégration progressive des nouvelles personnes : petites tâches, tickets bien cadrés, revues pédagogiques et reconnaissance des contributions non techniques.

## Modèle de gouvernance

Le projet utilise un modèle de **consensus paresseux** appuyé par un **comité de maintenance**.

Par défaut, une proposition raisonnable peut avancer si :

- elle est publique ;
- elle est suffisamment documentée ;
- elle laisse un délai raisonnable de réaction ;
- aucune objection motivée et bloquante n’est soulevée.

Une objection bloquante doit expliquer un risque concret : sécurité, régression, dette technique majeure, incompatibilité de licence, violation du code de conduite, coût de maintenance excessif ou rupture injustifiée pour les utilisateurs.

## Rôles

### Utilisateur ou utilisatrice

Toute personne qui utilise le projet, lit la documentation, signale une difficulté ou pose une question.

Droits :

- ouvrir une discussion ;
- signaler un bogue ;
- demander une fonctionnalité ;
- proposer une amélioration de documentation.

### Contributeur ou contributrice

Personne qui participe activement au projet par du code, de la documentation, des tests, de la traduction, du design, du tri ou du support communautaire.

Droits :

- ouvrir des demandes de tirage ;
- participer aux revues ;
- proposer des orientations ;
- contribuer aux discussions de gouvernance.

Obligations :

- respecter le code de conduite ;
- signer les commits selon le DCO ;
- suivre `CONTRIBUTING.md` ;
- accepter la revue publique.

### Mainteneur ou mainteneuse

Personne ayant la confiance du projet pour examiner, intégrer ou rejeter des contributions.

Droits :

- étiqueter et prioriser les tickets ;
- demander des modifications ;
- fusionner des demandes de tirage ;
- publier des versions selon le processus établi ;
- participer aux décisions de gouvernance.

Obligations :

- agir dans l’intérêt du projet ;
- expliquer les refus importants ;
- appliquer le code de conduite ;
- éviter les décisions opaques ;
- protéger le temps de maintenance ;
- déclarer les conflits d’intérêts pertinents.

### Comité de maintenance

Groupe de mainteneurs responsables des décisions transversales : publication, feuille de route, gouvernance, sécurité, conflits et attribution des droits.

Le comité peut déléguer des responsabilités à des mainteneurs spécialisés.

## Trajectoire vers les droits d’écriture

Une personne peut être invitée à devenir mainteneur ou mainteneuse lorsqu’elle démontre durablement :

- des contributions de qualité ;
- une compréhension de l’architecture ;
- une capacité à faire des revues constructives ;
- une communication respectueuse ;
- une attention à la documentation et aux tests ;
- un respect constant du DCO, de la licence et du code de conduite ;
- une présence fiable, sans exigence de disponibilité permanente.

Processus :

1. Un mainteneur propose la candidature dans un canal de gouvernance documenté.
2. Les mainteneurs discutent des contributions et risques éventuels.
3. En l’absence d’objection bloquante, les droits appropriés sont accordés.
4. Les droits peuvent être progressifs : tri, revue, fusion limitée, publication.
5. La nomination est annoncée publiquement.

## Prise de décision

### Changements mineurs

Exemples : documentation, corrections simples, tests, petits correctifs.

Décision : revue normale et fusion par un mainteneur.

### Changements significatifs

Exemples : nouvelle fonctionnalité, modification d’architecture, changement de format de fichier, nouvelle dépendance majeure.

Décision : ticket ou discussion préalable, puis demande de tirage.

### Changements majeurs

Exemples : rupture de compatibilité, changement de licence, modification de gouvernance, retrait d’une fonctionnalité importante.

Décision : proposition publique, période de commentaires, décision du comité de maintenance.

## Consensus paresseux

Une proposition peut être considérée acceptée si aucun désaccord motivé n’est exprimé après un délai raisonnable.

Délais indicatifs :

- changement mineur : 2 à 5 jours ;
- changement significatif : 7 à 14 jours ;
- changement majeur : 14 à 30 jours.

Ces délais peuvent être raccourcis pour une correction urgente de sécurité.

## Gestion des désaccords

Les désaccords sont normaux. Ils doivent être traités en se concentrant sur :

- les faits ;
- les risques ;
- les utilisateurs touchés ;
- les coûts de maintenance ;
- les alternatives possibles.

Si aucun consensus n’émerge, le comité de maintenance tranche. La décision et sa justification doivent être documentées.

## Conflits d’intérêts

Toute personne impliquée dans une décision doit signaler un conflit d’intérêts pertinent : employeur, client, intérêt financier, relation personnelle ou obligation externe susceptible d’influencer la décision.

Le signalement n’exclut pas automatiquement la participation, mais permet une décision plus transparente.

## Retrait ou suspension des droits

Les droits d’écriture peuvent être suspendus ou retirés en cas de :

- violation grave ou répétée du code de conduite ;
- intégration de changements dangereux sans revue ;
- non-respect répété du processus de sécurité ;
- conflit d’intérêts non déclaré ayant causé un tort ;
- inactivité prolongée si le retrait est nécessaire à la sécurité du projet.

La décision doit être documentée par le comité de maintenance, sauf si la confidentialité est nécessaire pour protéger une personne.

## Publication des versions

Les versions doivent respecter :

- le versionnage sémantique ;
- le changelog ;
- les tests obligatoires ;
- les notes de migration si rupture ;
- la politique de sécurité si un correctif de vulnérabilité est inclus.

## Évolution de cette gouvernance

Ce document peut évoluer. Toute modification substantielle doit être proposée publiquement et approuvée selon le processus des changements majeurs.
