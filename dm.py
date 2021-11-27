import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

from cocktail_predict import cocktail_description


class State(Enum):
    START = 1
    ASKING = 2


class Action(Enum):
    SAY_HELLO = 1
    SAY_GOODBYE = 2
    START_ASKING = 3
    ASK = 4
    END_ASKING = 5
    UNKNOWN = 6


@dataclass
class ActionWithIngredient:
    action: Action
    ingredient: str = ''


def _random_error_message() -> str:
    return random.choice(['What you talkin?'])


def _random_aga_phrase() -> str:
    return random.choice(['Aga', 'Heard ya', 'Go on'])


def apply_action(state: State, action_with_ingredient: ActionWithIngredient, ingredients: List[str]) -> Tuple[str, State]:
    action = action_with_ingredient.action
    if state == State.START:
        if action == Action.SAY_HELLO:
            return 'G’day mate and welcome to my absolute beauty of a bar!', State.START
        if action == Action.SAY_GOODBYE:
            return 'Bye mate, no worries', State.START
        if action == Action.START_ASKING:
            return 'I ll tell ya all about them cocktails, gimme your ingredients', State.ASKING
    if state == State.ASKING:
        if action == Action.SAY_GOODBYE:
            return 'Oh, I guess you\'re not so interested.....', State.START
        if action == Action.ASK:
            ingredients.append(action_with_ingredient.ingredient)
            return _random_aga_phrase(), State.ASKING
        if action == Action.END_ASKING:
            ingredients_names = ", ".join(ingredients)
            cocktail = cocktail_description(ingredients)
            del ingredients[:]
            return f'Tough one.... Maybe for "{ingredients_names}" the best one is:\n{cocktail}', State.START

    return _random_error_message(), state
