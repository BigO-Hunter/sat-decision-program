# Decision-versus-counting certificate program

A compact research program on the 3-SAT decision-versus-counting gap: the certificate object is the count polynomial `H(T)`, with `H(0) = #F`, Hermite data and inclusion–exclusion.

## Verdicts

- **Candidate A — partial Hermite/sparse recovery: closed.** Exact small-case computation shows the deformation makes `H` almost fully dense, including near-threshold SAT instances. There is no usable sparse target.
- **Candidate B — mod-p/one-sided decision: closed by analysis.** It changes the arithmetic, not the combinatorial cost.
- **Candidate C — inclusion–exclusion-width pruning: closed by computation.** Every restricted sum contributes; there is no generic nonzero-branching saving.
- **Candidate D — proof-complexity minimality: open.** The remaining question is whether decision-only IPS/PC^oplus certificates can be shorter than the counting transcript.

See [CERTIFICATE.md](CERTIFICATE.md) for the derivation, citation ledger, exact negative results and caveats. These are generic-case obstructions, not a proof that no decision gap exists.

## Files

- `q1_degree_sparsity.py` — exact degree/sparsity measurements of `H`.
- `q2_zero_fraction.py` — exact restricted-sum zero-fraction measurements.
- `q3_ips_check.py` — IPS-object checks.
- `q4_gate_verification.py` — gate checks for the remaining proof-complexity question.
- `q5_hermite_pipeline.py` — the Hermite/count-polynomial pipeline.
- `q5_results.txt` — recorded output.
- `ALIGNMENT.md`, `BRIDGE.md`, `DERIVATION.md`, `IPS_OBJECT.md` — supporting derivations and source alignment.

AI-assisted by the darkhipo/MultiAgency swarm, with source attribution in the certificate.
