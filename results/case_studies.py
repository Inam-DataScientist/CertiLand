"""Case-study data for the paper: deadline sweep and scalability (shield + certification only)."""
import json, time, numpy as np
from safeland.config import Config
from safeland.world import World
from safeland.logic.ltl import Monitor, parse_ltl
from safeland.product import Product
from safeland.shield import synthesize_sure, synthesize_prob, check_certificate, battery_reserve_map
from safeland.verification import certify, random_policy_baseline

base = "G(!crash & !collision & !nfz & !geofence & !empty)"
out = {"deadline": [], "scale": []}
for k in [None, 12, 10, 8, 6, 5, 4]:
    spec = base if k is None else f"{base} & G(low -> F[<={k}] landed)"
    cfg = Config.load(None, [f"spec.safety_ltl={spec}"])
    w = World(cfg.world); m = Monitor(parse_ltl(spec), w.alphabet); p = Product(w, m)
    sh = synthesize_sure(p); init = p.initial_states()
    rm = battery_reserve_map(p, sh, 3)
    out["deadline"].append(dict(k=k, monitor_states=m.n_states, product_states=p.n_states,
        W_start_frac=float(sh.winning[init].mean()), synth_s=sh.synthesis_time,
        mean_reserve=float(np.nanmean(rm)), max_reserve=float(np.nanmax(rm)),
        allowed=float(sh.allowed[sh.winning & ~p.terminal].sum(1).mean()), cert=check_certificate(p, sh).ok))
    print(out["deadline"][-1])
for n in [8, 12, 16, 24, 32]:
    cfg = Config.load(None, [f"world.width={n}", f"world.depth={n}"])
    t0 = time.perf_counter(); w = World(cfg.world); m = Monitor(parse_ltl(cfg.spec.safety_ltl), w.alphabet); p = Product(w, m); t_build = time.perf_counter() - t0
    sh = synthesize_sure(p)
    t0 = time.perf_counter(); c = check_certificate(p, sh); t_cert = time.perf_counter() - t0
    pol = np.argmax(sh.allowed, axis=1)  # a deterministic shield-compliant policy
    t0 = time.perf_counter(); cr = certify(p, pol, cfg.spec.ctl, cfg.spec.pctl); t_ver = time.perf_counter() - t0
    out["scale"].append(dict(grid=n, world_states=w.n_states, product_states=p.n_states, build_s=t_build,
        synth_s=sh.synthesis_time, iterations=sh.iterations, cert_s=t_cert, cert=c.ok,
        verify_s=t_ver, closed_loop_states=cr["closed_loop_states"], W_start_frac=float(sh.winning[p.initial_states()].mean())))
    print(out["scale"][-1])
json.dump(out, open("results/case_studies.json", "w"), indent=2)
