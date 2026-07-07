# Birth of a Governed Standard

**Deployment ceremonies with on-chain read-back: governance-native genesis, payload determinism, and verifiable dormancy**

Author: [nicobernad](https://github.com/nicobernad)
Date: July 7, 2026 · Network: Base mainnet (chain id 8453)
Related: ERC-8240 — *Trust Infrastructure for Agents and Assets* (Draft; number assigned April 2026, in editor review) — submitted to ethereum/ERCs as PR #1705.

> **STATUS: v1.0 — released July 7, 2026.** Network state anchored to block 48,318,211 (2026-07-07 12:01 UTC).
> Publication rule of this corpus: *never a surclaim in a citable — a claim receives a present proof, or it waits for its wave.* Consequently this document may not be released while (a) any bracketed slot remains unfilled, or (b) any figure present in the text has not been re-anchored firsthand (on-chain read or command re-run at pinned commit) during the pre-publication read-back pass. All empirical values below were re-anchored firsthand on 2026-07-07 (on-chain reads, Base mainnet). **No open slots, no blocking escalation**: author decisions are resolved, and the Sepolia-gas corroboration was dropped — cross-network determinism rests on the gate-3 keccak byte-identity match (firsthand-verified). Nothing here is exempt.

---

## Abstract

We report the method and results of giving birth to an on-chain standard under multisig governance from its first block, across two ceremonies on Base mainnet. The method contributes five practices: (1) **governance-native birth** — a single-use deployer executed by `delegatecall` from a Gnosis Safe, so that every `owner`/`governor`, transferable or not, is the Safe at genesis, with no transfer window; (2) a **no-placeholder rule for immutables**, which decomposes deployment into waves as a consequence rather than a preference; (3) **payload freeze with byte-identity proof** — the mainnet ceremony executed only the frozen payload whose keccak equals the rehearsed gate-3 value (`0xa9571570b6f7b57b40fdcd39dfcc9458c3e2aeb053f27f44b5cf588b4cd25eef`), so the executed payload is provably byte-identical to the rehearsed one (the ceremony consumed 7,679,482 gas); (4) a **read-back protocol** — seventeen post-conditions read from chain twice, by two independent paths — of which this note is itself an instance: every empirical claim below carries an address (or commit), a method, and an expected value; (5) **verifiable dormancy** — the standard's not-yet-active state (attestation quorum threshold = 1, zero sealed transitions since genesis) is published and watched rather than hidden, inverting the usual burden of proof. The reader is not asked to trust any of this; the reader is asked to re-read it.

---

## 1. The problem: deployment as an unverifiable trust event

Most protocol launches are narrated rather than proven. "Live," "governed," "N contracts," "audited" are published as sentences; the reader who wants to check them must reconstruct addresses, guess at ownership, and take activity claims on faith. The asymmetry is structural: the deployer holds all the evidence, the reader holds none, and the gap is filled with reputation.

A *standard* carries a stricter burden than a product. Its credibility is not what it will eventually do but **how it was born**: who owned it at block one, what its immutable constructor arguments received, whether its governance is a fact or a slide, and — critically — whether its inactive state is legible. A standard that cannot yet act, and can be *seen* not to have acted, is in the honest starting position. A standard whose dormancy is invisible is indistinguishable from vaporware.

This note describes a deployment method whose output is not only a set of contracts but a set of **replayable claims**, and it is structured as an instance of its own protocol. Section 7 is a claims table: statement → location → method → expected value. Any reader with an RPC endpoint can replay it. Where a verdict of absence is made ("zero transitions," "no residual capability"), the perimeter that produced it is declared — an absence claim is only as strong as its declared perimeter.

## 2. Method

### 2.1 Governance-native birth

A firsthand read of the codebase (not an assumption) established that part of the surface fixes `owner`/`governor` at construction with **no transfer function** — the deploying address owns those contracts forever. Any deploy-then-transfer pattern would therefore have produced a permanent split: some contracts owned by the Safe, others married to an EOA.

The uniform solution: a **single-use deployer contract** executed via `delegatecall` from a Gnosis Safe. In the delegatecall frame, `msg.sender` is the Safe itself; every child contract — transferable or not — is born with the Safe as owner and governor. No transfer window exists for any contract; there is one auditable path instead of two. The vehicle is inert after the ceremony: the deployer holds no state and no post-ceremony entry point (a stateless-gate — `vm.record` verified zero storage writes in the delegatecall frame, so the ceremony could not corrupt the Safe's own owners/threshold/nonce), and its function performs only child `CREATE`s and wiring in a single shot.

### 2.2 Two domains, one keyring

The standard must not be governed by the address that governs the products built on it. Two Safes were therefore created (2-of-3, the **same three hardware signers** at genesis, distinct addresses):

- **Safe-ALIA** (standard domain) owns ParameterRegistry, VerifyTransition, AIR, AgentThetaJournal — several of which are non-transferable, i.e. this ownership is permanent by construction.
- **Safe-APIS** (operator domain) owns the commercial layer: resolver, PZ-2, PZ-4 (the oracle adapter between the two domains is deliberately ownerless — an immutable, read-only boundary).

The cost was one extra factory transaction and one extra ceremony. The return is that the separation is an **on-chain fact**, checkable in two reads: `journal.owner() == SAFE_ALIA` and `SAFE_APIS != SAFE_ALIA`. We state the genesis honestly: **twin governances — same three humans behind both doors today; divergence is the roadmap, and the structure that permits divergence without touching a contract is what the ceremonies purchased.**

### 2.3 The immutability rule and wave decomposition

Rule, applied without exception: **never a placeholder in an immutable — an immutable constructor argument receives a real, canonical, verified address, or the contract waits for its wave.** A settable may be born unwired if documented (the honest stub).

The rule is not a style preference; it *decomposes* the deployment. Everything wireable-real-and-activatable shipped as **Wave A** (resolver, adapter, PZ-2, PZ-4). Contracts whose immutables would have required placeholders (the matrix/vault/anchor cluster, pending a router) wait as **Wave B**, to be deployed together with their dependency. Consequence: nothing inert, nothing lying, ships to mainnet. External immutables in Wave A received canonical live addresses only — e.g. `PZ-4.asset` = native USDC on Base, read from the official source and re-verified; `groupAgent` = a dedicated genesis EOA created and custodied **before** the ceremony, because an immutable's argument must exist before the contract that enshrines it.

### 2.4 Gates

Four gates precede any mainnet broadcast:

1. **Human review** of the deployer source — the vehicle is small enough to be read in full.
2. **Bytecode == artifact**: deployed code is compiled from a pinned commit whose test suite is re-executed and *read* at that commit, never recalled from memory.
3. **Payload freeze with rehearsal**: the exact scripted payload is executed on Sepolia, then frozen; mainnet may execute only the frozen bytes. The witness is the payload's keccak: the mainnet ceremony's payload hashed to the frozen gate-3 value `0xa9571570…`, so the executed payload is provably byte-identical to the rehearsed one; the gas figure (§3.2) is a corroborating, secondary witness.
4. **Human hands only on the trigger**: tooling prepares and reads back; the key-holder alone executes. Preparation and signature never share hands.

### 2.5 Read-back

Post-conditions are written **before** the ceremony. After it, each is read from chain **twice, by two independent paths**: once by the ceremony tooling, once by a from-scratch raw read (direct RPC, no shared code with the deployer). A deployment is *complete* when the read-back is green — not when the transaction confirms. Every figure that later enters a citable document is re-anchored at citation time; a claim is not something that *was* true, it is something whose proof *still answers today*.

## 3. Results — two ceremonies on Base mainnet

### 3.1 Ceremony G1 — the standard (Mur 1)

Four contracts born Safe-ALIA-native via the Mur1Deployer vehicle (`0xcbb260F26ed47a02BDd909BDa84e065e980DaFd2`, runtime 1,369 B on-chain): **ParameterRegistry, VerifyTransition, AIR, AgentThetaJournal**. Birth transaction `0x6ffff8030b0d18f381b16b118623ba1a08cb35cf14b71b017f045e73fdc9a639` (block 48,247,442, 2026-07-05 20:43 UTC, gas 7,150,443); seed transaction `0x6a5a643889e55a5d7fb4f39f19239dd3220a436b5f1871901fce3c8cca84c776` (block 48,269,274, 2026-07-06 08:51 UTC): six governed transition parameters + the category namespace as deployed (`0x1dc67168f639332f2d75dff21e943d12cfe6ade5d58ebaac37eaad8b0fc40159`, read back on-chain via `VerifyTransition.category()`) + the enclave-PCR slot, which must be set before any transition can verify.

#### 3.1.1 Post-mortem: EIP-170

The first-generation deployers embedded the four child initcodes in their own runtime, reaching 32,251 B (Mur 1) and 33,877 B (PZ) — both past the 24,576-byte runtime limit. The Foundry test bench does not enforce EIP-170, so the suites were green on a contract that could not be deployed; the limit surfaced as a `CreateContractSizeLimit` failure at the first real `forge create` on Sepolia — caught by the rehearsal, before mainnet. Lesson, gated permanently: **gate-2 (a bytecode hash) proves identity, not deployability**; a size-gate plus a successful real `forge create` are now mandatory before any ceremony. Resolution: the v2 idiom carries the four initcodes in calldata, leaving the vehicle only the wiring logic — the deployed Mur1Deployer is 1,369 B (margin 23,207 B under the limit; its PZ twin is 1,497 B, margin 23,079 B), both read on-chain.

### 3.2 Ceremony PZ Wave A — the operator layer

Four contracts born Safe-APIS-native via the PZDeployer vehicle (`0xFe143b77d4cFe7E41BC1f6e3a75db419604C6276`, runtime 1,497 B on-chain): **resolver (θ→tier), ALIAOracleAdapter** (ownerless immutable boundary), **PZ-2 CircuitBreaker, PZ-4 TradingSwarm**.

Transaction `0x5e79e5060b35ca0d6c58794dc2bc5a216ba540cb93f60d6ae8c3daa64c422a44` — status 1, block 48,286,238 (2026-07-06 18:17 UTC), gas used **7,679,482**. Safe-APIS nonce moved 0 → 1: the ceremony was that Safe's **first act on chain** — the operator domain has no history prior to its own genesis.

*(Determinism note: the executed payload is proven byte-identical to the rehearsed one by its gate-3 keccak — `0xa9571570…4cd25eef`, §2.4 — which is firsthand-verifiable. A cross-network gas comparison against the Sepolia rehearsal was dropped: the exact rehearsal figure is not firsthand-retrievable this cycle, and the keccak match is the stronger witness in any case.)*

**Seventeen post-conditions, green twice** (ceremony read-back via `ledger_execute_pz.py`, then independent raw re-read — session Fable, direct RPC). By class:

- *Ownership*: `owner`/`governor` == Safe-APIS on all three governed children; the adapter exposes no owner (the ALIAOracleAdapter ABI declares no `owner()`/`governor()`, and a raw `eth_call` to the `owner()` selector returns empty).
- *Wiring*: both PZ contracts read θ through the adapter (`oracle()` == adapter ×2); the adapter's journal is the ATJ (`journal()` == ATJ); `PZ-4.asset` == native USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`); `groupAgent` == the genesis EOA `0x01B0e09BCA2c801E20619741Fa36711D76D72335`.
- *Dormancy*: the B-COMPAT dormant slots read zero.
- *Separation*: `journal.owner()` == Safe-ALIA **and** Safe-APIS ≠ Safe-ALIA — the two-domain claim as two reads.
- *Integrity*: `extcodehash` of all four children == the pinned build artifacts.

Verbatim 17-item read-back log (reproduced from the ceremony record, unedited):

```
[OK] 1.  resolver.governor      == Safe-APIS
[OK] 2.  PZ-2.owner             == Safe-APIS
[OK] 3.  PZ-4.owner             == Safe-APIS
[OK] 4.  adapter.journal        == journal (ATJ)
[OK] 5.  adapter.tierResolver   == resolver
[OK] 6.  adapter.quarantine     == 0
[OK] 7.  PZ-2.oracle            == adapter
[OK] 8.  PZ-4.oracle            == adapter
[OK] 9.  resolver.journal       == journal
[OK] 10. PZ-4.asset             == USDC (native Base)
[OK] 11. PZ-4.groupAgent        == genesis EOA
[OK] 12. SAFE_APIS             != SAFE_ALIA
[OK] 13. journal.owner          == SAFE_ALIA  (two domains)
[OK] 14. extcodehash resolver   == artifact
[OK] 15. extcodehash adapter    == artifact
[OK] 16. extcodehash PZ-2       == artifact
[OK] 17. extcodehash PZ-4       == artifact
READ-BACK PZ GREEN — 17/17 (twice: ceremony tooling + independent raw re-read)
```

### 3.3 Source verification

**8/8 contracts source-verified** on Basescan (2026-07-07) — the four standard contracts and the four Wave-A contracts — after an explicit import-perimeter review distinguishing guard-rail mechanics (thresholds, bounds, fail-safes: publishable) from off-chain heuristics (out of scope by standing rule; the consumed sub-grade is *called* on-chain, never computed there). Process lesson, adopted for all future waves: **the verify perimeter is decided before the ceremony**, so that vendored imports are a choice, never a fait accompli.

### 3.4 Canonical addresses

*All rows re-read on-chain during the pre-publication pass (2026-07-07).*

| Role | Contract | Address |
|---|---|---|
| Governance (standard) | Safe-ALIA — 2-of-3 | `0x92050BF3eC9D0742569907AA43590E0254424c1c` |
| Governance (operator) | Safe-APIS — 2-of-3 | `0xB782Eb5E339AfEb136CA1f33B8ee0E733Cc46448` |
| Standard | ParameterRegistry | `0x1A2a3D106AFBBd59CF2e186257521Bdb34bf869c` |
| Standard | VerifyTransition | `0x3bF63Dd358359f3e2cD37a5212147ad6C8458C75` |
| Standard | AIR | `0x02448AfB76E6709127490b540263459e6D55A01e` |
| Standard | AgentThetaJournal (ATJ) | `0xC154cd4BEc95E1CCfA0e164770C6016A32d19398` |
| Operator | Resolver θ→tier | `0xF026B520c8BF06e7A93bD5DE8e53f81cF1496C41` |
| Boundary (ownerless) | ALIAOracleAdapter | `0xBfD516961C97BA014b9dC6aE04536626692cE2e5` |
| Operator | PZ-2 CircuitBreaker | `0xe419a2d09e5E6f0F0D9007F07c535ba63B9B7B4a` |
| Operator | PZ-4 TradingSwarm | `0xBa1149744305BAcEE6A7406beAcC280e105AA23b` |
| Vehicle (inert) | Mur1Deployer | `0xcbb260F26ed47a02BDd909BDa84e065e980DaFd2` |
| Vehicle (inert) | PZDeployer | `0xFe143b77d4cFe7E41BC1f6e3a75db419604C6276` |
| External | USDC (native, Base) | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |

*Owner EOAs are not listed. Reproducibility is method-and-expected only: `getOwners()` on Safe-ALIA and on Safe-APIS each return **identical sets of 3, threshold 2** — the same signers behind both domains at genesis (§2.2). Any reader enumerates them on-chain; no owner values are published here.*

## 4. Verifiable dormancy — publishing the OFF state

The usual failure mode of protocol communication is claiming activity that cannot be checked. We invert it: **we publish inactivity in a form anyone can check.**

As of block 48,318,211 (2026-07-07 12:01 UTC):

- `agilThreshold == 1`, with the operator set containing only the genesis operator — both **enumerable on-chain** by any reader. This is the weakest possible attestation configuration, and it is deliberately legible.
- The journal contains **zero sealed transitions since genesis**. Perimeter of this absence claim: full event scan from the birth block (48,247,442) to block 48,318,211 — 70,769 blocks — returned no journal events.
- By this corpus's standing publication rule, **every statement about attested transitions remains future-tense** until a quorum of ≥ 3 independent operators is live. The gate is not editorial discipline alone; it is checkable against the chain, because the threshold that would falsify a premature claim is itself public state.
- The fail-safe during the dormant window is **procedural and watched, not enforced**: the genesis key is cold and signs nothing; a guard process re-reads journal emptiness, the threshold, the operator set, and both Safe nonces on a fixed cadence, with out-of-band alerting and a heartbeat whose *absence* is itself a signal. Every check the guard performs is a pure RPC read — any reader can replay the guard's entire verdict independently.

A standard in this state makes exactly one promise: *nothing has happened yet, and you can verify that nothing has happened yet.* We submit that this is the only honest starting state for infrastructure that intends to be trusted later.

## 5. The unit of a multi-chain census

During the census re-cast supporting this note, one address (`0xe1D56f8DB28C4F257dF4A501e1D304073475ce14`), deployed on three chains, was found to carry **three distinct bytecodes** — Base 7,273 B, Gnosis 3,080 B, BNB 5,055 B, pairwise-distinct keccak — established by direct bytecode reads, not inferred from tooling. Consequence: **deduplicating a multi-chain census by address undercounts structurally.** The correct unit is *(bytecode × chain)*. The census cited in the companion annex (37 contracts code-present: Base 22, Gnosis 14, BNB 1, re-cast 2026-07-07) counts contracts under this unit, never addresses.

## 6. Non-claims and limitations

Stating what this note does **not** claim is part of its method.

- **No predictive-quality claim.** The θ engine is dormant; the journal is empty. Whether the standard's attested transitions will carry predictive value is a question that belongs to its own future prediction record, not to this note.
- **Governance separation is structural, not yet political.** Same three signers behind both Safes at genesis, stated as-is (§2.2). The on-chain fact is the *possibility* of divergence without touching a contract.
- **Gates are not an audit.** This note claims process integrity and verified post-state, not the absence of vulnerabilities. No security-audit claim is made or implied.
- **Scope of the ceremonies.** A pre-existing market line — the four registries owned by a single deployer EOA (FQRAnchor and the agent/asset/auditor identity registries, `owner()` == the deployer EOA, verified firsthand) — predates the two ceremonies and sits outside their scope; its migration under Safe-APIS is scheduled with its own read-back (status at publication: **scheduled** — transfer script prepared, not yet executed).
- **Absence verdicts are perimeter-bound.** Capability sweeps proving key inertness cover the declared Base live surface; multi-chain role enumeration on Gnosis/BNB is an open, dated debt in the working record, and no cross-chain inertness is claimed here.

## 7. Reproducibility appendix — the claims table

*Method column uses standard tooling (`cast call`, `cast tx`, `cast codehash`, event scan via RPC). Every row carries status **re-anchored 2026-07-07**; no row is blocked.*

| # | Claim | Where | Method | Expected |
|---|---|---|---|---|
| 1 | PZ Wave A ceremony executed, status 1 | tx `0x5e79e506…c422a44` | `cast tx` / receipt | status 1, block 48,286,238 |
| 2 | Payload byte-identity Sepolia→mainnet | payload + gate-3 | keccak(payload) == frozen | `0xa9571570…4cd25eef` (mainnet gas 7,679,482) |
| 3 | Ceremony was Safe-APIS's first act | Safe-APIS | nonce before/after | 0 → 1 |
| 4 | Governed children owned by Safe-APIS | resolver, PZ-2, PZ-4 | `governor()` / `owner()` | Safe-APIS ×3 |
| 5 | Adapter is ownerless | adapter | ABI has no `owner()`; raw `eth_call` owner() → empty | no owner exposed |
| 6 | Both PZ read θ via adapter | PZ-2, PZ-4 | `oracle()` | adapter address ×2 |
| 7 | Adapter reads the ATJ | adapter | `journal()` | ATJ address |
| 8 | PZ-4 asset is native USDC | PZ-4 | `asset()` | `0x8335…2913` |
| 9 | Two-domain separation | ATJ + both Safes | `owner()` + address compare | ALIA-owned ∧ APIS ≠ ALIA |
| 10 | Children match pinned artifacts | 4 Wave-A contracts | `extcodehash` vs build | equal ×4 |
| 11 | Standard born Safe-ALIA-native | 4 Mur-1 contracts | `owner()`/`governor()` @ birth tx | Safe-ALIA ×4 |
| 12 | Seed applied as specified | ParameterRegistry + VT | read 6 params + `category()` | 6 transition params (public_parameters.json, sha256 `80f310cb…`) `valueAt`==source; category `0x1dc67168…40159` |
| 13 | Dormancy: zero sealed transitions | ATJ | event scan 48,247,442 → 48,318,211 | 0 events (70,769 blocks) |
| 14 | Weakest-quorum state is public | VerifyTransition/AGIL | `agilThreshold()` + operator set | 1; genesis-only |
| 15 | Sources are readable | 8 contracts | Basescan verification status | Verified ×8 (2026-07-07) |
| 16 | Census unit holds | `0xe1D56f…ce14` ×3 chains | bytecode size + keccak per chain | 7,273 / 3,080 / 5,055 B, distinct |
| 17 | Suites green at pinned commits | build commits | re-run per repo | per-repo table, annex §1 (sum 1,045 · 0 fail) |

---

### Publication gates (to be checked, in order, before release)

1. No unfilled bracket slots remain — placeholder-glyph grep count == 0. **✅ 0 (checked 2026-07-07).**
2. Every figure — including those present since the draft — re-anchored firsthand this cycle; registry updated. **✅ done 2026-07-07 (canonical table by cast, network state at block 48,318,211, linchpin by 3-chain bytecode read, 17-item log verbatim, per-repo table @pinned commits).**
3. Textual read-back: every sentence true *as of the borne date*, tenses correct; re-grep of retired surclaims == 0. **✅ passed 2026-07-07.**
4. Registry: Œuvre A → **PUBLISHED @2026-07-07**; annex cross-references resolved. **✅**

*This note was prepared under the corpus's standing doctrine: figures are re-read, never recalled; the judge is never the producer; escalate rather than guess.*
