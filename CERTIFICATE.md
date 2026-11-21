# The decision-vs-counting certificate program — session 1: the certificate object

2026-10-31. Sources: openai/math @ 7ef5c0cc, preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex (fetched to /private/tmp/eth-paper/). All equations below are verbatim extractions with line anchors.

## 1. The certificate object (what the algorithm implicitly constructs)

**The count polynomial** (eq:overview-direct-count → eq:simple-counting-polynomial, tex ~575-633):

    H(T) = Σ_{x∈{0,1}^n} Π_{e∈F} Φ_e((⟨P_{e,v}(T), x⟩)_{v∈I_e})  ∈ Q[T]

- Φ_e = clause satisfaction polynomial; P_{e,v}(T) = replacement linear-form
  coefficients, degree ≤ R, with ⟨P_{e,v}(0),X⟩ = X_v (restores the original).
- H(0) = #F exactly; deg H ≤ MR ≤ 3nR (M ≤ 3n by bounded occurrence).

**The Hermite data layer** (subsec:preview-interpolation, tex ~813-945):

- q = ⌊3nR/Q⌋, J = q+1; Taylor coefficients of H at t = 1..Q through degree q.
- Uniqueness: Q·J > 3nR ⟹ the data pins H; H(0) is a linear functional of it.
- The z-shift: G_x(X,z) = Π_e Φ_e(⟨P_{e,v}(t),x⟩ + ⟨ΔP_{e,v}(z),X⟩);
  **the load-bearing degree bound: deg_X([z^j]G_x) ≤ j** (every X carries a z),
  so mod z^J all monomials have ≤ q X-variables.
- Inclusion-exclusion (tex ~900): a_E(x,z) = Σ_{U⊆E}(-1)^{|E|-|U|}G_x(1_U,z),
  and H(t+z) ≡ Σ_{|E|≤q} Σ_{U⊆E}(-1)^{|E|-|U|}Z_{t,E,U}(z) (mod z^J), where
  Z_{t,E,U}(z) = Σ_{x: x_i=1 ∀i∈E} G_x(1_U,z) — the design-separable restricted sums.

**The three costs** (eq:overview-three-costs, tex ~975):

    [Σ_{j≤q} 2^j·C(n,j)] · [(2D+1)^{2τn}] · [2^{2n/r}]
    ~ (q+1)(2en/q)^q · (2D+1)^{2τn} · 2^{2n/r}

with r = Θ(√log n/(loglog n)²), Q = Θ(log n/loglog n), R = Θ(√log n),
τ = Θ(1/(r·log n)), D = r^{2Q} ≤ (2n)^{1/128}. Log-exponent = O(n(loglog n)²/√log n),
dominated by the group cost 1/r and the IE cost (R/Q)log(2Q/R).

## 2. The decision question, now precise

Decision needs only the predicate H(0) ≠ 0. The algorithm pays for EXACT
reconstruction of ALL of H. Candidate relaxations:

**(B) Mod-p / one-sided — CLOSED as a non-lever.** Running the identical
machinery over F_p decides "#F ≢ 0 mod p" with the same three combinatorial
costs (the exponent lives in q, r, τ — not the arithmetic). A one-sided-error
SAT detector with no exponent gain. Not a decision gap.

**(A) Partial-data sign determination — OPEN, testable.** With fewer Taylor
coefficients (J' < J), the Hermite system is underdetermined: an affine space
of consistent H's. The H(0)-sign is DECIDED by partial data iff it is constant
over that space. If near-threshold SAT instances (sparse #F) are pinned by
little data while the algorithm pays for full reconstruction, the gap exists.

**(C) IE-width pruning — OPEN, testable.** The first cost enumerates all
(E,U), |E| ≤ q. If many restricted sums Z_{t,E,U} ≡ 0 on SAT instances,
decision-only pruning (branch on nonzero sums only) beats the full IE.
Related: the whole algorithm never constructs the a_E — it exists for the
proof. A decision certificate could be a SPARSE sub-transcript.

**(D) Proof-complexity framing.** The transcript (Hermite data + linear
solve + design evaluations) is an IPS-family certificate of the arithmetized
identity H(0) = #F. For UNSAT: a PC^⊕-certificate that the count is zero.
Question: is it near-minimal, or do decision-only PC^⊕ refutations exist at
2^{o(n(loglog)²/√log n)}? Our CP closure (posted) says geometric systems
cannot do better; this asks it of the algebraic one that can.

## 3. The two testable small-case questions (session 2 target)

**Q1 (partial-data pin rate).** For n ≤ 20, random 3-CNF at densities
ρ ∈ {3.5, 4.26 (threshold), 5, 6}: compute H(T) exactly by brute force;
simulate partial Hermite data (J' ∈ {1..J} coefficients, Q' points);
measure the fraction of instances whose H(0)-sign is constant over the
consistent affine space. Prediction if the gap is real: near-threshold SAT
instances pin early (sparse H), dense-count instances need full J.

**Q2 (zero-sum fraction).** Same instances: compute the restricted sums
Z_{t,E,U} exactly for all |E| ≤ q (small q at small n); measure the fraction
identically zero mod z^J. High zero-fraction on SAT instances ⟹ a
nonzero-branching decision scheme pays strictly less than the full IE.

Both are exact-rational computations at brute-force scale — the same
instrument as the APSP covering arc. Verdict or bust.

## 5. Session 2 results (2026-10-31) — BOTH relaxations dead, honestly

**Q1 (degree/sparsity of H): DEAD.** n=10, 10 instances/density, random R=1
deformations, sanity 10/10 (H[0] = #F mod p verified; one real bug found and
fixed en route — a double-negation in the negative-literal encoding that the
single-clause test masked by coincidence: any one-negation clause has the
same 7/8 count). Results: deg(H) = 96-97% of worst-case at every density;
nonzero coefficients = degree+1 (H is FULLY dense); NO SAT/UNSAT separation
(threshold-density SAT mean deg 126.6 vs UNSAT 125.0). Near-threshold SAT
instances — the sparsest #F — have exactly as dense H as everything else.
The deformation smears the count across all degrees; #F's sparsity leaves
no trace in H(T). Partial-Hermite/sparse-recovery (candidate A) has no target.

**Q2 (zero-fraction of restricted sums): DEAD.** n=10, 8 instances/density,
q=2 (J=3), t=1: **0 of 4824 total (E,U) pairs have Z identically zero mod
z^J** — every restricted sum contributes, SAT and UNSAT alike. The
nonzero-branching scheme (candidate C) has nothing to branch on. Predicted
by Q1's density (dense H ⟹ no generic cancellations) and confirmed.

Caveat stated honestly: both tests use random R=1 deformations. The paper's
SPECIFIC P-construction (the spectral machinery, tex 2073+) is designed for
separability, not sparsity; nothing in it suggests forced cancellations, and
random deformations make cancellation measure-zero unless structurally
forced. The negatives hold for the generic case the relaxations targeted.

**Program state after session 2:** candidates A, B, C all closed (B by
reasoning, A and C by computation). The decision-vs-counting gap, if real,
lives only in (D): the PC^opl/IPS MINIMALITY question — are the counting
transcripts near-minimal certificates, or does a decision-only certificate
exist that no relaxation of the counting algorithm's own structure can
reach? That is a lower-bound question (prove minimality) or a genuinely
new-construction question (find the certificate) — the same fork the
APSP lane reached. Both verdicts posted to the 3sat board (pending).

