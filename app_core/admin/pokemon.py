from django.contrib import admin

from app_core.models import Move, MoveType, Pokemon, Stats


class StatsInline(admin.StackedInline):
    model = Stats
    readonly_fields = (
        "hp",
        "attack",
        "defense",
        "special_attack",
        "special_defense",
    )
    extra = 0


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    search_fields = ("name",)

    list_display = (
        "name",
        "get_hp",
        "get_attack",
        "get_defense",
        "get_special_attack",
        "get_special_defense",
        "get_move_selection",
    )

    fields = (
        "api_lookup_number",
        "name",
        "moves",
    )

    readonly_fields = (
        "api_lookup_number",
        "name",
        "moves",
    )

    def get_hp(self, obj):
        return obj.stats.hp

    get_hp.admin_order_field = "hp"
    get_hp.short_description = "HP"

    def get_attack(self, obj):
        return obj.stats.attack

    get_hp.admin_order_field = "attack"
    get_hp.short_description = "Attack"

    def get_defense(self, obj):
        return obj.stats.defense

    get_hp.admin_order_field = "defense"
    get_hp.short_description = "Defense"

    def get_special_attack(self, obj):
        return obj.stats.special_attack

    get_hp.admin_order_field = "special_attack"
    get_hp.short_description = "Special Attack"

    def get_special_defense(self, obj):
        return obj.stats.special_defense

    get_hp.admin_order_field = "special_defense"
    get_hp.short_description = "Special Defense"

    def get_move_selection(self, obj):
        return (
            ",".join(
                [f"{move.name} ({move.type}) " for move in obj.moves.order_by("?")[:4]]
            )
            + "...."
        )

    inlines = [
        StatsInline,
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Move)
class MovesAdmin(admin.ModelAdmin):
    search_fields = ("name",)

    list_filter = ("type",)

    list_display = (
        "name",
        "type",
    )

    fields = (
        "name",
        "type",
    )

    readonly_fields = (
        "name",
        "type",
    )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MoveType)
class MoveTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "get_move_selection")

    fields = (
        "name",
        "get_move_selection",
    )

    readonly_fields = (
        "name",
        "get_move_selection",
    )

    def get_move_selection(self, obj):
        return ",".join([move.name for move in obj.moves.order_by("?")[:4]]) + "...."

    get_move_selection.short_description = "Example Moves"

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
