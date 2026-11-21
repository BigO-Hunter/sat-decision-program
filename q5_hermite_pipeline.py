"""Session 6, Q5: the paper's FULL counting pipeline at small n (Hermite/Taylor route).

Implements subsec:preview-interpolation (tex ~813-945) end-to-end, per the CERTIFICATE:
  1. R=1 deformation family (q1's): P_{e,v}(T) = (1-T)e_v + T L_{e,v}, random
     small-int L. Delta P_{e,v}(z) = P(t+z)-P(t) = z(L - e_v).
  2. G_x(X,z) = prod_e Phi_e( (<P_{e,v}(t),x> + <Delta P_{e,v}(z), X>)_{v in I_e} ),
     Phi_e = 1 - prod(1 - lit_i), literal = r (s=1) or 1-r (s=0).
  3. Restricted sums Z_{t,E,U}(z) = sum_{x: x_E=1} G_x(1_U,z) mod z^J for ALL
     U subseteq E, |E| <= q.
  4. Inclusion-exclusion (eq:outline-taylor-recovery): H(t+z) = sum_{E,U}
     (-1)^{|E|-|U|} Z_{t,E,U}(z) mod z^J  -- verified coefficient-exact vs the
     Taylor shift of independently computed H.
  5. Hermite linear solve: Q*J equations sum_k H[k] C(k,j) t^{k-j} = [z^j]H(t+z);
     QJ > deg H pins H uniquely; solved mod p; H(0) must equal #F.

ARITHMETIC DISCIPLINE (session-5 run was voided by numpy int64 coercion):
zero numpy. Pure-Python ints mod p = 2^61-1 at every boundary; sampled
self-checks assert values in [0, 2^62).

FLAGGED DISCREPANCY (regime, not tex error): the tex sets q = floor(3nR/Q)
under bounded occurrence M <= 3n (CERTIFICATE line 13). Random density-rho
instances have M = 3m = 3*rho*n > 3n for rho > 1, so the tex's literal q would
break the uniqueness QJ > deg H. We set q = floor(M*R/Q), which EQUALS the
tex's value in the paper's own M <= 3n regime.
"""
import itertools
import random
import sys
import time

P = (1 << 61) - 1
R = 1
Q = 4
TWO62 = 1 << 62


def pmul(a, b, trunc):
    """(a*b) as polys, truncated at x^trunc, coefficients mod P. Pure ints."""
    la, lb = len(a), len(b)
    n_out = la + lb - 1
    if n_out > trunc:
        n_out = trunc
    raw = [0] * n_out
    for i in range(la if la < n_out else n_out):
        ai = a[i]
        if ai:
            lim = lb if lb < n_out - i else n_out - i
            for j in range(lim):
                bj = b[j]
                if bj:
                    raw[i + j] += ai * bj
    return [v % P for v in raw]


def eval_G(Af, Bf, J, CLZ):
    """G_x(1_U, z) mod z^J. Af[oi] = <P(t),x> part (scalar), Bf[oi] = z-coeff
    <L,1_U> - 1_U[v] (scalar). CLZ = clauses as tuples of (flat occ idx, sign).
    Phi_e = 1 - prod(1 - lit); lit = A + zB if s=1 else 1 - (A + zB)."""
    acc = [1]
    for cls in CLZ:
        prod = [1]
        for oi, s in cls:
            A, B = Af[oi], Bf[oi]
            if s:
                a0 = (1 - A) % P
                om = [a0, P - B] if B else [a0]
            else:
                om = [A, B] if B else [A]
            prod = pmul(prod, om, 4)
        phi = [(1 - prod[0]) % P] + [P - c if c else 0 for c in prod[1:]]
        acc = pmul(acc, phi, J)
        if len(acc) == 1 and acc[0] == 0:
            return [0] * J
    if len(acc) < J:
        acc = acc + [0] * (J - len(acc))
    return acc


def supersets(U, full):
    """Yield all x with U <= x (bitmask)."""
    comp = full ^ U
    s = comp
    while True:
        yield U | s
        if s == 0:
            return
        s = (s - 1) & comp


def brute_count(F, n):
    cnt = 0
    for bits in itertools.product([0, 1], repeat=n):
        ok = True
        for clause in F:
            sat = False
            for v, s in clause:
                if bits[v] == s:
                    sat = True
                    break
            if not sat:
                ok = False
                break
        if ok:
            cnt += 1
    return cnt


