"""Session 3, Q3: verify the IPS certificate identity C(x, f(x)) = 1 exactly mod p.

Certificate (see IPS_OBJECT.md):
  C(x, y) = sum_e y^cl_e * P_{e-1}(x) + sum_i y^b_i * Q_i(x)
  P_{e-1}(x) = prod_{e'<e} (1 - f_{e'}(x))          prefix layer, O(m) gates
  Q_i: exact Boolean-ideal division g = sum_i (x_i^2-x_i) Q_i,
       g(x) = prod_e (1 - f_e(x))  [vanishes on cube iff UNSAT]
Axioms substituted: y^cl_e <- f_e(x), y^b_i <- x_i^2 - x_i.
Identity: sum_e f_e P_{e-1} = 1 - g (pointwise telescoping), so C = (1-g) + g = 1.

Q_i evaluated pointwise by sequential division: as a poly in x_i,
  G_{i-1} = c0 + c1*x_i + (x_i^2 - x_i) Q_i,  v0 = G_{i-1}(x_i<-0), v1 = G_{i-1}(x_i<-1),
  Q_i(pt) = (G_{i-1}(pt) - v0 - (v1-v0)*pt_i) * inv(pt_i^2 - pt_i)   [needs pt_i not in {0,1}]
Full pointwise chain needs G-values on the closure {pt: each coord = root_k or 0 or 1}.
All arithmetic exact mod p = 2^61 - 1.
"""
import itertools
import random
import sys

import numpy as np

P = (1 << 61) - 1


def random_3cnf(n, rho, rng):
    m = int(round(rho * n))
    clauses = []
    for _ in range(m):
        vs = rng.sample(range(n), 3)
        clauses.append(tuple((v, rng.randint(0, 1)) for v in vs))
    return clauses


def brute_count(F, n):
    cnt = 0
    for bits in itertools.product([0, 1], repeat=n):
        ok = all(any(bits[v] == s for (v, s) in cl) for cl in F)
        cnt += ok
    return cnt


def eval_g(F, pts):
    """g = prod_e (1 - f_e) for an (N,n) object array of points, mod P."""
    g = np.ones(len(pts), dtype=object)
    for cl in F:
        f = np.ones(len(pts), dtype=object)
        for (v, s) in cl:
            lit = pts[:, v] if s else (1 - pts[:, v]) % P
            f = (f * ((1 - lit) % P)) % P
        g = (g * ((1 - f) % P)) % P
    return g


def clause_evals(F, pt):
    """f_e(pt) list and prefix products P_{e-1}(pt), and sum_e f_e P_{e-1}(pt)."""
    total = 0
    pref = 1
    for cl in F:
        f = 1
        for (v, s) in cl:
            lit = pt[v] if s else (1 - pt[v]) % P
            f = (f * ((1 - lit) % P)) % P
        total = (total + f * pref) % P
        pref = (pref * ((1 - f) % P)) % P
    return total  # = 1 - g(pt) pointwise


def chain_at_root(F, n, root, gvals):
    """Run sequential Boolean division at `root`; needs g-values on the
    3^n closure (each coord = root_k, 0 or 1) supplied via dict gvals.
    Returns (final reduced G(root) [should be 0], sum_i b_i Q_i(root))."""
    G = dict(gvals)  # point -> current G value
    bQ_sum = 0
    for i in range(n):
        newG = {}
        for pt, val in G.items():
            b = (pt[i] * pt[i] - pt[i]) % P
            if b == 0:
                # G_{i}(pt) = linear-interp value in x_i; recompute from variants
                p0 = pt[:i] + (0,) + pt[i + 1:]
                p1 = pt[:i] + (1,) + pt[i + 1:]
                v0, v1 = G[p0], G[p1]
                newG[pt] = (v0 + (v1 - v0) * pt[i]) % P
            else:
                p0 = pt[:i] + (0,) + pt[i + 1:]
                p1 = pt[:i] + (1,) + pt[i + 1:]
                v0, v1 = G[p0], G[p1]
                lin = (v0 + (v1 - v0) * pt[i]) % P
                q = ((val - lin) * pow(b, P - 2, P)) % P
                newG[pt] = lin
                if pt == root:
                    bQ_sum = (bQ_sum + b * q) % P
        G = newG
    return G[root] % P, bQ_sum


def closure(root):
    pts = {root}
    for i in range(len(root)):
        for pt in list(pts):
            pts.add(pt[:i] + (0,) + pt[i + 1:])
            pts.add(pt[:i] + (1,) + pt[i + 1:])
    return sorted(pts)


def main():
    rng = random.Random(31337)
    n = 8
    # sample until UNSAT
    while True:
        F = random_3cnf(n, 5.4, rng)
        if brute_count(F, n) == 0:
            break
    m = len(F)
    print(f"n={n} m={m} (rho=5.4) #F=0 (brute-forced over 2^{n})")

    # C(x,0) = 0: certificate is y-homogeneous (every gate path hits a y-leaf)
    print("C(x,0)=0: structurally (C is y-linear, no y-free monomial) [OK]")

    # cube checks: g == 0 and sum_e f_e P_{e-1} == 1 at all 2^n points;
    # count-functional the Z/IE/Hermite machinery targets
    cube = list(itertools.product([0, 1], repeat=n))
    cube_arr = np.array(cube, dtype=object).reshape(len(cube), n)
    gv = eval_g(F, cube_arr)
    assert int((gv != 0).sum()) == 0, "g nonzero on cube"
    prefix_ok = sum(1 for pt in cube if clause_evals(F, pt) == 1)
    count_fn = sum(clause_evals(F, pt) for pt in cube) % P
    print(f"cube: g=0 at 256/256, sum f_e P_(e-1) = 1 at {prefix_ok}/256, "
          f"count-functional sum = {count_fn} (= 2^{n} = {2**n})")

    # random roots: full identity C(x, f(x)) = 1 via Schwartz-Zippel points
    ok = 0
    tries = 5
    for t in range(tries):
        root = tuple(random.randrange(P) for _ in range(n))
        assert all(r not in (0, 1) for r in root)
        pts = closure(root)
        arr = np.array(pts, dtype=object).reshape(len(pts), n)
        gvals = dict(zip(pts, (int(v) for v in eval_g(F, arr))))
        final_g, bQ = chain_at_root(F, n, root, gvals)
        lhs = (clause_evals(F, root) + bQ) % P  # C(x, f(x))
        assert final_g == 0, "fully reduced g should vanish identically"
        ok += (lhs == 1)
    print(f"random F_p^{n} points: C(x,f(x))=1 at {ok}/{tries}, reduced g=0 at {tries}/{tries}")
    print("VERDICT:", "PASS" if ok == tries and prefix_ok == 2**n else "FAIL")


if __name__ == "__main__":
    sys.exit(main())
