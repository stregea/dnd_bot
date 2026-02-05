"""
Attack command cog for DnD Roller bot.

This module provides Discord commands for rolling attacks with multiple
creatures, handling advantage/disadvantage, critical hits, and damage calculation.
"""

from typing import Any

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from lib.roll import roll_attack, roll_damage, calculate_crit_damage, AttackType
from lib.settings import (
    CREATURES,
    STANDARD_ATTACK_COMMAND,
    ADVANTAGE_ATTACK_COMMAND,
    DISADVANTAGE_ATTACK_COMMAND,
)

# Type aliases for creature data structures
CreatureDict = dict[str, Any]
ActionDict = dict[str, Any]

# Maximum number of attack results to display in embed (prevents message overflow)
DISPLAY_LIMIT: int = 10

# Critical roll values for d20
CRITICAL_HIT_ROLL: int = 20
CRITICAL_MISS_ROLL: int = 1

# Valid attack type commands
VALID_ATTACK_TYPES: set[str] = {
    STANDARD_ATTACK_COMMAND,
    ADVANTAGE_ATTACK_COMMAND,
    DISADVANTAGE_ATTACK_COMMAND,
}


class AttackCog(commands.Cog):
    """
    A Discord cog for handling DnD attack rolls.

    This cog provides commands for rolling attacks with predefined creatures,
    supporting multiple attackers, different attack types (standard, advantage,
    disadvantage), and automatic damage calculation including critical hits.

    Attributes:
        bot: The Discord bot instance this cog is attached to.
    """

    def __init__(self, bot: Bot) -> None:
        """
        Initialize the AttackCog.

        Args:
            bot: The Discord bot instance to attach this cog to.
        """
        self.bot: Bot = bot

    @commands.command(
        name="attack",
        help="Roll attacks for multiple creatures against a target AC.\n"
             "Usage: !attack <creature> <count> <target_ac> [attack_type] [action]"
    )
    async def attack(
        self,
        ctx: Context,
        creature_name: str,
        num_creatures: int,
        target_ac: int,
        attack_type: AttackType = "standard",
        action_name: str | None = None,
    ) -> None:
        """
        Roll attacks for multiple creatures against a target.

        Handles attack rolls for a specified number of creatures, checking
        against the target's armor class and calculating damage for hits.
        Supports standard rolls, advantage, and disadvantage.

        Args:
            ctx: The Discord command context.
            creature_name: Name of the creature (must exist in creatures.json).
            num_creatures: Number of creatures making attacks.
            target_ac: Target's armor class to beat.
            attack_type: Roll type - 'standard', 'advantage', or 'disadvantage'.
            action_name: Optional specific action; uses creature's default if omitted.

        Examples:
            !attack Wolf 3 15 advantage
            !attack "Brown Bear" 2 16 standard Claws
        """
        # Reference the creatures dictionary from settings
        creatures: CreatureDict = CREATURES

        # Validate creature exists in configuration (commented out for flexibility)
        # if creature_name not in creatures:
        #     await ctx.send(f"❌ Creature '{creature_name}' not found. Use !creatures to see available creatures.")
        #     return

        # Validate attack type is one of the allowed values
        if attack_type not in VALID_ATTACK_TYPES:
            await ctx.send(
                f"❌ Attack type must be: {STANDARD_ATTACK_COMMAND}, "
                f"{ADVANTAGE_ATTACK_COMMAND}, or {DISADVANTAGE_ATTACK_COMMAND}."
            )
            return

        # Look up creature data (case-insensitive)
        creature: CreatureDict = creatures[creature_name.lower()]

        # Determine which action to use for the attack
        if action_name:
            # Validate specified action exists for this creature
            if action_name not in creature["actions"]:
                available_actions: str = ", ".join(creature["actions"].keys())
                await ctx.send(
                    f"❌ Action '{action_name}' not found for {creature_name}. "
                    f"Available: {available_actions}."
                )
                return
            action: ActionDict = creature["actions"][action_name]
            action_display: str = action_name
        else:
            # Use creature's default action if none specified
            action_name = creature["default_action"]
            action = creature["actions"][action_name]
            action_display = action_name

        # Initialize tracking variables for results
        results: list[dict[str, Any]] = []
        total_damage: int = 0
        hits: int = 0

        # Roll attacks for each creature
        for i in range(num_creatures):
            # Roll the attack using the action's attack bonus
            nat_roll, attack_total, dice = roll_attack(
                action["attack_bonus"], attack_type
            )

            # Build result dictionary for this attack
            result: dict[str, Any] = {
                "num": i + 1,
                "nat_roll": nat_roll,
                "dice": dice,
                "total": attack_total,
                "hit": False,
                "crit": False,
                "crit_fail": False,
                "damage": 0,
                "breakdown": "",
            }

            # Determine attack outcome
            if nat_roll == CRITICAL_MISS_ROLL:
                # Natural 1: Critical failure (auto-miss)
                result["crit_fail"] = True
            elif nat_roll == CRITICAL_HIT_ROLL:
                # Natural 20: Critical hit (auto-hit with bonus damage)
                result["crit"] = True
                result["hit"] = True
                hits += 1

                # Calculate critical damage (max + extra roll)
                dmg, breakdown = calculate_crit_damage(
                    action["damage"]["count"],
                    action["damage"]["sides"],
                    action["damage"]["bonus"],
                )
                result["damage"] = dmg
                result["breakdown"] = breakdown
                total_damage += dmg
            elif attack_total >= target_ac:
                # Normal hit: attack total meets or exceeds AC
                result["hit"] = True
                hits += 1

                # Roll normal damage
                dmg, rolls = roll_damage(
                    action["damage"]["count"],
                    action["damage"]["sides"],
                    action["damage"]["bonus"],
                )
                result["damage"] = dmg

                # Format damage breakdown string
                rolls_str: str = "+".join(map(str, rolls))
                bonus: int = action["damage"]["bonus"]
                bonus_str: str = f"+{bonus}" if bonus > 0 else ""
                result["breakdown"] = f"{rolls_str}{bonus_str}"
                total_damage += dmg

            results.append(result)

        # Build Discord embed for displaying results
        embed: discord.Embed = discord.Embed(
            title=f"⚔️ {num_creatures}x {creature_name} Attack Rolls",
            description=(
                f"**Action:** {action_display} | "
                f"**Target AC:** {target_ac} | "
                f"**Attack Type:** {attack_type.title()}"
            ),
            color=discord.Color.purple(),
        )

        # Add individual attack results (limited to prevent message overflow)
        for r in results[:DISPLAY_LIMIT]:
            # Determine status indicator based on roll outcome
            if r["crit"]:
                status: str = "🎯 **CRITICAL HIT!**"
                color: str = "🟡"
            elif r["crit_fail"]:
                status = "💥 **CRITICAL FAIL!**"
                color = "🔴"
            elif r["hit"]:
                status = "✅ Hit"
                color = "🟢"
            else:
                status = "❌ Miss"
                color = "⚪"

            # Format dice display (show both dice for advantage/disadvantage)
            if len(r["dice"]) > 1:
                dice_str: str = f"[{', '.join(map(str, r['dice']))}]"
            else:
                dice_str = str(r["nat_roll"])

            # Build attack roll display string
            attack_str: str = (
                f"{dice_str} + {action['attack_bonus']} = **{r['total']}**"
            )

            # Add damage info if the attack hit
            damage_str: str = ""
            if r["hit"]:
                damage_str = f"\n💥 Damage: **{r['damage']}** ({r['breakdown']})"

            # Add field for this attack result
            embed.add_field(
                name=f"{color} {creature_name} #{r['num']} - {status}",
                value=f"🎲 {attack_str}{damage_str}",
                inline=False,
            )

        # Show truncation warning if there are more results than displayed
        if len(results) > DISPLAY_LIMIT:
            embed.add_field(
                name="⚠️ Results Truncated",
                value=(
                    f"Showing {DISPLAY_LIMIT} of {len(results)} attacks. "
                    "See summary below."
                ),
                inline=False,
            )

        # Add summary statistics
        embed.add_field(
            name="📊 Summary",
            value=(
                f"**Hits:** {hits}/{num_creatures}\n"
                f"**Total Damage:** {total_damage}"
            ),
            inline=False,
        )

        # Send the embed to the Discord channel
        await ctx.send(embed=embed)

async def setup(bot: Bot) -> None:
    """
    Set up the AttackCog extension for the Discord bot.

    This function is called by discord.py when the cog is loaded via
    bot.load_extension(). It registers the AttackCog with the bot.

    Args:
        bot: The Discord bot instance to add the cog to.
    """
    await bot.add_cog(AttackCog(bot))