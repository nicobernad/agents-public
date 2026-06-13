# Schéma du journal d'outcomes — v0

Spécification publique. Tout journal conforme émet ces 12 champs. Le schéma est une **contrainte de
forme** : un journal qui naît sans ces champs paie un retrofit en cohérence.

> **Statut — v0 (niveau 12 champs).** Ce schéma précède la section « racines de la preuve d'outcome » du
> schéma canonique ; sa synchronisation est **différée à une décision dédiée**.

## Champs (12)
| # | Champ | Type | Description |
|---|---|---|---|
| 1 | score publié | nombre | la valeur de qualité publiée à `t` |
| 2 | millésime | chaîne | version de la recette / forme sous laquelle le score est calculé |
| 3 | horodatage | ISO-8601 UTC + bloc | `t` (temps + hauteur de bloc de référence, **finalisé**) |
| 4 | sujet | identifiant | le sujet évalué (identifiant canonique, cf. `anchoring_format.md` §0) |
| 5 | fonction | énumération | quelle fonction a produit le signal |
| 6 | flag | énumération | le signal levé |
| 7 | intervention | booléen | le signal a-t-il été suivi d'action ? |
| 8 | action du sujet | optionnel | si partagée volontairement par le sujet |
| 9 | outcome à t+k | nombre + `k` | l'outcome réalisé à `t+k`, comparé au score@`t` |
| 10 | strate | identifiant | la maille de stratification de l'échantillon |
| 11 | provenance | énumération | origine de l'échantillon : `production` (flux réel) · `evaluation` (flux d'évaluation contrôlé) |
| 12 | référence beacon | identifiant | le tirage d'aléa public attaché à l'échantillon |

## Sémantique outcome@t+k (champ 9)
La comparaison `t → t+k` est ce qui rend le score **falsifiable** : on confronte la valeur publiée à `t`
à l'outcome réalisé à `t+k`. De là se dérivent faux-positifs / faux-négatifs et lead-time. Le mécanisme
de remplissage différé (à `t+k`) est laissé à l'implémenteur ; le champ est **prévu par le schéma dès
`t`** pour éviter le retrofit.

## Discipline
Brut avant interprétation : un champ non capturé est **nommé absent**, jamais comblé. La forme (12
champs) prime ; un journal partiel déclare ses champs manquants plutôt que de les simuler.
