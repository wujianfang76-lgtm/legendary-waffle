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