def random_3cnf(n, rho, rng):
    m = int(round(rho * n))
    clauses = []
    for _ in range(m):
        vs = rng.sample(range(n), 3)
        clauses.append(tuple((v, rng.randint(0, 1)) for v in vs))
    return clauses


def pascal(D):
    C = [[0] * (D + 1) for _ in range(D + 1)]
    for k in range(D + 1):
        C[k][0] = 1
        for j in range(1, k + 1):
            C[k][j] = (C[k - 1][j - 1] + C[k - 1][j]) % P
    return C


def taylor_shift(H, t, J, Cnk):
    """[z^j] H(t+z) for j < J, mod p."""
    tp = [pow(t, i, P) for i in range(len(H))]
    out = []
    for j in range(J):
        c = 0
        for k in range(j, len(H)):
            hk = H[k]
            if hk:
                c += hk * Cnk[k][j] * tp[k - j]
        out.append(c % P)
    return out


def gauss_solve(rows, rhs, ncols):
    """Unique solution mod p, or 'RANK-DEFICIENT' / 'INCONSISTENT'."""
    A = [r[:] + [b] for r, b in zip(rows, rhs)]
    nrows = len(A)
    r = 0
    for c in range(ncols):
        piv = -1
        for i in range(r, nrows):
            if A[i][c]:
                piv = i
                break
        if piv < 0:
            return "RANK-DEFICIENT"
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], P - 2, P)
        Av = A[r]
        for j in range(c, ncols + 1):
            Av[j] = Av[j] * inv % P
        for i in range(nrows):
            if i != r and A[i][c]:
                f = A[i][c]
                Ai = A[i]
                for j in range(c, ncols + 1):
                    Ai[j] = (Ai[j] - f * Av[j]) % P
        r += 1
    for i in range(r, nrows):
        if any(A[i][j] for j in range(ncols)) or A[i][ncols]:
            return "INCONSISTENT"
    return [A[i][ncols] for i in range(ncols)]


def check62(vals, label):
    for v in vals:
        assert 0 <= v < TWO62, f"{label}: value {v} outside [0, 2^62)"


