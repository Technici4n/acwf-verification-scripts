import json

METRIC = "epsilon"
EXCELLENT_THR = 0.06
GOOD_THR = 0.2

SRC = "DFTK-0.5.1-fix"
REF = ["ae", "ABINIT"]
SET = ["oxides", "unaries"]

for ref in REF:
    for set_name in SET:
        with open(f"{METRIC}-{set_name}-{SRC}-vs-{ref}.json", "r") as f:
            data = json.load(f)
        excellent_count = 0
        good_count = 0
        bad_count = 0
        bad_keys = []
        total_count = len(data)
        for k, v in data.items():
            if v < EXCELLENT_THR:
                excellent_count += 1
            elif v < GOOD_THR:
                good_count += 1
            else:
                bad_count += 1
                bad_keys.append(k)
        print(f"{SRC} vs {ref} ({set_name}):")
        print(f"  Excellent: {excellent_count} ({excellent_count/total_count:.2%})")
        print(f"  Good: {good_count} ({good_count/total_count:.2%})")
        print(f"  Bad: {bad_count} ({bad_count/total_count:.2%})")
        print(f"    bad systems: {sorted(bad_keys)}")