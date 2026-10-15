"""Small CTL checker for the liveness formula used by the project model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Set


@dataclass(frozen=True)
class CTLCheck:
    """Result of evaluating AG(antecedent -> AF(consequent))."""

    holds: bool
    satisfying_states: frozenset[str]
    violating_states: frozenset[str]


def check_ag_implies_af(
    initial: Set[str],
    transitions: Mapping[str, Set[str]],
    labels: Mapping[str, Set[str]],
    antecedent: str,
    consequent: str,
) -> CTLCheck:
    """Evaluate AG(antecedent -> AF(consequent)) from the initial states."""
    states = set(transitions)
    if set(initial) - states:
        raise ValueError("initial state is not declared")
    if any(not successors or set(successors) - states for successors in transitions.values()):
        raise ValueError("transition relation must be total and declared")

    eventually_consequent = {
        state for state in states if consequent in labels.get(state, set())
    }
    changed = True
    while changed:
        changed = False
        for state, successors in transitions.items():
            if state not in eventually_consequent and successors <= eventually_consequent:
                eventually_consequent.add(state)
                changed = True

    reachable = set(initial)
    frontier = list(initial)
    while frontier:
        state = frontier.pop()
        for successor in transitions[state]:
            if successor not in reachable:
                reachable.add(successor)
                frontier.append(successor)

    violating = {
        state
        for state in reachable
        if antecedent in labels.get(state, set()) and state not in eventually_consequent
    }
    return CTLCheck(
        holds=not violating,
        satisfying_states=frozenset(reachable - violating),
        violating_states=frozenset(violating),
    )
