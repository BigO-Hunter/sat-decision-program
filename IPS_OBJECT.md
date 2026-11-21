# IPS_OBJECT — explicit IPS certificate (s3, 2026-10-31)

**Axioms** (standard CNF arithmetization): clause polys f_e=∏_{(i,s)∈e}(1−ℓ_{i,s}), Boolean b_i=x_i²−x_i. UNSAT ⟺ g:=∏_e(1−f_e)≡0 on {0,1}^n ⟺ g∈⟨b_i⟩.

**1. Circuit.** C(x,y)=Σ_e y^cl_e·P_{e−1}(x)+Σ_i y^b_i·Q_i(x); P_{e−1}=Π_{e'<e}(1−f_{e'}).
- Prefix layer, O(m) gates (P_e=P_{e−1}(1−f_e)): Σ_e f_eP_{e−1}=1−g, exact telescoping.
- Division layer: g=Σ_i b_iQ_i (exact; g vanishes on cube). Q_i=Σ_β c_{i,β}(x_{−i})·(x_i^{β−2}+⋯+1); the c_{i,β} are count-functionals — cube-sums of clause products = the restricted sums Z_{t,E,U} (IE tex~900; Z, :22-24), computed from Hermite data (subsec:preview-interpolation, tex~813-945; deg_X[z^j]G≤j :20-21) by the fixed linear solve (H(0) linear functional, :18).
- C(x,0)=0 (y-homogeneous); C(x,f(x))=(1−g)+g=1, exact identity.

**Size.** T_tr=(m+n)·J·(Σ_{j≤q}2^jC(n,j))·(2D+1)^{2τn}·2^{2n/r}+O(m²), J=q+1 [three-costs eq, tex~975, :28]; log₂T_tr=O(n(loglogn)²/√logn)=:E(n) (:33) = transcript runtime.

**2. Class C_tr:** y-degree 1. x-part: ΣΠΣ cores (Z-sums = Σ over cube-slices of Π of deg-3 clause arithmetizations of linear forms) ∘ linear IE ∘ fixed linear solve — depth ≤5; truncated X-degree ≤3q (mod z^J); prefix layer ΣΠ, deg ≤m. ⊕ appears only as parity-indexed coset aggregation in the 2^{2n/r} group cost — the PC^⊕ content (:57-59).

**3. Conjecture.** For F~random 3-CNF at threshold density (4.26n clauses): ∀c>0, P_F[∃C∈C_tr refuting F, size(C)≤2^{c·E(n)}]→0. No 2^{o(E(n))} certificate in C_tr: transcript near-minimal in its class. (Sparse-PC degree-Ω(n) bounds: monomial-sparse only; C_tr is a circuit class — open.)

**4. Sanity check** (n=8, mod p=2^61−1; q3_ips_check.py): one random ρ=5.4 instance, m=43, #F=0 (brute 2^8). C(x,f(x))=1 at all 256 cube pts + 5/5 random F_p⁸ pts; reduced g=0; C(x,0)=0; count-functional Σ_{x'}Σ_ef_eP_{e−1}=256=2^8 — the Z/IE/Hermite layer's targets. PASS.

## Session 5 addendum: gate-verification status (2026-10-31)

The Q_i-to-Z-sums identification was tested computationally
(q4_gate_verification.py) and the run was VOID — no verdict: (a) numpy
silently coerced object arrays to int64, corrupting the mod-p arithmetic
(overflow warnings at the elimination core); (b) the span basis design was
vacuous (C(35,6) ~ 2M columns against 24 test points — at rank 24 anything
is in span, so the test could only "fail" through corruption, which it did).
The FAIL verdict printed by that run is DISCARDED as an artifact.

The honest verification requires implementing the Z/Hermite route to
produce Q_i values directly (the full transcript pipeline at small n) and
comparing with division-chain ground truth — a session-sized task, scoped
as session 6. THE CAVEAT REMAINS OPEN: the identification is structural,
not verified. Alignment.md's embedding inherits exactly this openness.

## SESSION-6 AMENDMENT: the identification is REFUTED for exact identities

See DERIVATION.md and R2125607561: the paper's X-formalism multilinearizes
(tex 879-881), valid divisions force non-multilinear Q_i (hand-checked
counterexample), so X-carried functionals compute only Q_i mod <b> and the
exact C(x,f(x)) = 1 identity fails off the cube. The certificate above is
sound AS AN IPS CERTIFICATE (verified on the cube + generic points in
q3_ips_check.py — the sequential-division route carries the powers); the
claimed ROUTE (computing the Q_i via the Z/Hermite machinery) covers only
the mod-<b> quotient. ALIGNMENT.md's embedding is conditional on this.
The open gate: the polynomial-weight span test across instances.