def run_instance(n, rho, seed, chk_ctr):
    frng = random.Random(seed)
    lrng = random.Random(seed + 777)
    F = random_3cnf(n, rho, frng)
    m = len(F)
    L = [[[lrng.randint(-3, 3) for _ in range(n)] for _ in range(3)] for _ in F]
    nF = brute_count(F, n)

    D = 3 * m * R  # deg H <= (#occurrences)*R
    q = D // Q
    J = q + 1
    assert Q * J > D, f"uniqueness broken: QJ={Q * J} <= D={D}"

    # flat occurrences
    occ = []  # (v, s, Lvec)
    CLZ = []
    for e, clause in enumerate(F):
        cls = []
        for j, (v, s) in enumerate(clause):
            cls.append((len(occ), s))
            occ.append((v, s, L[e][j]))
        CLZ.append(tuple(cls))
    K = len(occ)
    full = (1 << n) - 1

    # DOT[x][oi] = <L_oi, x>;  A0[x][oi] = x_v;  B_all[U][oi] = <L,1_U> - 1_U[v]
    xs = list(range(1 << n))
    DOT = []
    for x in xs:
        bits = [(x >> i) & 1 for i in range(n)]
        row = []
        for v, s, Lv in occ:
            d = 0
            for i in range(n):
                if bits[i] and Lv[i]:
                    d += Lv[i]
            row.append(d % P)
        DOT.append(row)
    A0 = [[(x >> v) & 1 for (v, s, Lv) in occ] for x in xs]
    B_all = []
    for U in range(1 << n):
        Ubits = [i for i in range(n) if (U >> i) & 1]
        Uset = set(Ubits)
        row = []
        for v, s, Lv in occ:
            d = sum(Lv[i] for i in Ubits)
            row.append((d - (1 if v in Uset else 0)) % P)
        B_all.append(row)

    # direct H (independent reference): H(T) = sum_x G_x(1_x, z) at t=0, exact deg.
    D1 = D + 1
    Hdir = [0] * D1
    for x in xs:
        g = eval_G(A0[x], B_all[x], D1, CLZ)
        for i in range(D1):
            Hdir[i] = (Hdir[i] + g[i]) % P
    sanity_direct = Hdir[0] == nF % P
    check62(Hdir, "Hdir")

    Cnk = pascal(D)

    # pipeline: per t, all restricted sums + IE
    S_all = {}
    ident_coeffs_ok = 0
    ident_coeffs_tot = 0
    nz_Z = 0
    tot_Z = 0
    for t in range(1, Q + 1):
        A_t = [[((1 - t) * A0[x][oi] + t * DOT[x][oi]) % P for oi in range(K)] for x in xs]
        S = [0] * J
        for U in range(1 << n):
            Bf = B_all[U]
            gU = [None] * (1 << n)
            for x in supersets(U, full):
                gU[x] = eval_G(A_t[x], Bf, J, CLZ)
            for E in supersets(U, full):
                if bin(E).count("1") > q:
                    continue
                raw = [0] * J
                for x in supersets(E, full):
                    gp = gU[x]
                    for i in range(J):
                        raw[i] += gp[i]
                Zp = [v % P for v in raw]
                tot_Z += 1
                if any(Zp):
                    nz_Z += 1
                chk_ctr[0] += 1
                if chk_ctr[0] % 977 == 0:
                    check62(Zp, "Z")
                sgn = -1 if ((bin(E).count("1") - bin(U).count("1")) & 1) else 1
                if sgn > 0:
                    for i in range(J):
                        S[i] = (S[i] + Zp[i]) % P
                else:
                    for i in range(J):
                        S[i] = (S[i] - Zp[i]) % P
        S_all[t] = S
        Tsh = taylor_shift(Hdir, t, J, Cnk)
        ident_coeffs_tot += J
        ident_coeffs_ok += sum(1 for a, b in zip(S, Tsh) if a == b)

    # Hermite solve
    rows, rhs = [], []
    for t in range(1, Q + 1):
        S = S_all[t]
        tp = [pow(t, i, P) for i in range(D1)]
        for j in range(J):
            row = [0] * D1
            for k in range(j, D1):
                row[k] = Cnk[k][j] * tp[k - j] % P
            rows.append(row)
            rhs.append(S[j])
    sol = gauss_solve(rows, rhs, D1)
    if isinstance(sol, list):
        check62(sol, "sol")
        solve_ok = sol[0] == nF % P
        full_ok = sol == Hdir
        note = ""
    else:
        solve_ok = full_ok = False
        note = sol
    return dict(n=n, rho=rho, m=m, D=D, q=q, J=J, nF=nF, sat=nF > 0,
                sanity_direct=sanity_direct,
                ident_ok=ident_coeffs_ok, ident_tot=ident_coeffs_tot,
                nz_Z=nz_Z, tot_Z=tot_Z, solve_ok=solve_ok, full_ok=full_ok,
                note=note)


def main():
    per = {6: 3, 7: 2, 8: 2, 9: 1}
    if len(sys.argv) >= 3:
        per = {int(sys.argv[1]): int(sys.argv[2])}
    chk_ctr = [0]
    print(f"Q={Q}, R={R}, p=2^61-1, pure-Python ints (no numpy)", flush=True)
    hdr = f"{'n':>2} {'rho':>5} {'m':>3} {'q':>3} {'J':>3} {'#F':>6} {'SAT':>3} " \
          f"{'sanity':>6} {'ident':>9} {'solve':>5} {'fullH':>5}  note"
    print(hdr, flush=True)
    t0 = time.time()
    n_sat = n_unsat = 0
    for n in sorted(per):
        for rho in (3.5, 4.26, 5.0):
            for i in range(per[n]):
                seed = 20261031 + 1000 * n + int(rho * 100) * 10 + i
                t1 = time.time()
                r = run_instance(n, rho, seed, chk_ctr)
                dt = time.time() - t1
                if r["sat"]:
                    n_sat += 1
                else:
                    n_unsat += 1
                print(f"{r['n']:>2} {r['rho']:>5} {r['m']:>3} {r['q']:>3} {r['J']:>3} "
                      f"{r['nF']:>6} {'Y' if r['sat'] else 'N':>3} "
                      f"{'OK' if r['sanity_direct'] else 'FAIL':>6} "
                      f"{r['ident_ok']:>4}/{r['ident_tot']:<4} "
                      f"{'OK' if r['solve_ok'] else 'FAIL':>5} "
                      f"{'OK' if r['full_ok'] else 'FAIL':>5}  {r['note']} "
                      f"({dt:.1f}s, nzZ={r['nz_Z']}/{r['tot_Z']})", flush=True)
    print(f"\ntotal {time.time() - t0:.0f}s; SAT={n_sat} UNSAT={n_unsat}; "
          f"bound-checks sampled at {chk_ctr[0]} Z-evals", flush=True)


if __name__ == "__main__":
    main()
