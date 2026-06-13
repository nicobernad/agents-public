# Format d'ancrage — v0

La grammaire que **tout ancrage conforme doit parler**. Un ancrage conforme lie un *journal* à une
*preuve d'intégrité publique sur Base* que n'importe qui peut recalculer et vérifier — sans confiance
dans l'émetteur.

## 0. Identifiant de sujet (canonique)
Le sujet d'une entrée est identifié par un identifiant **déterministe et permissionless** :

    subjectId = keccak256( abi.encode( uint256 chainId, address registry, address subject ) )

Identique bit-à-bit en Solidity, Python et via les outils EVM standard. Aucune création gardée n'est
requise : posséder un `subjectId`, c'est le calculer. Une identité **sans journal ne pèse rien**.

## 1. Racine (entry_hash)
Chaque entrée de journal est un objet JSON. Sa **racine** est :

    entry_hash = sha256( json_canonical( entrée_sans_le_champ_entry_hash ) )

où `json_canonical` = sérialisation JSON **déterministe** : clés triées (`sort_keys=True`) et séparateurs
compacts (`(",", ":")`, sans espaces), encodage UTF-8. Résultat = 64 hexadécimaux (sha256).

## 2. Chaînage (prev_hash)
Chaque entrée porte `prev_hash` = la racine `entry_hash` de l'entrée précédente. La genèse a `prev_hash`
= 64 zéros. La continuité de la chaîne est ainsi vérifiable de bout en bout.

## 3. Ancrage on-chain (Base)
La racine `entry_hash` (bytes32) est enregistrée sur Base par une transaction. Deux formes conformes :
- **événement** : un contrat enregistre la racine et émet `Anchored(address anchor, bytes32 entryHash, uint256 seq)` — `entryHash` = la racine ;
- **calldata** : la racine est portée en calldata, préfixée du marqueur `ALIA-FQR1:` (forme minimale, sans contrat).

L'ancrage **ne requiert aucune permission** de la couche neutre : n'importe qui poste sa propre
transaction. La couche neutre est **lecteur-vérifieur, pas guichet**.

## 4. Procédure de vérification (pas-à-pas, recalculable)
Étant donné une entrée de journal et une transaction Base :
1. Retirer le champ `entry_hash` de l'entrée.
2. Sérialiser en JSON canonique (clés triées, séparateurs compacts, UTF-8).
3. Calculer `sha256` → comparer au `entry_hash` revendiqué. **Doit être égal.**
4. Vérifier que cette racine `bytes32` apparaît dans la transaction Base citée (événement `Anchored.entryHash`, ou calldata après `ALIA-FQR1:`).
5. Vérifier `prev_hash` = `entry_hash` de l'entrée précédente (continuité de chaîne).

Un ancrage est **conforme** ssi 3, 4 et 5 passent. Voir [`conformity_vectors.json`](conformity_vectors.json)
pour des exemples valides et invalides, recalculables avec `sha256` seul.
