"""
Dice rolling utilities for DnD combat mechanics.

This module provides functions for rolling dice, calculating attack rolls,
and determining damage for DnD 5e combat encounters.
"""

from random import randint
from typing import Literal

# Type alias for attack roll types (standard, advantage, or disadvantage)
type AttackType = Literal["standard", "advantage", "disadvantage"]

# Critical hit-and-miss thresholds for d20 rolls
CRITICAL_HIT: int = 20
CRITICAL_MISS: int = 1
D20_SIDES: int = 20


def roll_die(sides: int) -> int:
    """
    Roll a single die with the specified number of sides.

    Args:
        sides: The number of sides on the die (e.g., 20 for a d20).

    Returns:
        A random integer between 1 and sides (inclusive).

    Example:
        >>> roll = roll_die(20)  # Roll a d20
        >>> 1 <= roll <= 20
        True
    """
    return randint(1, sides)


def roll_damage(count: int, sides: int, bonus: int) -> tuple[int, list[int]]:
    """
    Roll damage dice and calculate the total.

    Simulates rolling multiple dice (e.g., 2d6+3) and returns both
    the total damage and the individual roll results.

    Args:
        count: The number of dice to roll (e.g., 2 for 2d6).
        sides: The number of sides on each die (e.g., 6 for 2d6).
        bonus: A flat bonus to add to the total damage (e.g., 3 for 2d6+3).

    Returns:
        A tuple containing:
            - The total damage (sum of all rolls + bonus).
            - A list of individual die roll results.

    Example:
        >>> total, rolls = roll_damage(2, 6, 3)  # Roll 2d6+3
        >>> len(rolls) == 2
        True
    """
    # Roll each die and collect results
    rolls: list[int] = [roll_die(sides) for _ in range(count)]

    # Calculate total: sum of rolls plus flat bonus
    return sum(rolls) + bonus, rolls


def roll_attack(
        attack_bonus: int,
        attack_type: AttackType
) -> tuple[int, int, list[int]]:
    """
    Roll an attack with the given bonus and attack type.

    Handles standard rolls, advantage (roll twice, take higher),
    and disadvantage (roll twice, take lower) as per DnD 5e rules.

    Args:
        attack_bonus: The modifier to add to the attack roll
                      (typically ability modifier + proficiency).
        attack_type: The type of roll - 'standard', 'advantage', or 'disadvantage'.

    Returns:
        A tuple containing:
            - The selected d20 roll (after applying advantage/disadvantage).
            - The total attack value (selected roll + bonus).
            - A list of all d20 rolls made (1 for standard, 2 for adv/disadv).

    Example:
        >>> nat_roll, total, dice = roll_attack(5, "advantage")
        >>> total == nat_roll + 5
        True
    """
    # Roll the first d20
    roll1: int = roll_die(D20_SIDES)

    # For standard attacks, return the single roll immediately
    if attack_type == "standard":
        return roll1, roll1 + attack_bonus, [roll1]

    # For advantage/disadvantage, roll a second d20
    roll2: int = roll_die(D20_SIDES)

    # Select the appropriate roll based on attack type
    if attack_type == "advantage":
        # Advantage: take the higher of the two rolls
        selected: int = max(roll1, roll2)
    else:
        # Disadvantage: take the lower of the two rolls
        selected = min(roll1, roll2)

    return selected, selected + attack_bonus, [roll1, roll2]


def calculate_crit_damage(count: int, sides: int, bonus: int) -> tuple[int, str]:
    """
    Calculate critical hit damage using max damage + extra rolled damage.

    Critical hits in DnD 5e deal maximum possible damage plus an additional
    roll of the damage dice. This function implements that calculation.

    Args:
        count: The number of damage dice (e.g., 2 for 2d6).
        sides: The number of sides on each die (e.g., 6 for 2d6).
        bonus: A flat bonus to add to the damage (e.g., 3 for 2d6+3).

    Returns:
        A tuple containing:
            - The total critical damage (max + extra roll).
            - A formatted string describing the damage breakdown.

    Example:
        >>> # For 2d6+3 crit: max is 12+3=15, plus another 2d6+3 roll
        >>> total, breakdown = calculate_crit_damage(2, 6, 3)
        >>> "max" in breakdown
        True
    """
    # Calculate maximum possible damage (all dice show max value)
    max_damage: int = count * sides + bonus

    # Roll extra damage dice for the critical hit
    extra_total, extra_rolls = roll_damage(count, sides, bonus)

    # Format the breakdown string for display
    rolls_str: str = "+".join(map(str, extra_rolls))
    bonus_str: str = f"+{bonus}" if bonus > 0 else ""

    # Return total and formatted breakdown
    return (
        max_damage + extra_total,
        f"{max_damage} (max) + {extra_total} ({rolls_str}{bonus_str})"
    )
