# Régimes de preuve — v0

Chaque dimension d'un score porte deux étiquettes orthogonales — **source** et **zone**. Elles disent
*si* et *comment* un tiers peut reproduire la dimension.

## Source
- `recalculable` — re-dérivable depuis l'état public on-chain au bloc épinglé (un tiers reproduit le calcul).
- `attested` — fait off-chain signé et tracé (preuve par attestation, non re-dérivable depuis la seule chaîne).

Miroir on-chain : un énuméré `ProofRegime { Recalculable, Attested }` accompagne l'attestation signée.
C'est une **étiquette d'origine, jamais un droit** : un fait `attested` ne relâche aucune borne ; la
vérification on-chain ne lit que les faits bruts publics.

## Zone
- `public` — forme + inputs recalculables par un tiers (ce que décrit cette spécification).
- `private` — pondération propriétaire, **hors** de la forme publique recalculable.

La spécification publie la **forme** — `score = 100 − somme(pénalités par dimension)` — et étiquette,
dimension par dimension, où passe la frontière `public` / `private`. Elle ne contient **aucune valeur de
pondération privée** : une dimension `zone=private` est **nommée et localisée, jamais détaillée**.

## Table de dimensions (forme publique, exemple)
| dimension | source | zone | s'applique à |
|---|---|---|---|
| ratio disponible | recalculable | public | marchés de prêt |
| utilisation | recalculable | public | marchés de prêt |
| déviation de peg | recalculable | public | stablecoins |
| liquidité on-chain | recalculable | public | stablecoins |
| propagation de régime | recalculable | **private** | marchés dépendant d'un stablecoin sous-jacent |

Un score est **conforme** s'il publie sa forme et ses inputs `public/recalculable`, et déclare (sans la
détailler) la frontière `private`. La recalculabilité d'un tiers porte sur les dimensions `public`.
