from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from deepalign_bench import (
    AgentAction,
    AttributeImportanceGraph,
    Classification,
    DisclosureLevel,
    EnvironmentMode,
    HiddenPersonaState,
    ImportanceEdge,
    InteractionCase,
    InteractionEnvironment,
    JSONLLMSimulatorBackend,
    PersonaAttribute,
    RevealPolicy,
    RevealRule,
    RevealStrategy,
    RuleBasedSimulatorBackend,
    Task,
    load_case,
    run_episode,
)
from deepalign_bench.backends import ClassificationRequest, ResponseRequest
from deepalign_bench.models import AttributeMatch, GeneratedResponse


ROOT = Path(__file__).resolve().parents[1]
DEMO_CASE = ROOT / "src" / "deepalign_bench" / "data" / "demo_case.json"


class RecordingBackend(RuleBasedSimulatorBackend):
    def __init__(self) -> None:
        self.classification_requests: list[ClassificationRequest] = []
        self.response_requests: list[ResponseRequest] = []

    def classify(self, request: ClassificationRequest) -> Classification:
        self.classification_requests.append(request)
        return super().classify(request)

    def respond(self, request: ResponseRequest) -> GeneratedResponse:
        self.response_requests.append(request)
        return super().respond(request)


class LeakingBackend(RuleBasedSimulatorBackend):
    def respond(self, request: ResponseRequest) -> GeneratedResponse:
        return GeneratedResponse("The employer is Northstar Biologics.", ())


class InteractionEnvironmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.case = load_case(DEMO_CASE)

    def test_oracle_exposes_complete_persona_at_reset(self) -> None:
        env = InteractionEnvironment(self.case, EnvironmentMode.ORACLE)
        observation = env.reset(seed=1)
        self.assertIsNotNone(observation.persona)
        self.assertEqual(
            set(observation.initially_revealed_attribute_ids),
            set(self.case.persona.attribute_ids),
        )
        self.assertEqual(set(env.revealed_attribute_ids), set(self.case.persona.attribute_ids))

    def test_interactive_exposes_only_configured_initial_values_and_naive_stays_task_only(self) -> None:
        case = InteractionCase(
            "initial-visible-case",
            self.case.task,
            self.case.persona,
            importance_graph=self.case.importance_graph,
            reveal_policy=self.case.reveal_policy,
            initially_revealed=("budget",),
        )
        observation = InteractionEnvironment(case, EnvironmentMode.INTERACTIVE).reset(seed=1)
        self.assertIsNotNone(observation.persona)
        attributes = observation.persona["attributes"]  # type: ignore[index]
        self.assertEqual([attribute["attribute_id"] for attribute in attributes], ["budget"])
        self.assertNotIn("Northstar Biologics", json.dumps(observation.persona))
        naive_observation = InteractionEnvironment(case, EnvironmentMode.NAIVE).reset(seed=1)
        self.assertIsNone(naive_observation.persona)
        self.assertEqual(naive_observation.initially_revealed_attribute_ids, ())

    def test_naive_bypasses_never_reveal_rule(self) -> None:
        env = InteractionEnvironment(self.case, EnvironmentMode.NAIVE)
        env.reset(seed=1)
        result = env.step("Could you share your employer name?")
        self.assertIn("Northstar Biologics", result.response or "")
        self.assertEqual(result.event.newly_revealed_attribute_ids, ("employer_name",))
        self.assertEqual(result.event.policy_decisions[0].reason, "naive_policy_bypass")

    def test_interactive_enforces_selective_disclosure_and_logs_hidden(self) -> None:
        env = InteractionEnvironment(self.case, EnvironmentMode.INTERACTIVE)
        env.reset(seed=1)
        result = env.step("Could you share your employer name?")
        self.assertNotIn("Northstar Biologics", result.response or "")
        self.assertEqual(result.event.matched_attribute_ids, ("employer_name",))
        self.assertEqual(result.event.matched_unrevealed_attribute_ids, ("employer_name",))
        self.assertEqual(result.event.newly_revealed_attribute_ids, ())
        self.assertIn("employer_name", result.event.still_hidden_attribute_ids)
        self.assertEqual(result.event.policy_decisions[0].reason, "attribute_never_disclose")

    def test_interactive_only_passes_approved_values_to_response_backend(self) -> None:
        backend = RecordingBackend()
        env = InteractionEnvironment(self.case, EnvironmentMode.INTERACTIVE, backend=backend)
        env.reset(seed=1)
        env.step("What budget can you spend?")
        descriptors = backend.classification_requests[0].attribute_descriptors
        self.assertFalse(any(hasattr(descriptor, "value") for descriptor in descriptors))
        visible = backend.response_requests[0].visible_attributes
        self.assertEqual(tuple(attribute.attribute_id for attribute in visible), ("budget",))
        self.assertFalse(any(attribute.attribute_id == "employer_name" for attribute in visible))

    def test_backend_literal_leak_fails_closed(self) -> None:
        env = InteractionEnvironment(
            self.case,
            EnvironmentMode.INTERACTIVE,
            backend=LeakingBackend(),
        )
        env.reset(seed=1)
        result = env.step("Could you share your employer name?")
        self.assertEqual(result.response, "I would rather not share that information right now.")
        self.assertEqual(result.event.backend_blocked_attribute_ids, ("employer_name",))
        self.assertEqual(result.event.newly_revealed_attribute_ids, ())

    def test_structured_llm_backend_never_receives_denied_value_in_interactive_mode(self) -> None:
        calls: list[str] = []

        def completion(messages) -> str:
            payload = messages[-1]["content"]
            calls.append(payload)
            if "attribute_descriptors_without_values" in payload:
                return json.dumps(
                    {
                        "is_question": True,
                        "matches": [
                            {
                                "attribute_id": "budget",
                                "confidence": 0.99,
                                "evidence": "budget",
                            }
                        ],
                        "rationale": "direct question",
                    }
                )
            return json.dumps(
                {
                    "response": "We can spend up to USD 1,200 per year.",
                    "disclosed_attribute_ids": ["budget"],
                }
            )

        env = InteractionEnvironment(
            self.case,
            EnvironmentMode.INTERACTIVE,
            backend=JSONLLMSimulatorBackend(completion),
        )
        env.reset(seed=1)
        result = env.step("What budget can you spend?")
        self.assertIn("USD 1,200", result.response or "")
        self.assertEqual(len(calls), 2)
        self.assertNotIn("Northstar Biologics", calls[0])
        self.assertNotIn("Northstar Biologics", calls[1])
        self.assertNotIn("USD 1,200", calls[0])
        self.assertIn("USD 1,200", calls[1])

    def test_unmatched_question_does_not_reveal_anything(self) -> None:
        env = InteractionEnvironment(self.case, EnvironmentMode.INTERACTIVE)
        env.reset(seed=1)
        result = env.step("Which databases should you search?")
        self.assertTrue(result.event.classification.is_question)
        self.assertEqual(result.event.matched_attribute_ids, ())
        self.assertEqual(result.event.newly_revealed_attribute_ids, ())
        self.assertEqual(
            set(result.event.still_hidden_attribute_ids), set(self.case.persona.attribute_ids)
        )

    def test_graph_ranks_direct_matches_without_expanding_to_unmatched_nodes(self) -> None:
        persona = HiddenPersonaState(
            "p",
            (
                PersonaAttribute(
                    "a",
                    "alpha",
                    "A-value",
                    keywords=("alpha",),
                    importance=0.4,
                    disclosure_level=DisclosureLevel.PUBLIC,
                ),
                PersonaAttribute(
                    "b",
                    "beta",
                    "B-value",
                    keywords=("beta",),
                    importance=0.3,
                    disclosure_level=DisclosureLevel.PUBLIC,
                ),
                PersonaAttribute(
                    "c",
                    "gamma",
                    "C-value",
                    keywords=("gamma",),
                    importance=1.0,
                    disclosure_level=DisclosureLevel.PUBLIC,
                ),
            ),
        )
        case = InteractionCase(
            "graph-case",
            Task("t", "Do research."),
            persona,
            importance_graph=AttributeImportanceGraph((ImportanceEdge("a", "b", 1.0),)),
            reveal_policy=RevealPolicy(max_attributes_per_turn=1),
        )
        env = InteractionEnvironment(case)
        env.reset(seed=2)
        result = env.step("What are your alpha and beta preferences?")
        self.assertEqual(result.event.newly_revealed_attribute_ids, ("b",))
        self.assertIn("a", result.event.matched_unrevealed_attribute_ids)
        self.assertIn("c", result.event.still_hidden_attribute_ids)
        self.assertNotIn("c", result.event.matched_attribute_ids)

    def test_probabilistic_rule_is_seed_reproducible(self) -> None:
        attribute = PersonaAttribute(
            "risk",
            "risk tolerance",
            "low",
            keywords=("risk",),
            disclosure_level=DisclosureLevel.CONDITIONAL,
        )
        case = InteractionCase(
            "probability-case",
            Task("t", "Research options."),
            HiddenPersonaState("p", (attribute,)),
            reveal_policy=RevealPolicy(
                rules={
                    "risk": RevealRule(
                        strategy=RevealStrategy.PROBABILISTIC,
                        probability=0.37,
                    )
                }
            ),
        )
        draws = []
        outcomes = []
        for _ in range(2):
            env = InteractionEnvironment(case)
            env.reset(seed=19)
            result = env.step("What is your risk tolerance?")
            draws.append(result.event.policy_decisions[0].random_draw)
            outcomes.append(result.event.policy_decisions[0].reveal)
        self.assertEqual(draws[0], draws[1])
        self.assertEqual(outcomes[0], outcomes[1])

    def test_final_submission_terminates_and_trace_omits_full_persona_by_default(self) -> None:
        env = InteractionEnvironment(self.case)
        env.reset(seed=1)
        result = env.step("Final memo", final=True)
        self.assertTrue(result.terminated)
        trace = env.export_trace()
        self.assertNotIn("hidden_persona", trace)
        self.assertIn("hidden_persona", env.export_trace(include_persona_values=True))
        with self.assertRaises(RuntimeError):
            env.step("another message")

    def test_runner_wraps_object_agent(self) -> None:
        class Agent:
            def act(self, context):
                if not context.history:
                    return {"message": "What budget can you spend?", "final": False}
                return AgentAction("Final answer", final=True)

        result = run_episode(Agent(), InteractionEnvironment(self.case), seed=4)
        self.assertEqual(result.final_artifact, "Final answer")
        self.assertFalse(result.truncated)
        self.assertEqual(len(result.trace["events"]), 2)

    def test_invalid_unknown_graph_node_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown attributes"):
            InteractionCase(
                "bad",
                self.case.task,
                self.case.persona,
                importance_graph=AttributeImportanceGraph(
                    (ImportanceEdge("budget", "not-real", 0.5),)
                ),
            )

    def test_descriptor_with_hidden_literal_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "value-free descriptor"):
            PersonaAttribute(
                "employer",
                "employer",
                "Secret Corp",
                description="The user works at Secret Corp",
                leak_markers=("Secret Corp",),
            )

    def test_trace_can_be_written_as_json(self) -> None:
        env = InteractionEnvironment(self.case)
        env.reset(seed=1)
        env.step("What budget can you spend?")
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "trace.json"
            from deepalign_bench import write_trace

            write_trace(env.export_trace(), path)
            self.assertEqual(json.loads(path.read_text())["mode"], "interactive")


if __name__ == "__main__":
    unittest.main()
