from random import randint


def can_talk() -> bool:
    """
    Used to limit bot interaction.
    """
    can_talk = roll_dices()
    if can_talk > 10:
        return False
    return True


def roll_dices() -> int:
    dice1 = randint(1, 6)
    dice2 = randint(1, 6)
    dice3 = randint(1, 6)
    return dice1 + dice2 + dice3
