"""Generate beauty content ideas."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import cycle, islice

from .data import FEATURES, SAFE_LANGUAGE_NOTES


@dataclass(frozen=True)
class ContentIdea:
    """A single short-video content idea."""

    feature: str
    hook: str
    angle: str
    cta: str
    safety_note: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ScriptOutline:
    """A short-video script outline derived from a content idea."""

    idea: ContentIdea
    opening: str
    conflict: str
    guidance: str
    proof_prompt: str
    cta: str

    def to_dict(self) -> dict[str, object]:
        return {
            "idea": self.idea.to_dict(),
            "opening": self.opening,
            "conflict": self.conflict,
            "guidance": self.guidance,
            "proof_prompt": self.proof_prompt,
            "cta": self.cta,
        }


def supported_features() -> tuple[str, ...]:
    """Return supported feature keys."""

    return tuple(FEATURES.keys())


def generate_ideas(feature: str, count: int = 5) -> list[ContentIdea]:
    """Generate content ideas for one feature or all features."""

    if count < 1:
        raise ValueError("count must be at least 1")

    features = _resolve_features(feature)
    ideas: list[ContentIdea] = []

    for feature_key in cycle(features):
        data = FEATURES[feature_key]
        index = len([idea for idea in ideas if idea.feature == feature_key])
        hook = data["hooks"][index % len(data["hooks"])]
        angle = data["angles"][index % len(data["angles"])]
        cta = data["ctas"][index % len(data["ctas"])]
        safety_note = SAFE_LANGUAGE_NOTES[index % len(SAFE_LANGUAGE_NOTES)]
        ideas.append(
            ContentIdea(
                feature=feature_key,
                hook=hook,
                angle=angle,
                cta=cta,
                safety_note=safety_note,
            )
        )

        if len(ideas) == count:
            break

    return ideas


def generate_outlines(feature: str, count: int = 3) -> list[ScriptOutline]:
    """Generate reusable short-video script outlines."""

    ideas = generate_ideas(feature, count)
    return [outline_from_idea(idea) for idea in ideas]


def outline_from_idea(idea: ContentIdea) -> ScriptOutline:
    """Convert a content idea into a practical short-video outline."""

    return ScriptOutline(
        idea=idea,
        opening=f"Open with the hook: {idea.hook}",
        conflict=f"Name the client concern behind this topic: {idea.angle}.",
        guidance=(
            "Explain one practical judgment point, then remind viewers that a "
            "real consultation should confirm fit before any service."
        ),
        proof_prompt=(
            "Show a checklist, consultation note, before-after expectation, or "
            "safe wording example instead of making a guaranteed claim."
        ),
        cta=idea.cta,
    )


def _resolve_features(feature: str) -> tuple[str, ...]:
    normalized = feature.strip().lower()
    if normalized == "all":
        return supported_features()
    if normalized not in FEATURES:
        valid = ", ".join((*supported_features(), "all"))
        raise ValueError(f"unknown feature '{feature}'. Choose one of: {valid}")
    return (normalized,)


def preview_lines(ideas: list[ContentIdea]) -> list[str]:
    """Format ideas as human-readable CLI output."""

    lines: list[str] = []
    for number, idea in enumerate(ideas, start=1):
        lines.extend(
            [
                f"{number}. {idea.hook}",
                f"   Feature: {idea.feature}",
                f"   Angle: {idea.angle}",
                f"   CTA: {idea.cta}",
                f"   Safety: {idea.safety_note}",
            ]
        )
    return list(islice(lines, None))


def outline_lines(outlines: list[ScriptOutline]) -> list[str]:
    """Format script outlines as human-readable CLI output."""

    lines: list[str] = []
    for number, outline in enumerate(outlines, start=1):
        lines.extend(
            [
                f"{number}. {outline.idea.hook}",
                f"   Feature: {outline.idea.feature}",
                f"   Opening: {outline.opening}",
                f"   Conflict: {outline.conflict}",
                f"   Guidance: {outline.guidance}",
                f"   Proof: {outline.proof_prompt}",
                f"   CTA: {outline.cta}",
                f"   Safety: {outline.idea.safety_note}",
            ]
        )
    return lines
