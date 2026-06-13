# agents-public

Spécifications publiques de la couche d'instrumentation ALIA — **recalculables**, **conditions
identiques pour tout implémenteur** (aucune implémentation n'a de statut privilégié).

Voir [`spec/`](spec/) : schéma de journal, régimes de preuve, format d'ancrage, vecteurs de
conformité, et le vérifieur autonome [`spec/verify.py`](spec/verify.py).

Vérifier soi-même (sans confiance dans l'émetteur) :

    python3 spec/verify.py spec/conformity_vectors.json    # -> REPLAY_OK
