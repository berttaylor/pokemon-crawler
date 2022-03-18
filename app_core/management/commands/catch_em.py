import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from app_core.models import Move, MoveType, Pokemon, Stats


class Command(BaseCommand):
    """
    This Command gets all pokemon form the API, updating where needed.
    This is just a draft - really this should be run in a celery task, perhaps with the queryset split
    into different nights of the week.

    To improve - Can we try to get more info out of the 'list' api endpoint to avoid extra queries?
    """

    def add_arguments(self, parser):
        parser.add_argument("HOW_MANY")

    def success(self, text):
        self.stdout.write(self.style.SUCCESS(text))

    def error(self, text):
        self.stdout.write(self.style.ERROR(text))

    def handle(self, *args, **options):

        print("Starting Up...")
        print("Searching for updates")

        # Set our API parameters
        base_api_address = "https://pokeapi.co/api/v2/"
        type_query_string = "type"
        pokemon_query_string = "pokemon"

        # Set our counters
        moves_created = 0
        move_types_created = 0
        pokemon_created = 0

        with transaction.atomic():

            # 1) Get move-types
            print("Searching for move-types")
            move_types_endpoint_response = requests.get(
                base_api_address + type_query_string
            )
            types_list = move_types_endpoint_response.json()["results"]
            for move_type in types_list:
                move_type_object, created = MoveType.objects.get_or_create(
                    name=move_type["name"],
                )
                if created:
                    move_types_created += 1

                # 2) Get moves (we look up by category, so that we make fewer requests (20 vs 844))
                moves_endpoint_response = requests.get(move_type["url"])
                moves_list = moves_endpoint_response.json()["moves"]
                for move in moves_list:
                    move_object, created = Move.objects.get_or_create(
                        name=move["name"],
                        type=move_type_object,
                    )
                    if created:
                        moves_created += 1

            print(f"{moves_created} Moves and {move_types_created} Move types created")

            # 3) Get pokemon
            print("Downloading Pokemon")

            how_many = str(options["HOW_MANY"])
            if how_many == "ALL":
                print("CATCHING THEM ALL!! (THIS WILL TAKE A COUPLE MINS)")
                # Make one query to get the number of Pokémon in the API
                # Note - we could just set the limit to '99999999999' - it's more efficient and unlikely to cause issues
                initial_pokemon_endpoint_response = requests.get(
                    base_api_address + pokemon_query_string
                )
                limit_string = (
                    f"?limit={initial_pokemon_endpoint_response.json()['count']}"
                )
            else:
                # We set the request to only 20 Pokémon (this is much quicker for testing)
                limit_string = f"?limit={20}"

            # Make the actual request for Pokemon
            pokemon_endpoint_response = requests.get(
                base_api_address + pokemon_query_string + limit_string
            )
            pokemon_list = pokemon_endpoint_response.json()["results"]

            # Update the pokemon in our db, to ensure we have them all
            for pokemon in pokemon_list:
                pokemon_object, created = Pokemon.objects.get_or_create(
                    name=pokemon["name"],
                    api_lookup_number=pokemon["url"].split("/")[6],
                )
                if created:
                    # Create stats - we don't have to do this now, but it allows for easy debugging so
                    # it's staying for the draft
                    Stats.objects.create(related_pokemon=pokemon_object)
                    pokemon_created += 1

            # 4) Get stats & update moves list
            # This would be best sent to a celery beat task, as it will be a lot of requests
            # Can hopefully find a way to get the required data from the APIs list endpoint, but no luck so far.
            for pokemon in Pokemon.objects.all():

                # Get stats object (o2o)
                db_pokemon_stats = pokemon.stats

                # Call the endpoint to get the updated stats
                pokemon_detail_endpoint_response = requests.get(
                    base_api_address
                    + pokemon_query_string
                    + f"/{pokemon.api_lookup_number}"
                )
                downloaded_pokemon_stats = pokemon_detail_endpoint_response.json()[
                    "stats"
                ]

                # Updated the values we are holding in the DB
                # Note: the order of the status is consistent, so we can index into the list but, for future proofing,
                # we may want to assign values by matching the names
                db_pokemon_stats.hp = downloaded_pokemon_stats[0]["base_stat"]
                db_pokemon_stats.attack = downloaded_pokemon_stats[1]["base_stat"]
                db_pokemon_stats.defense = downloaded_pokemon_stats[2]["base_stat"]
                db_pokemon_stats.special_attack = downloaded_pokemon_stats[3][
                    "base_stat"
                ]
                db_pokemon_stats.special_defense = downloaded_pokemon_stats[4][
                    "base_stat"
                ]
                db_pokemon_stats.save()

                # Update the moves list
                downloaded_pokemon_moves = pokemon_detail_endpoint_response.json()[
                    "moves"
                ]
                pokemon_moves_list = [
                    move["move"]["name"] for move in downloaded_pokemon_moves
                ]
                pokemon.moves.set(Move.objects.filter(name__in=pokemon_moves_list))

        self.success(f"{pokemon_created} pokemon created and stats updated for all")
