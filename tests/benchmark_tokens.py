"""
Benchmark script comparing Token Consumption Before vs After Serena-style AST optimizations.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from framework.core import Context
from framework.engines.token_economy import TokenEconomyEngine


def estimate_tokens(text: str) -> int:
    """Heuristic token estimation (~4 characters per token)."""
    return len(text) // 4


def run_benchmark():
    files_to_test = [
        ROOT / "framework" / "core" / "orchestrator.py",
        ROOT / "framework" / "scanners" / "code_scanner.py",
        ROOT / "framework" / "engines" / "discovery.py",
    ]

    engine = TokenEconomyEngine()

    print("=" * 80)
    print("BENCHMARK DE ECONOMIA DE TOKENS (SERENA MCP STYLE vs ANTES)")
    print("=" * 80)

    total_orig_chars = 0
    total_orig_tokens = 0
    total_legacy_tokens = 0
    total_serena_tokens = 0

    results_table = []

    for file_path in files_to_test:
        if not file_path.exists():
            continue

        raw_code = file_path.read_text(encoding="utf-8")
        orig_chars = len(raw_code)
        orig_tokens = estimate_tokens(raw_code)

        # 1. Modo Antigo (Legacy Token Economy - apenas filler words)
        ctx_legacy = Context()
        ctx_legacy.set("text", raw_code)
        ctx_legacy.set("mode", "conversational")
        res_legacy = engine.run(ctx_legacy)
        legacy_tokens = estimate_tokens(res_legacy.output["text"])

        # 2. Modo Novo (Serena MCP - AST Skeleton)
        ctx_serena = Context()
        ctx_serena.set("code", raw_code)
        ctx_serena.set("mode", "ast_skeleton")
        res_serena = engine.run(ctx_serena)
        serena_tokens = estimate_tokens(res_serena.output["text"])

        savings_tokens = orig_tokens - serena_tokens
        savings_pct = (savings_tokens / orig_tokens) * 100 if orig_tokens else 0

        # Totals
        total_orig_chars += orig_chars
        total_orig_tokens += orig_tokens
        total_legacy_tokens += legacy_tokens
        total_serena_tokens += serena_tokens

        results_table.append({
            "file": file_path.name,
            "orig_tokens": orig_tokens,
            "legacy_tokens": legacy_tokens,
            "serena_tokens": serena_tokens,
            "saved_tokens": savings_tokens,
            "economy_pct": f"{savings_pct:.1f}%",
        })

    # Imprimir tabela
    header = f"{'Arquivo':<24} | {'Tokens Originais':<16} | {'Modo Antigo':<14} | {'Modo Serena (Novo)':<18} | {'Tokens Salvos':<13} | {'Economia (%)':<12}"
    print(header)
    print("-" * len(header))
    for r in results_table:
        print(f"{r['file']:<24} | {r['orig_tokens']:<16} | {r['legacy_tokens']:<14} | {r['serena_tokens']:<18} | {r['saved_tokens']:<13} | {r['economy_pct']:<12}")

    total_saved = total_orig_tokens - total_serena_tokens
    total_pct = (total_saved / total_orig_tokens) * 100 if total_orig_tokens else 0
    print("-" * len(header))
    print(f"{'TOTAL ACUMULADO':<24} | {total_orig_tokens:<16} | {total_legacy_tokens:<14} | {total_serena_tokens:<18} | {total_saved:<13} | {total_pct:.1f}%")
    print("=" * 80)


if __name__ == "__main__":
    run_benchmark()
