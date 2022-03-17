from app_core.models.base import TimeStampedBase
from django.db import models


class Pokemon(TimeStampedBase):
    """
    A 'Pokémon' is a fictional creature - we are just storing records of them here.
    """

    api_lookup_number = models.PositiveSmallIntegerField(
        help_text="The lookup number we can use to query the API"
    )

    name = models.CharField(
        help_text="The pokemons name",
        max_length=255,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["api_lookup_number"]


class Stats(TimeStampedBase):
    """
    Stats are numerical indicators of a Pokémon's ability, split into sections.
    """

    related_pokemon = models.ForeignKey(
        "Pokemon",
        related_name="stats",
        on_delete=models.CASCADE,
        help_text="The pokemon that these statistics represent"
    )

    hp = models.PositiveSmallIntegerField(
        help_text="Hit Points"
    )

    attack = models.PositiveSmallIntegerField(
        help_text="Attack Power"
    )

    defense = models.PositiveSmallIntegerField(
        help_text="Defense Power"
    )

    special_attack = models.PositiveSmallIntegerField(
        help_text="Special Attack Power"
    )

    special_defense = models.PositiveSmallIntegerField(
        help_text="Special Defense Power"
    )

    def __str__(self) -> str:
        return f"{self.related_pokemon.name}' Stats"

    class Meta:
        ordering = ["related_pokemon__name"]


class Move(TimeStampedBase):
    """
    Moves are attacks that can be performed by a Pokémon.
    """

    api_lookup_number = models.PositiveSmallIntegerField(
        help_text="The lookup number we can use to query the API"
    )

    name = models.CharField(
        help_text="The name of the move",
        max_length=255,
        unique=True,
    )

    power = models.PositiveSmallIntegerField(
        help_text="The amount of damage it does"
    )

    type = models.ForeignKey(
        "MoveType",
        related_name="moves",
        on_delete=models.CASCADE,
        help_text="The type of attack"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["related_pokemon__name"]


class MoveType(TimeStampedBase):
    """
    MoveTypes are categories for the different moves
    """

    api_lookup_number = models.PositiveSmallIntegerField(
        help_text="The lookup number we can use to query the API",
        unique=True,
    )

    name = models.CharField(
        help_text="Name of the move type",
        unique=True,
        max_length=255,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name", ]
