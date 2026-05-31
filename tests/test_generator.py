import pytest

from beauty_content_kit.generator import (
    generate_ideas,
    generate_outlines,
    outline_from_idea,
    outline_lines,
    preview_lines,
    supported_features,
)


def test_supported_features_include_core_beauty_areas():
    assert supported_features() == ("lip", "brow", "eye")


def test_generate_lip_ideas_count_and_shape():
    ideas = generate_ideas("lip", count=3)

    assert len(ideas) == 3
    assert all(idea.feature == "lip" for idea in ideas)
    assert "纹唇" in ideas[0].hook
    assert ideas[0].cta
    assert ideas[0].safety_note


def test_generate_all_rotates_features():
    ideas = generate_ideas("all", count=4)

    assert [idea.feature for idea in ideas] == ["lip", "brow", "eye", "lip"]


def test_generate_rejects_invalid_count():
    with pytest.raises(ValueError, match="count must be at least 1"):
        generate_ideas("lip", count=0)


def test_generate_rejects_unknown_feature():
    with pytest.raises(ValueError, match="unknown feature"):
        generate_ideas("nose", count=1)


def test_preview_lines_contains_numbered_hook():
    lines = preview_lines(generate_ideas("brow", count=1))

    assert lines[0].startswith("1. ")
    assert "Angle:" in lines[2]


def test_outline_from_idea_preserves_cta_and_safety_context():
    idea = generate_ideas("eye", count=1)[0]
    outline = outline_from_idea(idea)

    assert outline.idea == idea
    assert outline.cta == idea.cta
    assert "guaranteed claim" in outline.proof_prompt


def test_generate_outlines_supports_all_features():
    outlines = generate_outlines("all", count=3)

    assert [outline.idea.feature for outline in outlines] == ["lip", "brow", "eye"]


def test_outline_lines_contains_script_sections():
    lines = outline_lines(generate_outlines("lip", count=1))

    assert lines[0].startswith("1. ")
    assert any(line.strip().startswith("Opening:") for line in lines)
    assert any(line.strip().startswith("Proof:") for line in lines)
