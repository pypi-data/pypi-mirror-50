from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Type, Optional, TypeVar, Generic, List, Set, Any

E = TypeVar("E", bound=Enum)

S = TypeVar("S", bound=Enum)

A = TypeVar("A", bound="Automation")


@dataclass
class Input(Generic[E]):
    event: E
    payload: Any = None


class Transition(Generic[A, E]):
    """ Task called when moving from one state to another."""

    def __call__(self, automation: A, event: Input[E]) -> Input[E]:
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__


class Noop(Transition):
    """ Transition without any action."""

    def __call__(self, automation, event):
        pass


class ConditionMeta(type):
    def __rmatmul__(cls, state: S) -> "Condition":
        """ Binds condition to source state."""
        return cls(state)


class Condition(Generic[A, E], metaclass=ConditionMeta):
    """ Condition for state transition."""
    def __init__(self, state: S):
        self.src: S = state
        self.dst: Optional[S] = None
        self.transitions: List[Transition[A, E]] = []

    def true(self, automation: A, event: Input[E]) -> bool:
        """ returns True if event satisfies condition in current state."""
        raise NotImplementedError()

    def __or__(self, other: Type[Transition[A, E]]) -> "Condition[A, E]":
        """ Links current condition to transition."""
        self.transitions.append(other())
        return self

    def __gt__(self, state: S) -> "Condition[A, E]":
        """ Sets destination state for current condition."""
        self.dst = state
        return self

    def __str__(self):
        t = ' | '.join(map(str, self.transitions))
        return f'{self.src} @ {self.__class__.__name__} | {t} > {self.dst}'

    def __repr__(self):
        return str(self)


class OK(Condition):
    """ Condition that is always satisfied."""

    def true(self, automation, event) -> bool:
        return True


class Automation(Generic[E]):
    """ Automation in state."""

    def __init__(self: A, state: Optional[S] = None, **kwargs):
        self.state = state
        """ Initial automation state."""
        self.transitions: Dict[S, Set[Condition[A, E]]] = defaultdict(set)
        """ Automation transition table."""

    @property
    def finished(self) -> bool:
        return self.state == self.state.Finish

    def run_transition(self, transition: Transition[A, E],
                       event: Input[E]) -> Input[E]:
        return transition(self, event)

    def next_condition(self: A, event: Input[E]) -> Condition[A, E]:
        """ Chooses condition satisfied by event in current state."""
        satisfied_conditions = set()
        conditions = self.transitions[self.state]
        for condition in conditions:
            if condition.true(self, event.event):
                satisfied_conditions.add(condition)
        if len(satisfied_conditions) == 0:
            raise RuntimeError("No satisfied conditions",
                               self.state, event, conditions)
        if len(satisfied_conditions) > 1:
            raise RuntimeError("Multiple satisfied conditions",
                               self.state, event, satisfied_conditions)
        return satisfied_conditions.pop()

    def states(self: A, *conditions: Condition):
        """ Initializes transition table."""
        for condition in conditions:
            state_conditions = self.transitions[condition.src]
            if condition in state_conditions:
                raise ValueError("Duplicate condition for state",
                                 condition, condition.src)
            state_conditions.add(condition)
