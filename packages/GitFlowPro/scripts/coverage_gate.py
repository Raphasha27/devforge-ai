import json
import os
import sys

THRESHOLD_DROP_ALLOWED = float(os.getenv("COVERAGE_DROP_ALLOWED", "0.0"))


def load_coverage(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Coverage file not found: {filepath}")
        return None

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data.get("totals", {}).get("percent_covered", None)
    except Exception as e:
        print(f"❌ Error loading coverage from {filepath}: {e}")
        return None


def main():
    base_cov = load_coverage("coverage_main.json")
    pr_cov = load_coverage("coverage_pr.json")

    if base_cov is None or pr_cov is None:
        print("⚠️ Missing coverage files. Skipping gate.")
        sys.exit(0)

    drop = base_cov - pr_cov

    print(f"📌 Main Coverage: {base_cov:.2f}%")
    print(f"📌 PR Coverage:   {pr_cov:.2f}%")
    print(f"📉 Coverage Drop: {drop:.2f}%")

    if drop > THRESHOLD_DROP_ALLOWED:
        print(f"❌ Coverage dropped more than allowed ({THRESHOLD_DROP_ALLOWED}%).")
        sys.exit(1)

    print("✅ Coverage gate passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
