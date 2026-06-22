import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOWNLOADS_PDF = Path.home() / "Downloads" / "106.pdf"
DESKTOP_PDF = Path.home() / "Desktop" / "106.pdf"
ROOT_PDF = ROOT.parent / "106.pdf"

EXPECTED_ROWS = {
    "dataset_summary_rows": 3840,
    "main_rollout_rows": 345600,
    "main_group_rows": 57600,
    "main_seed_metric_rows": 150,
    "main_metric_rows": 120,
    "hard_seed_rows": 150,
    "hard_metric_rows": 15,
    "hard_pairwise_rows": 14,
    "ablation_rollout_rows": 115200,
    "ablation_seed_rows": 100,
    "ablation_metric_rows": 10,
    "stress_rollout_rows": 288000,
    "stress_seed_rows": 1000,
    "stress_metric_rows": 100,
    "fixed_risk_rows": 276480,
    "fixed_risk_seed_rows": 480,
    "fixed_risk_metric_rows": 48,
    "fixed_risk_pairwise_rows": 44,
    "failure_case_rows": 24,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def page_count(path: Path) -> int:
    try:
        from pypdf import PdfReader
    except Exception:
        from PyPDF2 import PdfReader
    return len(PdfReader(str(path)).pages)


def count_csv(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def assert_finite_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row_index, row in enumerate(reader, start=1):
            for key, value in row.items():
                if value is None or value == "":
                    continue
                try:
                    number = float(value)
                except ValueError:
                    continue
                if not math.isfinite(number):
                    raise AssertionError(f"non-finite value in {path}:{row_index}:{key}")


def main():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    if summary["terminal_decision"] != "STRONG_REVISE":
        raise AssertionError("terminal decision is not STRONG_REVISE")
    if summary["iclr_main_ready"]:
        raise AssertionError("scope gate should keep ICLR main readiness false")
    for key, expected in EXPECTED_ROWS.items():
        actual = int(summary["row_counts"][key])
        if actual != expected:
            raise AssertionError(f"{key}: expected {expected}, got {actual}")

    file_rows = {
        "dataset_summary_rows": RESULTS / "dataset_summary.csv",
        "main_rollout_rows": RESULTS / "rollouts.csv",
        "main_group_rows": RESULTS / "main_group_metrics.csv",
        "main_metric_rows": RESULTS / "metrics.csv",
        "hard_metric_rows": RESULTS / "hard_aggregate_metrics.csv",
        "ablation_rollout_rows": RESULTS / "ablation_rollouts.csv",
        "stress_rollout_rows": RESULTS / "stress_sweep_raw.csv",
        "fixed_risk_rows": RESULTS / "fixed_risk_raw.csv",
        "failure_case_rows": RESULTS / "failure_cases.csv",
    }
    for key, path in file_rows.items():
        actual = count_csv(path)
        if actual != EXPECTED_ROWS[key]:
            raise AssertionError(f"{path} row count expected {EXPECTED_ROWS[key]}, got {actual}")
        assert_finite_csv(path)

    tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    if "citebordercolor={0 0.85 0.20}" not in tex or "pdfborder={0 0 1.5}" not in tex:
        raise AssertionError("bright boxed citation hyperref settings missing")
    if "ICLR main ready is \\textbf{no}" not in tex:
        raise AssertionError("scope-gate sentence missing")

    paper_pdf = PAPER / "main.pdf"
    if not paper_pdf.exists():
        raise AssertionError("paper/main.pdf missing")
    if not DOWNLOADS_PDF.exists():
        raise AssertionError("Downloads/106.pdf missing")
    if DESKTOP_PDF.exists():
        raise AssertionError("visible Desktop 106.pdf must not exist")
    if ROOT_PDF.exists():
        raise AssertionError("factory-root 106.pdf must not exist")
    pages = page_count(paper_pdf)
    if pages < 25:
        raise AssertionError(f"paper is too short: {pages} pages")
    paper_hash = sha256(paper_pdf)
    downloads_hash = sha256(DOWNLOADS_PDF)
    if paper_hash != downloads_hash:
        raise AssertionError("Downloads PDF hash does not match paper/main.pdf")
    print(f"validated Paper 106 artifacts: pages={pages}, sha256={paper_hash}")


if __name__ == "__main__":
    main()
