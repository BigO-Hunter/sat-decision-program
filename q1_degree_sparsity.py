"""Session 2, Q1: degree/sparsity distributions of the count polynomial H(T).

Model (faithful to the paper's interpolation layer, R=1 deformations):
- H(T) = sum_{x in {0,1}^n} prod_e Phi_e((<(1-T)e_v + T L_{e,v}, x>))
  with random small-integer linear forms L_{e,v}; Phi_e multilinear in its
  three literals, so deg H <= #occurrences = 3m (actual degree measured).
- All arithmetic mod a large prime p (2^61-1): nonzero-detection is sound
  whp; the count #F is cross-checked by exact brute force.

Measurements per instance:
  #F (exact), SAT?, deg(H) actual, #nonzero coefficients of H,
  worst-case degree 3m, sparsity ratio.

If SAT instances (especially near-threshold) have systematically lower
effective degree or sparser H, decision-from-partial-Hermite-data has a
real target; if not, that relaxation dies honestly.
"""
import itertools
import random
import sys

import numpy as np

P = (1 << 61) - 1
NEG = P - 1  # -1 mod p


def clause_poly(coefs_x):
    """Phi_e for one clause, given the three literals' linear-in-T forms.
    Each literal: value at x = a + b*T with a = <e_v, x> (0/1), b = <L - e_v, x>.
    Phi = 1 - prod(1 - lit_i). Returns coefficient array (deg <= 3) mod p."""
    one = np.array([1, 0], dtype=object)
    prod = np.array([1, 0], dtype=object)
    for (a, b) in coefs_x:
        lit = np.array([a % P, b % P], dtype=object)
        one_minus = (np.array([1, 0], dtype=object) - lit) % P
        # polynomial multiply (deg <= 2 after two, 3 after three)
        prod = np.convolve(prod, one_minus) % P
    phi = np.zeros(len(prod) + 0, dtype=object)
    phi[0] = 1
    if len(phi) < len(prod):
        phi = np.concatenate([phi, np.zeros(len(prod) - len(phi), dtype=object)])
    return (phi[: len(prod)] - prod) % P


def count_poly(F, n, L, xs_batch):
    """H mod p as coefficient array; F = list of clauses (tuples of (var, sign)),
    L[e][j] = integer coefficient vector for occurrence j of clause e."""
    H = None
    m = len(F)
    dmax = 3 * m + 1
    for x in xs_batch:
        acc = np.array([1], dtype=object)
        for e, clause in enumerate(F):
            coefs = []
            for j, (v, s) in enumerate(clause):
                # the replacement r(T) = a + (b-a)T interpolates the VARIABLE X_v:
                # a = x[v] always; the literal applies s-mapping to the replaced value
                a = x[v]
                b = int(np.dot(L[e][j], x))
                if s == 1:
                    coefs.append((a, b - a))          # literal = r(T)
                else:
                    coefs.append((1 - a, NEG * (b - a) % P))  # literal = 1 - r(T)
            phi = clause_poly(coefs)
            acc = np.convolve(acc, phi) % P
            if len(acc) > dmax:
                acc = acc[:dmax]
        if H is None:
            H = np.zeros(dmax, dtype=object)
        H[: len(acc)] = (H[: len(acc)] + acc) % P
    return H


def brute_count(F, n):
    cnt = 0
    for bits in itertools.product([0, 1], repeat=n):
        ok = all(any(bits[v] == s for (v, s) in clause) for clause in F)
        cnt += ok
    return cnt


def random_3cnf(n, rho, rng):
    m = int(round(rho * n))
    clauses = []
    for _ in range(m):
        vs = rng.sample(range(n), 3)
        clauses.append(tuple((v, rng.randint(0, 1)) for v in vs))
    return clauses


def instance_stats(n, rho, rng, nrng, coef_range=3):
    F = random_3cnf(n, rho, rng)
    L = [[nrng.integers(-coef_range, coef_range + 1, n).tolist() for _ in range(3)] for _ in F]
    nF = brute_count(F, n)
    xs = list(itertools.product([0, 1], repeat=n))
    H = count_poly(F, n, L, xs)
    nz = int(np.count_nonzero(H))
    deg = int(len(H) - 1 - np.argmax(H[::-1] != 0)) if nz else 0
    # sanity: H[0] mod p should equal nF mod p
    ok = (int(H[0]) == nF % P)
    return dict(nF=nF, sat=nF > 0, deg=deg, nz=nz, worst=3 * len(F), sanity=ok)


if __name__ == "__main__":
    rng = random.Random(20261031)
    nrng = np.random.default_rng(20261031)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    per = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    print(f"n={n}, instances per density: {per}")
    for rho in (3.5, 4.26, 5.0, 6.0):
        stats = [instance_stats(n, rho, rng, nrng) for _ in range(per)]
        sat = [s for s in stats if s["sat"]]
        uns = [s for s in stats if not s["sat"]]
        def agg(ss, key):
            return (np.mean([s[key] for s in ss]) if ss else float("nan"), max((s[key] for s in ss), default=0))
        print(f"rho={rho}: SAT={len(sat)} UNSAT={len(uns)} sanity={sum(s['sanity'] for s in stats)}/{per}")
        for key in ("deg", "nz"):
            ms, Ms = agg(sat, key)
            mu, Mu = agg(uns, key)
            print(f"  {key}: SAT mean/max {ms:.1f}/{Ms}  UNSAT mean/max {mu:.1f}/{Mu}  worst={stats[0]['worst']}")
