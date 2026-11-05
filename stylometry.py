"""
Signal two: the style signal. (Milestone 4)

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────

# Punctuation I count. I left out periods because every sentence has one, so
# they don't tell you anything. Dashes, semicolons, colons, quotes and brackets
# are the ones that change a lot from writer to writer.
INTERESTING_PUNCT = r"[,;:\u2014\u2013()\"!?]|--"

# Window size for the type-token ratio (see type_token_ratio below).
TTR_WINDOW = 40


def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies.

    I use the standard deviation of sentence lengths (in words) divided by the
    mean, so a long text and a short text can be compared.
    0 means every sentence is the same length. Higher means more uneven.
    HIGHER = MORE HUMAN.

    Edge case: with only one sentence there is no spread to measure, and
    stdev crashes on fewer than two values, so I return 0.0 here. style_signal
    checks for this and treats it as "no evidence" instead of "very AI".
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, between 0 and 1. Higher = more varied words.

    Plain TTR goes down as text gets longer, so instead I take the average TTR
    over every 40-word window (people call this moving-average TTR). That way a
    300 word text and a 60 word text are on the same scale. If the text is
    shorter than one window I just use plain TTR.

    Direction: the starter says AI has a narrower vocabulary, but my test texts
    did the opposite. The clearly-AI text scored 0.94 and the clearly-human one
    scored 0.83. Formal AI writing keeps using new "big" words, and casual
    human writing repeats little words like "I", "and", "she". So for me
    HIGHER = MORE AI. I only have three texts though, so I don't trust this
    much and it gets the smallest weight.
    """
    w = words(text)
    if not w:
        return 0.0
    if len(w) <= TTR_WINDOW:
        return len(set(w)) / len(w)
    windows = [w[i:i + TTR_WINDOW] for i in range(len(w) - TTR_WINDOW + 1)]
    return statistics.mean(len(set(win)) / TTR_WINDOW for win in windows)


def punctuation_density(text: str) -> float:
    """
    Interesting punctuation marks per word (see INTERESTING_PUNCT).

    0.04 means about one mark every 25 words. HIGHER = MORE HUMAN.
    """
    w = words(text)
    if not w:
        return 0.0
    return len(re.findall(INTERESTING_PUNCT, text)) / len(w)


# ── Combining them ───────────────────────────────────────────────────────────

# How much each measure counts. Spread and punctuation matched what I expected
# on my test texts, vocab variety was the surprise, so it counts the least.
WEIGHT_SPREAD = 0.4
WEIGHT_PUNCT = 0.4
WEIGHT_TTR = 0.2


def _squash(value: float, low: float, high: float) -> float:
    """Map value onto 0-1, where low -> 0 and high -> 1, clamped at the ends."""
    return max(0.0, min(1.0, (value - low) / (high - low)))


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. HIGHER = MORE LIKELY AI.

    Each measure gets turned into its own 0-1 "how AI does this look" score,
    then I take a weighted average (0.4 spread, 0.4 punctuation, 0.2 vocab).

    The low/high numbers come from looking at my three test texts:
      spread:      0.3 or less -> 1 (very even, AI-ish), 1.0 or more -> 0
                   (flipped, because more spread = more human)
      punctuation: 0.02 or less -> 1, 0.12 or more -> 0 (also flipped)
      vocab:       0.80 or less -> 0, 0.95 or more -> 1 (not flipped, see
                   type_token_ratio for why)

    If there's only one sentence, the spread part is set to 0.5 (no opinion)
    so a short one-liner doesn't get called AI just for being short.
    """
    if len(sentences(text)) < 2:
        spread_ai = 0.5
    else:
        spread_ai = 1 - _squash(sentence_length_spread(text), 0.3, 1.0)
    punct_ai = 1 - _squash(punctuation_density(text), 0.02, 0.12)
    ttr_ai = _squash(type_token_ratio(text), 0.80, 0.95)

    score = (WEIGHT_SPREAD * spread_ai
             + WEIGHT_PUNCT * punct_ai
             + WEIGHT_TTR * ttr_ai)
    return round(score, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
