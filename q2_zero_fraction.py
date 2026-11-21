"""Session 2, Q2: the zero-fraction of restricted sums Z_{t,E,U}.

Model (R=1 deformation, faithful to the paper's IE layer):
  G_x(X,z) = prod_e Phi_e((a_e(x) + z*b_e(U))_{lit}) at X = 1_U, with
  a_e(x) = (1-t)x_v + t<L_e_v, x>   (replacement value at point t)
  b_e(U)  = <L_e_v - e_v, 1_U>      (the z-shift direction, U's indicator)
  Z_{t,E,U}(z) = sum_{x: x_i=1 (i in E)} G_x(1_U, z)  mod z^J

Question: what fraction of pairs (E,U), U subseteq E, |E| <= q, have
Z identically zero mod z^J?  If SAT instances have a high zero-fraction,
a nonzero-branching decision scheme beats the full inclusion-exclusion.

All arithmetic mod p (2^61-1) in numpy int64; zero-detection sound whp.
"""
import itertools
import random
import sys

import numpy as np

P = (1 << 61) - 1


def phi_z(a, b, s, J):
    """Phi_e for one clause given per-literal (constant a, z-coef b) arrays
    over x (vectorized), mod z^J. Literal value: s=1 -> a + b z; s=0 -> 1-a-b z.
    Phi = 1 - prod(1 - lit). Returns (J, nx) int64 array."""
    nx = a.shape[0]
    if s == 1:
        one_m = np.stack([(-a + 1) % P, (-b) % P] + [np.zeros(nx, dtype=np.int64)] * (J - 2))
    else:
        # 1 - (1 - a - b z) = a + b z
        one_m = np.stack([a % P, b % P] + [np.zeros(nx, dtype=np.int64)] * (J - 2))
    return one_m


def clause_phi_z(F, L, t, Uind, xs, J):
    """G_x(1_U, z) mod z^J for all x (rows of xs). Returns (J, nx)."""
    nx = xs.shape[0]
    acc = np.zeros((J, nx), dtype=np.int64)
    acc[0] = 1
    for e, clause in enumerate(F):
        prod = np.zeros((J, nx), dtype=np.int64)
        prod[0] = 1
        for j, (v, s) in enumerate(clause):
            Lv = np.array(L[e][j], dtype=np.int64)
            a = ((1 - t) * xs[:, v] + t * (xs @ Lv % P)) % P
            d = (Lv.copy() - 0) % P
            d[v] = (d[v] - 1) % P
            b = int(Uind @ d % P)
            om = phi_z(a, np.full(nx, b, dtype=np.int64), s, J)
            # polynomial multiply in z, truncate to J
            new = np.zeros((J, nx), dtype=np.int64)
            for kz in range(J):
                if not prod[kz].any():
                    continue
                for k2 in range(J - kz):
                    new[kz + k2] = (new[kz + k2] + prod[kz] * om[k2]) % P
            prod = new
        acc = acc + ((0 - prod) % P)
        acc[0] = (acc[0] + 1) % P  # 1 - prod accumulated as acc += (1 - prod)
    return acc % P


def zfractions(n, rho, rng, nrng, q=2, t=1, coef_range=3):
    F = []
    m = int(round(rho * n))
    for _ in range(m):
        vs = rng.sample(range(n), 3)
        F.append(tuple((v, rng.randint(0, 1)) for v in vs))
    L = [[nrng.integers(-coef_range, coef_range + 1, n).tolist() for _ in range(3)] for _ in F]
    xs = np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int64)
    nF = sum(1 for x in xs if all(any(x[v] == s for (v, s) in c) for c in F))

    pairs_total = pairs_zero = 0
    for E in itertools.chain.from_iterable(
        itertools.combinations(range(n), j) for j in range(q + 1)
    ):
        for Ubits in itertools.product([0, 1], repeat=len(E)):
            Uind = np.zeros(n, dtype=np.int64)
            for i, on in zip(E, Ubits):
                Uind[i] = on
            G = clause_phi_z(F, L, t, Uind, xs, q + 1)
            mask = np.all(xs[:, list(E)] == 1, axis=1) if E else np.ones(len(xs), dtype=bool)
            Z = G[:, mask].sum(axis=1) % P
            pairs_total += 1
            if not Z.any():
                pairs_zero += 1
    return nF, pairs_zero, pairs_total


if __name__ == "__main__":
    rng = random.Random(20261031)
    nrng = np.random.default_rng(20261031)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    per = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    q = 2
    print(f"n={n} per={per} q={q} (J={q+1}), t=1")
    for rho in (3.5, 4.26, 5.0, 6.0):
        sat_z = uns_z = sat_n = uns_n = 0
        for _ in range(per):
            nF, pz, pt = zfractions(n, rho, rng, nrng, q=q)
            if nF > 0:
                sat_z += pz; sat_n += pt
            else:
                uns_z += pz; uns_n += pt
        print(f"rho={rho}: SAT zero-frac {sat_z}/{sat_n} = {sat_z/max(sat_n,1):.3f}   "
              f"UNSAT zero-frac {uns_z}/{uns_n} = {uns_z/max(uns_n,1):.3f}")
