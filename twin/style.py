from __future__ import annotations

import re
import textstat
from statistics import mean
from typing import Any, Callable


def _call_first_existing(obj: Any, names: list[str], *args: Any, default: Any = None) -> Any:
    """Try multiple function names on a module/object and call the first that exists."""
    for name in names:
        fn: Callable[..., Any] | None = getattr(obj, name, None)
        if callable(fn):
            try:
                return fn(*args)
            except Exception:
                pass
    return default


def style_fingerprint(texts: list[str]) -> dict[str, float]:
    """
    Simple, explainable fingerprint from your writing.
    Compatible across textstat versions.
    """
    joined = "\n".join(texts).strip()
    if not joined:
        return {}

    exclaims = joined.count("!")
    questions = joined.count("?")
    emojis = len(re.findall(r"[\U0001F300-\U0001FAFF]", joined))

    sentences = [s for s in re.split(r"[.!?]\s+", joined) if s.strip()]
    sent_lengths = [float(len(s.split())) for s in sentences]
    avg_sent_len = float(mean(sent_lengths)) if sent_lengths else 0.0

    fk = _call_first_existing(
        textstat,
        ["flesch_kincaid_grade", "flesch_kincaid_grade_score", "flesch_kincaid_grade_level"],
        joined,
        default=None,
    )
    ease = _call_first_existing(
        textstat,
        ["flesch_reading_ease", "flesch_reading_ease_score"],
        joined,
        default=None,
    )

    out: dict[str, float] = {
        "exclaim_rate": float(exclaims / max(1, len(joined))),
        "question_rate": float(questions / max(1, len(joined))),
        "emoji_rate": float(emojis / max(1, len(joined))),
        "avg_sentence_words": avg_sent_len,
    }

    if fk is not None:
        out["readability_fk"] = float(fk)
    if ease is not None:
        out["readability_ease"] = float(ease)

    return out
