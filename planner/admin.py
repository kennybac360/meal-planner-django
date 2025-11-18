from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    MealPlanDay,
    MealEntry,
    ShoppingList,
    ShoppingListItem,
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "default_unit",
        "calories_per_unit",
        "protein_g_per_unit",
        "carbs_g_per_unit",
        "fat_g_per_unit",
        "sodium_mg_per_unit",
    )
    search_fields = ("name",)
    list_filter = ("default_unit",)
    ordering = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "meal_type", "user", "servings")
    list_filter = ("meal_type", "user")
    search_fields = ("name", "instructions")
    inlines = [RecipeIngredientInline]
    autocomplete_fields = ("user",)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity", "unit")
    list_filter = ("unit", "ingredient")
    search_fields = ("recipe__name", "ingredient__name")


class MealEntryInline(admin.TabularInline):
    model = MealEntry
    extra = 1


@admin.register(MealPlanDay)
class MealPlanDayAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "notes")
    list_filter = ("user", "date")
    search_fields = ("notes", "user__username")
    inlines = [MealEntryInline]
    ordering = ("-date",)


@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ("meal_plan_day", "meal_type", "recipe", "portion_multiplier")
    list_filter = ("meal_type", "meal_plan_day__user")
    search_fields = ("recipe__name", "meal_plan_day__notes")


class ShoppingListItemInline(admin.TabularInline):
    model = ShoppingListItem
    extra = 1


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("user", "week_start_date", "created_at")
    list_filter = ("user", "week_start_date")
    inlines = [ShoppingListItemInline]
    ordering = ("-week_start_date",)


@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ("shopping_list", "ingredient", "quantity", "unit", "is_checked")
    list_filter = ("is_checked", "ingredient")
    search_fields = ("ingredient__name",)
