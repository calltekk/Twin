from __future__ import annotations

def generate_reply(prompt: str, retrieved_texts: list[str], fingerprint: dict) -> str:
    """
    MVP generator (non-LLM) that still looks impressive:
    - Uses your retrieved writing as "voice examples"
    - Produces a structured reply template
    Later: swap for an LLM call.
    """
    examples = "\n\n---\n\n".join(retrieved_texts[:3])

    # A “twin-like” response format: summary + response + tone rules
    tone_notes = []
    if fingerprint:
        if fingerprint.get("avg_sentence_words", 0) < 12:
            tone_notes.append("Keep sentences punchy.")
        else:
            tone_notes.append("Allow longer, more analytical sentences.")
        if fingerprint.get("question_rate", 0) > fingerprint.get("exclaim_rate", 0):
            tone_notes.append("Use questions to engage.")
        if fingerprint.get("emoji_rate", 0) > 0:
            tone_notes.append("Optional: add a light emoji if it fits.")
    tone = " ".join(tone_notes) if tone_notes else "Match the user’s typical tone."

    return (
        "DIGITAL TWIN (MVP)\n"
        "==================\n\n"
        f"Prompt:\n{prompt}\n\n"
        "Voice references (most similar past writing):\n"
        f"{examples}\n\n"
        "Draft reply (template):\n"
        "- Acknowledge clearly.\n"
        "- Respond directly.\n"
        "- Add one personal-style flourish.\n\n"
        "Suggested reply:\n"
        f"(Write your reply here, following: {tone})\n"
    )
