# DERIVATION — evaluation-reduction for Q_i (session 6, 2026-10-31)

Question: does "evaluate Q_i at x*" reduce to a Z-sum/Hermite run on a derived
instance, poly(m,n) per point?

## 1. The literal reduction EXISTS — but is vacuous (conf: high)

Derived instance F'_{i,x*}: pin x_{-i}:=x*_{-i} inside the literal forms; each
clause arg becomes a_{e,v}·y + b_{e,v}, y:=x_i (a∈{0,±1}). Choose replacement
forms <P'_{e,v}(T),X> := a_{e,v}(X_i+T)+b_{e,v}: degree 1≤R, restores originals
at T=0, design trivial (1 variable). Then the derived count-polynomial is
H'(T) = q(T)+q(T+1), q(Y):=g(Y,x*_{-i}) — exactly the paper's shift machinery
(tex 846–857) with X_i-port = +T. Taylor recovery at t=1, J'=d_i+1 determines
H' (uniqueness argument verbatim, tex 822–830); data = Z'-sums with E,U⊆{i}
(tex 906–920), each a ≤2-point sum, poly(m) cost. Then q=(I+S)^{-1}H' (S the
unit shift on coefficients; det=2^{d_i+1}≠0 over Q), and
c_{i,β}(x*_{-i})=[Y^β]q, Q_i(x*)=Σ_{β≥2}[Y^β]q·(x*^{β-2}_i+…+1).
**But vacuous:** q's coefficients are directly the product of m univariates,
poly(m·d_i) with no machinery; and x* enters as instance constants, not as
input wires of a fixed circuit — this witnesses nothing about c_{i,β}∈C_tr.

## 2. The intended identification (original transcript, X-carried) is REFUTED
for exact identities (conf: high)

Type fact: Z_{t,E,U}∈Q[z]/z^J has no free x-slot; x can only enter as post-map
weights. The X-formalism (tex 839–895) multilinearizes — "replace every
positive power of X_i by X_i" (tex 879–881), IE inverts only Boolean
evaluation (tex 888–895) — so every X-carried functional is MULTILINEAR in x.
But valid divisions are forced non-multilinear: counterexample (UNSAT, n=2)
F=(x1∨x2)(x1∨¬x2)(¬x1∨x2)(¬x1∨¬x2): [x1⁴]g=−x2³ and the x1⁴x2³-monomial of
g=Σb_iQ_i forces some Q_i to contain x-degree ≥2. Multilinear functionals
cannot. Also q-truncation (|E|≤q< n−1) blocks point-isolation on the original
instance regardless. So X-carried C_tr circuits compute only Q_i mod ⟨b⟩ —
the exact IPS identity (IPS_OBJECT line 8) fails for them off the cube.
Identification survives ONLY mod-Boolean-ideal.

## 3. Open residue (conf: medium)

General polynomial weights w(x)·Z-linear post-maps: a finite-dim span question
across instances — the correct session-6 gate test (span across instances, not
session-5's vacuous across-points basis). Any dense post-map costs 2^{Θ(E(n))}
per evaluation, so poly-cost forces sparsity — evidence against.

**Verdict:** reduction exists (vacuous); identification FALSE in the exact
reading, TRUE only mod ⟨b⟩; ALIGNMENT.md inherits conditionality — embed
mod-⟨b⟩ certificates or extend C_tr with a power-structure port.
