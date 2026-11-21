# The bridge: decision-vs-counting = the IPS size question, decomposed

2026-10-31, session 3. Written while the HLT-2026 deep-read and the
transcript-as-IPS formalization run in parallel (their outputs land in
this directory).

## The chain

Let T_count(n) = 2^{O(n·(loglog n)²/√log n)} — the algorithm's runtime.

1. **(GP transfer, established)** Any algorithm deciding unsatisfiability
   of a polynomial system in time T(n) yields IPS certificates of size
   poly(T(n)) for the yes-instances-of-unsat (Grochow–Pitassi 2014/2018;
   the "algorithms ⟹ proofs" folklore; PIT↔IPS arXiv:2306.02184 for the
   simulation side).

2. **(Applied)** The counting algorithm, on an UNSAT instance (H(0) = 0),
   decides unsatisfiability in T_count. Hence every UNSAT bounded-occurrence
   instance (and, via the sparse-parity reduction, general k-SAT with
   overhead) admits an IPS certificate of size poly(T_count).

3. **(The two directions)**
   - IF random 3-CNF has an IPS lower bound size ≥ 2^{Ω(f(n))} in the
     certificate class that the transcript's circuit occupies (see
     IPS_OBJECT.md once it lands), THEN no algorithm — decision or counting —
     beats 2^{Ω(f(n))} on those instances. The gap closes from above.
   - IF a decision-only certificate of size o(T_count) exists (and is
     findable), the gap opens.

## The decomposition the transfer makes possible

The GP transfer is one-directional: algorithm ⟹ certificate. The reverse
fails — a small certificate may exist without any efficient algorithm
FINDING it. So the decision-vs-counting question decomposes:

    gap  =  (existence gap)  ×  (findability gap)

- **Existence**: do UNSAT random 3-CNF admit IPS certificates strictly
  smaller than the transcript bound T_count? This is a pure proof-complexity
  question — the HLT-2026 line's territory. A NO (lower bound at T_count's
  scale) closes the entire gap.
- **Findability**: even if certificates of size S exist, an algorithm needs
  to construct one. The counting algorithm FINDS its certificate by running
  itself. A decision algorithm could fail to exist even when small
  certificates exist — if finding them is hard (e.g., the findability
  problem is itself NP-hard-ish, or requires search the certificate's
  structure hides).

Our sessions 1-2 negatives now read precisely: they closed three
FINDABILITY relaxations (ways a decision algorithm might find/verify
cheaper data using the counting algorithm's own machinery). The
existence question was never touched by them — it lives entirely in
proof complexity.

## What would close each branch

- Existence-NO (gap closed): an IPS lower bound ≥ 2^{Ω(n(loglog)²/√log · (1-o(1)))}
  for random 3-CNF in the transcript's circuit class. Requires extending
  HLT-2026's technique to random formulas — the identified frontier.
- Existence-YES + findability-YES: an explicit sub-T_count certificate
  family — a new algebraic construction. The positive race.
- Existence-YES + findability-NO: the subtlest outcome — smaller
  certificates exist but no efficient search finds them. Would itself
  need a proof (e.g., findability hard under some assumption).

## Session 3's deliverables (in flight)

1. HLT-2026 deep-read: how far their technique is from random 3-CNF, and
   what circuit class their bounds cover (gates the transcript's class).
2. IPS_OBJECT.md: the transcript's explicit circuit, its size formula
   T_tr(n,m,Q,J,q,r,τ,D), its circuit class, the stated conjecture, and a
   mod-p sanity check at n=8.
3. This bridge: the decomposition and the closing conditions.

## Session 3 additions — HLT-2026 verdict (sub-agent deep-read)

**The technique and its reach**: rank-based monotone feasible interpolation
(Pudlak-Sgall style) + order-lifting, consuming a MONOTONE SPAN PROGRAM
lower bound for a structured generator function GEN_n. Bounds: roABP-IPS_LIN
width 2^{N^Omega(1)} for their lifted split CNFs, any field, any order.

**Distance from random 3-CNF: maximal.** The paper never touches random
formulas. The technique REQUIRES an unsatisfiable split formula whose
interpolant is a monotone function with a known span-program bound —
structure random CNFs lack entirely. The stated next milestones are
OTHER fragments (multilinear-formula IPS, low-individual-degree
constant-depth), not random formulas. And the stakes they name: a
constant-depth-IPS lower bound for a CNF would imply AC0[p]-Frege
lower bounds — a longstanding open problem.

**What this means for the fork (honest recalibration):**
- The EXISTENCE-NO branch (prove the transcript near-minimal for random
  3-CNF) is BEYOND the current frontier — not incrementally, but
  structurally: no existing technique addresses random 3-CNF at ANY
  superpolynomial IPS size, let alone the transcript's scale. This branch
  is a multi-year program if it is possible at all.
- The EXISTENCE-YES branch (smaller decision certificates than T_count)
  is the only tractable side — new-construction research, exactly the
  shape of the near-miss hunting the APSP lane does.
- CLASS ALIGNMENT (to verify when IPS_OBJECT.md lands): the transcript's
  circuit is Sigma-Pi shaped (sums over x of products over clauses);
  if it is an roABP of small width, then our upper bound and HLT's lower
  bounds live in the SAME class (roABP-IPS) on DIFFERENT families —
  meaning the random-3-CNF roABP-IPS question is well-posed and open,
  bounded above by T_count and below by nothing.

**PC^opl: untouched by HLT** — our system remains open in both directions.

Revised program standing: the fork's productive branch is certificate
construction (upper); the lower branch is frontier-beyond-frontier.
The next bounded session should chase the class alignment and then,
if aligned, state the random-3-CNF roABP-IPS question as the program's
central open problem — bounded above by our transcript, below by nothing.
