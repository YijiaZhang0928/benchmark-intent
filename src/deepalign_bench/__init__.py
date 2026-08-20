"""Public API for DeepAlign-Bench interaction environments."""

from .backends import JSONLLMSimulatorBackend, RuleBasedSimulatorBackend, SimulatorBackend
from .environment import InteractionEnvironment
from .io import case_from_dict, load_case, write_trace
from .models import (
    AttributeImportanceGraph,
    AttributeMatch,
    Classification,
    DisclosureLevel,
    EnvironmentMode,
    HiddenPersonaState,
    ImportanceEdge,
    InteractionCase,
    PersonaAttribute,
    RevealPolicy,
    RevealRule,
    RevealStrategy,
    StepResult,
    Task,
)
from .policy import DisclosureState, GraphRevealPolicy, RevealPolicyEngine
from .runner import AgentAction, AgentContext, EpisodeResult, run_episode

__all__ = [
    "AgentAction",
    "AgentContext",
    "AttributeImportanceGraph",
    "AttributeMatch",
    "Classification",
    "DisclosureLevel",
    "DisclosureState",
    "EnvironmentMode",
    "EpisodeResult",
    "GraphRevealPolicy",
    "HiddenPersonaState",
    "ImportanceEdge",
    "InteractionCase",
    "InteractionEnvironment",
    "JSONLLMSimulatorBackend",
    "PersonaAttribute",
    "RevealPolicy",
    "RevealPolicyEngine",
    "RevealRule",
    "RevealStrategy",
    "RuleBasedSimulatorBackend",
    "SimulatorBackend",
    "StepResult",
    "Task",
    "case_from_dict",
    "load_case",
    "run_episode",
    "write_trace",
]

__version__ = "0.58.0"
