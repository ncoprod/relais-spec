"""Check that the spec is consistent: schema valid, examples conform, taxonomy codes unique,
memo ids prefixed by their firm, domains and countries known. Usage: python scripts/validate.py [memo dirs...]"""
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def main(extra_dirs):
    errors = []
    schema = load(ROOT / "schema/memo.schema.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    countries = [c["iso"] for c in load(ROOT / "taxonomy/countries.json")["countries"]]
    domains = [d["code"] for d in load(ROOT / "taxonomy/domains.json")["domains"]]
    for name, codes in (("country", countries), ("domain", domains)):
        dup = {c for c in codes if codes.count(c) > 1}
        if dup:
            errors.append(f"duplicate {name} codes: {sorted(dup)}")

    yaml.safe_load((ROOT / "api/openapi.yaml").read_text(encoding="utf-8"))

    files = list((ROOT / "examples").glob("*.json"))
    for d in extra_dirs:
        files += sorted(Path(d).rglob("*.json"))
    for f in files:
        memo = load(f)
        for e in validator.iter_errors(memo):
            errors.append(f"{f.name}: {'/'.join(map(str, e.path))}: {e.message}")
        if not memo["id"].startswith(memo["firm"]["iso"].lower() + "-"):
            errors.append(f"{f.name}: id must start with the firm iso code")
        for j in memo["jurisdictions"] + [memo["firm"]["iso"]]:
            if j not in countries:
                errors.append(f"{f.name}: unknown country {j}")
        for dom in memo["domains"]:
            if dom not in domains:
                errors.append(f"{f.name}: unknown domain {dom}")
        ids = [p["id"] for p in memo["passages"]]
        if len(ids) != len(set(ids)):
            errors.append(f"{f.name}: duplicate passage ids")

    for e in errors:
        print("ERROR", e)
    print(f"{len(files)} memo file(s), {len(countries)} countries, {len(domains)} domains, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
