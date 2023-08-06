from collections import defaultdict
from enum import Enum
from typing import Dict, Type, Optional, TypeVar, Generic, List, Set

Event = TypeVar("Event", bound=Enum)

State = TypeVar("State", bound=Enum)

A = TypeVar("A", bound="Automation")


class Transition(Generic[A]):
    """ Task called when moving from one state to another."""

    def __call__(self, automation: A) -> Event:
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__


class Noop(Transition):
    """ Transition without any action."""

    def __call__(self, automation):
        pass


class ConditionMeta(type):
    def __rmatmul__(cls, other: State) -> "Condition":
        """ Binds condition to source state."""
        return cls(other)


class Condition(Generic[A], metaclass=ConditionMeta):
    """ Condition for state transition."""
    def __init__(self, state: State):
        self.src: State = state
        self.dst: Optional[State] = None
        self.transitions: List[Transition] = []

    def true(self, automation: A, event: Event) -> bool:
        """ returns True if event satisfies condition in current state."""
        raise NotImplementedError()

    def __or__(self, other: Type[Transition]) -> "Condition":
        """ Links current condition to transition."""
        self.transitions.append(other())
        return self

    def __gt__(self, other: State) -> "Condition":
        """ Sets destination state for current condition."""
        self.dst = other
        return self

    def __str__(self):
        t = ' | '.join(map(str, self.transitions))
        return f'{self.src} @ {self.__class__.__name__} | {t} > {self.dst}'


class OK(Condition):
    """ Condition that is always satisfied."""

    def true(self, automation, event: Event) -> bool:
        return True


class Automation:
    """ Automation in state."""

    def __init__(self, state: Optional[State] = None, **kwargs):
        self.state = state
        """ Initial automation state."""
        self.transitions: Dict[State, Set[Condition]] = defaultdict(set)
        """ Automation transition table."""

    @property
    def finished(self) -> bool:
        return self.state == self.state.Finish

    def run_transition(self, transition: Transition) -> Event:
        return transition(self)

    def next_condition(self, event: Event) -> Condition:
        """ Chooses condition satisfied by event in current state."""
        satisfied_conditions = set()
        conditions = self.transitions[self.state]
        for condition in conditions:
            if condition.true(self, event):
                satisfied_conditions.add(condition)
        if len(satisfied_conditions) == 0:
            raise RuntimeError("No satisfied conditions")
        if len(satisfied_conditions) > 1:
            raise RuntimeError("Multiple satisfied conditions")
        return satisfied_conditions.pop()

    def states(self: A, *conditions: Condition[A]):
        """ Initializes transition table."""
        for condition in conditions:
            state_conditions = self.transitions[condition.src]
            if condition in state_conditions:
                raise ValueError("Duplicate condition for state",
                                 condition, condition.src)
            state_conditions.add(condition)
