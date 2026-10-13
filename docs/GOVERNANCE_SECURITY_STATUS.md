# P0 Governance Security — Evidence Boundaries

The off-chain governance engine now requires:
- An externally provisioned snapshot of eligible citizen IDs mapped to ML-DSA-65 public keys.
- Signed proposals and ballots under the `OEQ-GOVERNANCE-V1` domain.
- Signed proposal content digest, voting deadline and proposal-specific ballot binding.
- At most one ballot per registered identity per proposal; altered/replayed ballots are rejected.
- At least 50% voter participation and >=60% affirmative votes among valid participating ballots, calculated by integer arithmetic.
- Voting closure before result execution.

**This does not establish one-human-one-vote.** An approved, privacy-preserving personhood issuer, key lifecycle/revocation, registry distribution, durable transaction storage, administrative control, concurrency and replay across process restarts, audit trails, independent crypto review, and on-chain governance integration remain unresolved.

**This is an off-chain prototype.** The mutable Python process is not a decentralized governance ledger. Signatures are not legal consent by themselves. A static in-memory registry is a controlled local input, not evidence of actual human enrollment. Time is caller-injectable for deterministic tests; production time sources must be trusted and authenticated. Do not authorize value-bearing decisions or mainnet deployment based on these tests.

**Zero spending**. No blockchain deployments or paid services. Gate status: LOCAL VERIFICATION PENDING CI; production readiness BLOCKED.
