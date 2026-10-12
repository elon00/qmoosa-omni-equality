# Production security truth status

**Deployment decision: BLOCKED.** No chain transactions, paid executions or cycle expenditures are authorized by this branch.

## Confirmed changes
- Ledger registration now requires its immutable registrar and a registered identity in an explicitly configured deployed SovereignIdentity contract. Constructor ABI has changed; do not deploy without a compatibility review.
- Reality Gate refuses to certify the bespoke lattice signer as NIST FIPS 204 ML-DSA-65.
- Reality Gate refuses to certify Solidity by checking only filenames or method strings.
- CI executes pip-audit; unresolved advisories block that job.

## Remaining mandatory gates (none may be marked complete without evidence)
1. Replace bespoke lattice signatures with a validated, interoperable ML-DSA-65 implementation; positive, negative and cross-implementation test vectors, safe secret handling, API migration.
2. Prove unique-person enrollment using privacy-preserving trustworthy human verification; preventing duplicate hashes does **not** prove one human one vote. Threat-model registrar abuse, revocation and recovery.
3. Compile contracts reproducibly; run runtime tests for registration, unauthorized operations, demurrage rounding, supply conservation, overflow/underflow, gas bounds and malicious recipient behavior.
4. Resolve accounting-policy inconsistency between README (50/50) and Solidity (40/20/40) through a documented governance decision. **Do not silently change economic policy.**
5. Add authentication, request resource caps, rate limiting, secret management, telemetry, API integration tests and independent security assessment.
6. Lock and review dependency versions, reproducible builds, automated advisory monitoring, software bill of materials, protected branches.
7. Document testnet-only deployment plan and verifiable chain IDs/addresses after all security gates pass; separate additional mainnet authorization.

The Qiskit statevector solver runs on a simulator; describing it as execution on quantum hardware or as a 'zero simulation' environment would be inaccurate.
