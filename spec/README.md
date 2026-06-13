# ALIA — spécification de la couche d'instrumentation (v0)

> Spécification publique, recalculable. **Conditions identiques pour tout implémenteur : aucune
> implémentation n'a de statut privilégié.** La couche neutre publie une grammaire et une procédure
> de vérification ; n'importe qui peut produire, ancrer et vérifier un journal conforme — aux mêmes
> conditions, sans permission ni confiance dans l'émetteur.

## Contenu
- [`journal_schema.md`](journal_schema.md) — schéma du journal d'outcomes (12 champs, types, sémantique outcome@t+k).
- [`proof_regimes.md`](proof_regimes.md) — régimes de preuve : source (recalculable / attested) · zone (public / private).
- [`anchoring_format.md`](anchoring_format.md) — format d'ancrage : racine, chaînage, ancrage on-chain, procédure de vérification pas-à-pas.
- [`conformity_vectors.json`](conformity_vectors.json) — vecteurs de conformité minimaux (3 valides, 3 invalides), recalculables avec `sha256`.

## Principe
La spécification décrit la **forme publique** et **où passe la frontière** entre ce qui est recalculable
par un tiers et ce qui ne l'est pas. Elle ne contient aucune pondération privée, aucun secret. Un score
ou un ancrage est *conforme* si et seulement s'il satisfait cette grammaire — vérifiable par recalcul.
