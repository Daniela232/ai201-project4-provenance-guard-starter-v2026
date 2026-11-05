"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0-1 signals into one 0-1 score. Higher = more likely AI.

    My rule (rule 2, "disagreement means unsure"):

      1. Take the weighted average (0.5 model, 0.5 style, set in config.py).
      2. If the two signals are more than 0.3 apart, they disagree. Then I
         pull the average halfway back toward 0.5.

    Why: in my Milestone 1 notes I decided something should only get a
    confident "AI" label if both signals agree, because calling a real writer
    AI is the worst mistake this system can make. With this rule one signal
    can't get someone accused on its own.

    The cost: real human writing can land in "unsure" too. My clearly-human
    test text got model 0.445 and style 0.057 (a 0.39 gap), so it gets pulled
    from 0.25 to about 0.38. I'm ok with that because "unsure" hurts a lot
    less than a wrong accusation.
    """
    average = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )

    if abs(model_score - style_score) > config.DISAGREEMENT_GAP:
        average = average + (0.5 - average) * config.DISAGREEMENT_PULL

    return round(average, 4)


# The three labels, exactly as a writer sees them. Every one says how to
# appeal, because in my Milestone 1 notes I decided nobody should have to go
# looking for that.
LABEL_AI = (
    "This looks like it was written by AI. If you wrote this yourself, you "
    "can appeal and a real person will review it."
)
LABEL_HUMAN = (
    "This looks like it was written by a person. If you think something is "
    "wrong with this result, you can still appeal."
)
LABEL_UNSURE = (
    "We couldn't get an accurate read on this one, so we can't say whether a "
    "person or AI wrote it. This is not an accusation. If you have questions, "
    "you can appeal and a real person will review it."
)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a combined score into (guess, label_text).

      score below 0.40       -> "human"
      0.40 up to 0.70        -> "unsure"
      score above 0.70       -> "ai"

    The thresholds live in config.py. Every score from 0 to 1 lands in exactly
    one of these, so there are no gaps.
    """
    if score > config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score < config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
