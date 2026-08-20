"""Adapters for running arbitrary callable agents against an environment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping, Protocol

from .environment import InteractionEnvironment
from .models import ConversationTurn, EnvironmentMode, ResetObservation


@dataclass(frozen=True)
class AgentAction:
    message: str
    final: bool = False


@dataclass(frozen=True)
class AgentContext:
    case_id: str
    mode: EnvironmentMode
    task_prompt: str
    deliverable: str
    visible_persona: Mapping[str, Any] | None
    history: tuple[ConversationTurn, ...]
    remaining_turns: int


class Agent(Protocol):
    def act(self, context: AgentContext) -> AgentAction | str | Mapping[str, Any]: ...


AgentCallable = Callable[[AgentContext], AgentAction | str | Mapping[str, Any]]


@dataclass(frozen=True)
class EpisodeResult:
    reset_observation: ResetObservation
    final_artifact: str | None
    trace: Mapping[str, Any]
    truncated: bool


def _normalize_action(raw: AgentAction | str | Mapping[str, Any]) -> AgentAction:
    if isinstance(raw, AgentAction):
        return raw
    if isinstance(raw, str):
        return AgentAction(message=raw, final=False)
    if isinstance(raw, Mapping):
        message = raw.get("message", raw.get("content", ""))
        return AgentAction(message=str(message), final=bool(raw.get("final", False)))
    raise TypeError("agent action must be AgentAction, str, or mapping")


def run_episode(
    agent: Agent | AgentCallable,
    environment: InteractionEnvironment,
    *,
    seed: int | None = None,
) -> EpisodeResult:
    """Run an agent object with ``act`` or any callable accepting AgentContext."""

    observation = environment.reset(seed=seed)
    truncated = False
    while True:
        context = AgentContext(
            case_id=observation.case_id,
            mode=observation.mode,
            task_prompt=observation.task.prompt,
            deliverable=observation.task.deliverable,
            visible_persona=observation.persona,
            history=environment.conversation,
            remaining_turns=max(0, observation.max_turns - len(environment.conversation)),
        )
        raw = agent.act(context) if hasattr(agent, "act") else agent(context)  # type: ignore[misc]
        action = _normalize_action(raw)
        step = environment.step(action.message, final=action.final)
        if step.done:
            truncated = step.truncated
            break
    return EpisodeResult(
        reset_observation=observation,
        final_artifact=environment.final_artifact,
        trace=environment.export_trace(),
        truncated=truncated,
    )
