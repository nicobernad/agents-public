#!/usr/bin/env python3
"""
verify.py — vérifie la conformité d'un ancrage ALIA par RECALCUL, sans confiance dans l'émetteur.
Bibliothèque standard uniquement. Grammaire : voir anchoring_format.md.

  entry_root(entry)                                  -> racine sha256 canonique
  conform(entry, claimed_entry_hash, expected_prev)  -> (bool, raison)

Usage : python3 verify.py conformity_vectors.json    # rejoue les vecteurs (REPLAY_OK / REPLAY_FAIL)
"""
import hashlib
import json
import sys


def entry_root(entry):
    """Racine canonique d'une entrée (champ entry_hash exclu) : sha256(json trié, compact, UTF-8)."""
    e = {k: v for k, v in entry.items() if k != "entry_hash"}
    return hashlib.sha256(json.dumps(e, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def conform(entry, claimed_entry_hash, expected_prev_hash=None):
    """Conformité d'un ancrage : racine correcte ET (si fournie) continuité de chaîne."""
    if entry_root(entry) != claimed_entry_hash:
        return False, "racine != sha256(json_canonical(entree))"
    if expected_prev_hash is not None and entry.get("prev_hash") != expected_prev_hash:
        return False, "chaine rompue : prev_hash != entry_hash precedent"
    return True, "conforme"


def _replay(path):
    v = json.load(open(path))
    ok = True
    for x in v.get("valid", []):
        c, why = conform(x["entry"], x["claimed_entry_hash"], x.get("expected_prev_hash"))
        ok = ok and c
        print(f"[valide   attendu] conforme={c} ({why}) — {x['description']}")
    for x in v.get("invalid", []):
        c, why = conform(x["entry"], x["claimed_entry_hash"], x.get("expected_prev_hash"))
        ok = ok and (not c)
        print(f"[invalide attendu] conforme={c} ({why}) — {x['description']}")
    print("REPLAY_OK" if ok else "REPLAY_FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(_replay(sys.argv[1] if len(sys.argv) > 1 else "conformity_vectors.json"))
