from pathlib import Path

from router import load_calibrator, score_candidate, select_questions, validated_evidence, CanonicalCandidate


ROOT = Path(__file__).resolve().parent


def candidate(**overrides):
    row = {
        "candidate_id": "C01",
        "source_proposal_ids": ["D01", "F01"],
        "decision_slot": "strategy",
        "overlap_group": "strategy",
        "axis": "speed versus durability",
        "candidate_kind": "preference",
        "ownership": "user_owned",
        "answer_form": "ordinal_tradeoff",
        "importance": 5,
        "wrong_default_cost": 5,
        "residuality_after_research": 5,
        "counterfactual_strength": 5,
        "burden": 1,
        "evidence_relation": "inferred",
        "visible_evidence_quote": "launch quickly",
        "neutral_question": "Which trade-off matters most?",
        "verification_question": "I infer speed matters most; should I optimize for it?",
        "rationale": "Changes the plan.",
        "multi_lens_support": 2,
    }
    row.update(overrides)
    return row


def enrich(row, task="Please launch quickly."):
    evidence = validated_evidence(CanonicalCandidate.model_validate(row), task)
    row = dict(row)
    row["validated_evidence"] = {
        "relation": evidence.relation,
        "quote_valid": evidence.quote_valid,
        "strength": evidence.strength,
        "directness": evidence.directness,
    }
    return row


def test_invalid_quote_cannot_be_direct_evidence():
    row = candidate(evidence_relation="explicit", visible_evidence_quote="not present")
    evidence = validated_evidence(CanonicalCandidate.model_validate(row), "visible text")
    assert evidence.relation == "absent"
    assert evidence.directness == 0


def test_v4r_critical_inferred_value_receives_override():
    calibrator = load_calibrator(ROOT / "calibrator_v0.json")
    scored = score_candidate(enrich(candidate()), calibrator, "v4r")
    assert scored["critical_override"] is True
    assert scored["utility"] > scored["utility_raw"]


def test_direct_explicit_value_is_not_selected():
    calibrator = load_calibrator(ROOT / "calibrator_v0.json")
    row = candidate(evidence_relation="explicit", visible_evidence_quote="launch quickly")
    pool = {"canonical_candidates": [enrich(row)]}
    result = select_questions(pool, calibrator, "v4r")
    assert result["selected"] == []


def test_research_fact_is_never_selected_even_if_important():
    calibrator = load_calibrator(ROOT / "calibrator_v0.json")
    row = candidate(candidate_kind="research_fact", ownership="research_owned")
    pool = {"canonical_candidates": [enrich(row)]}
    result = select_questions(pool, calibrator, "v4r")
    assert result["selected"] == []


def test_diversity_and_question_cap_are_deterministic():
    calibrator = load_calibrator(ROOT / "calibrator_v0.json")
    rows = []
    for index in range(7):
        row = candidate(
            candidate_id=f"C{index:02d}",
            source_proposal_ids=[f"D{index:02d}"],
            overlap_group="same" if index < 2 else f"g{index}",
            decision_slot=f"slot{index}",
            axis=f"axis{index}",
        )
        rows.append(enrich(row))
    result = select_questions({"canonical_candidates": rows}, calibrator, "v4r")
    assert len(result["selected"]) == 4
    assert len({item["overlap_group"] for item in result["selected"]}) == 4
