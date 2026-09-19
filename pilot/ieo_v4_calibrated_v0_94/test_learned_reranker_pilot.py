from learned_reranker_pilot import DEV, DOMAINS, TASKS, VALIDATION, evaluate_fold, load_data


def test_grouped_splits_and_training_labels():
    data = load_data()
    assert set(DEV).isdisjoint(VALIDATION)
    assert sum(len(data[task]["rows"]) for task in TASKS) == 111
    assert sum(sum(bool(units) for units in data[task]["candidate_units"].values()) for task in TASKS) == 20
    assert {task for tasks in DOMAINS.values() for task in tasks} == set(TASKS)


def test_fixed_split_respects_budget_and_reproduces_counts():
    fold = evaluate_fold(load_data(), DEV, VALIDATION)
    assert fold["training"] == {"candidates": 65, "positive_candidates": 12}
    assert [row["learned"]["covered_count"] for row in fold["results"]] == [0, 0]
    assert [row["heuristic"]["covered_count"] for row in fold["results"]] == [1, 1]
    for row in fold["results"]:
        assert row["learned"]["questions"] <= 4
        assert row["heuristic"]["questions"] <= 4
