from typing import List

from dm import ActionWithIngredient, Action


def _check_smth_in_str(strings: List[str], s: str) -> bool:
    return any([substr in s for substr in strings])


def _most_probable_action(message: str) -> Action:
    message = message.lower()
    if _check_smth_in_str(['hi', 'hello', 'good day', 'good morning', 'good evening'], message):
        return Action.SAY_HELLO
    if _check_smth_in_str(['bye', 'goodbye', 'good night', 'see you', 'see ya'], message):
        return Action.SAY_GOODBYE
    if _check_smth_in_str(['ingredients', 'ingredient', 'drink',
                           'drinks', 'stuff', 'bottles', 'ask', 'only',
                           'tell', 'say', 'suggest', 'cocktail', 'cocktails'], message):
        return Action.START_ASKING
    if _check_smth_in_str(['all', 'finish', 'end', 'everything', 'nothing'], message):
        return Action.END_ASKING
    return Action.ASK


def _parse_ingredient(message: str) -> str:
    return message.split(' ')[0]


def parse_action(message: str) -> ActionWithIngredient:
    probable_action = _most_probable_action(message)
    if probable_action == Action.ASK:
        ingredient = _parse_ingredient(message)
        if not ingredient:
            return ActionWithIngredient(Action.UNKNOWN)
        return ActionWithIngredient(probable_action, ingredient)
    return ActionWithIngredient(probable_action)
