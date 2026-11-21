# Class alignment: C_tr embeds in roABP-IPS_LIN — session 4
# [CONDITIONAL — session-6 amendment below]

## SESSION-6 AMENDMENT (2026-10-31, DERIVATION.md + R2125607561): the exact-identity embedding is REFUTED

The Q_i-to-Z-sums identification fails for EXACT identities: the paper's
X-formalism multilinearizes every X-carried functional (tex 879-881), but
valid Boolean-ideal divisions require non-multilinear Q_i (counterexample:
(x1 or x2)(x1 or ~x2)(~x1 or x2)(~x1 or ~x2) forces x1^4-monomials in every
valid division). X-carried C_tr circuits compute only Q_i mod <b> — the
exact identity C(x,f(x)) = 1 fails for them OFF THE CUBE. CONSEQUENCE: the
embedding below holds for MOD-<b> certificates (a weaker IPS variant), or
requires C_tr extended with a power-structure port. The literal
evaluation-reduction exists (construction R+ in DERIVATION.md) but is
vacuous. OPEN RESIDUE: general polynomial-weight post-maps — the span
question across instances — is the correctly-scoped gate test (replaces
session-5's vacuous basis design). Until it resolves, everything below is
CONDITIONAL on the mod-<b> reading.


2026-10-31. The refinement that connects our transcript to HLT-2026's bounds.

## The embedding theorem (informal but checkable)

**Claim.** Every C_tr certificate (IPS_OBJECT.md) is an roABP-IPS_LIN
certificate: y-linear (already: C(x,y) = sum y_ax A_a(x), y-degree 1 =
IPS_LIN by definition), with the x-part computable by a read-once ABP of
width W <= 2^{2n/r} · poly(n,m) = 2^{O(E(n))}.

**The two-step width argument.**

(1) *Each cube-slice summand is width O(m).* Fix a Z-core:
sum_{x~: x~_E=1} prod_e Phi_e(a_e(x~) + z b_e) — with x~ summed OUT, this is
a constant times prod_e Phi_e(<c_e1,x> + d1, <c_e2,x> + d2, <c_e3,x> + d3)
— a product over clauses of degree-3 polynomials in THREE LINEAR FORMS of
all n variables. In any read-once variable order, the partial state of one
clause factor is exactly the 3 running dot-product partials (linear forms
have scalar partial state — the whole point). The product over clauses
carries the tuple of open factors' partial triples: state dimension
3·(#open) <= 3m. Transitions: reading x_j updates the running sums (linear,
order-respecting) and completes factors whose last variable was read
(multiplying the running scalar). This is an roABP layer-by-layer.
=> width O(m) per slice. Same for the P_{e-1} prefix products (arity-3
clause polys: partial state = the factor's value on read vars — carried as
one scalar per open factor since classical clause factors are evaluated
incrementally... for the PREFIX layer the factors are degree-3 in SINGLE
variables (standard arithmetization, no linear forms) — width <= #open+1
<= m+1 directly).

(2) *The cube-slice union.* The transcript's group cost 2^{2n/r} is a SUM
of that many slice circuits (coset aggregation). A sum of K roABPs of
width w is one roABP of width K·w (standard: run them in parallel tracks).
=> total width <= 2^{2n/r} · O(m) · (IE/Hermite layers are FIXED LINEAR
maps — absorbed into the layer matrices, width-free).

**Caveat inherited from IPS_OBJECT.md**: the identification of Q_i's
coefficient functionals c_{i,beta} with the Z-machinery is structural,
not gate-by-gate proven. The embedding is exactly as strong as that step.

## What the alignment buys

1. **HLT's bounds now SIT in our certificate class**: their theorem is
   roABP-IPS_LIN width lower bounds 2^{N^{Omega(1)}} for lifted GEN CNFs.
   Our transcript certificate lives in the SAME class (width 2^{O(E(n))}).
   Their lifted formulas are HARD for the very class that certifies our
   random formulas. No contradiction (different formula families), full
   compatibility — the class is the right arena.

2. **The central problem sharpens to width**: random 3-CNF at threshold
   density — roABP-IPS_LIN refutations of width between... upper:
   2^{O(E(n))} (the transcript, poly(n) variables); lower: NOTHING (HLT's
   interpolation needs split structure random formulas lack). The gap
   question is now literally a WIDTH question in a single well-studied
   class — the standard currency of roABP lower bounds (Nisan's
   communication-complexity method for ORDER-RESTRICTED; HLT's lifting
   kills order-dependence).

3. **The conjecture restated in the standard currency** (replaces
   IPS_OBJECT.md's C_tr version): whp over random 3-CNF F at 4.26n, every
   roABP-IPS_LIN refutation of F has width 2^{Omega(E(n))}. This is now a
   question existing roABP-tool users could recognize — order-lifting
   (HLT's contribution) removes the usual order-quantifier objection.

## What would attack it

- Lower side: Nisan-style rank/communication arguments need structured
  hard polynomials; random CNFs resist (no structure to hang rank on).
  The HLT-style route: find a MONOTONE span-program-hard function whose
  SPLIT-CNF interpolant relates to random formulas — none known.
- Upper side: compress the transcript — the width is dominated by the
  2^{2n/r} coset aggregation; a width-reduced aggregation (better design
  or a decision-only certificate) would be the constructive gap.

Both sides are now stated in one class, one currency (width), one arena.
