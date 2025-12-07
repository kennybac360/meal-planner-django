from django.db.models import Sum, F, FloatField

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    default_unit = models.CharField(max_length=20, help_text="e.g., g, cup, tbsp")

    calories_per_unit = models.FloatField(help_text="Calories per default unit")
    protein_g_per_unit = models.FloatField(default=0)
    carbs_g_per_unit = models.FloatField(default=0)
    fat_g_per_unit = models.FloatField(default=0)
    sodium_mg_per_unit = models.FloatField(default=0)

    # optional extras
    fiber_g_per_unit = models.FloatField(default=0, blank=True)
    sugar_g_per_unit = models.FloatField(default=0, blank=True)
    vitamin_a_mg_per_unit = models.FloatField(default=0, blank=True)
    vitamin_c_mg_per_unit = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    MEAL_TYPES = [
        ("any", "Any"),
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
        ("smoothie", "Smoothie"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    name = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    instructions = models.TextField(blank=True)
    servings = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
    def total_calories(self):
        return sum(
            ri.quantity * ri.ingredient.calories_per_unit
            for ri in self.recipe_ingredients.all()
        )
    def total_protein(self):
        return sum(
            ri.quantity * ri.ingredient.protein_g_per_unit
            for ri in self.recipe_ingredients.all()
        )
    def total_carbs(self):
        return sum(
            ri.quantity * ri.ingredient.carbs_g_per_unit
            for ri in self.recipe_ingredients.all()
        )
    def total_fat(self):
        return sum(
            ri.quantity * ri.ingredient.fat_g_per_unit
            for ri in self.recipe_ingredients.all()
        )
    def total_sodium(self):
        return sum(
            ri.quantity * ri.ingredient.sodium_mg_per_unit
            for ri in self.recipe_ingredients.all()
        )
    def per_serving_calories(self):
        return self.total_calories() / self.servings if self.servings else 0
    
    def per_serving_protein(self):
        return self.total_protein() / self.servings if self.servings else 0


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_recipes")
    quantity = models.FloatField()
    unit = models.CharField(max_length=20, help_text="e.g., cup, tbsp, g")

    class Meta:
        unique_together = ("recipe", "ingredient", "unit")

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name} in {self.recipe.name}"


class MealPlanDay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_days")
    date = models.DateField()
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    def total_daily_calories(self):
        total = 0
        for entry in self.entries.select_related('recipe'):
            total+= entry.portion_multiplier * entry.recipe.per_serving_calories()
        return total


class MealEntry(models.Model):
    MEAL_TYPES = Recipe.MEAL_TYPES

    meal_plan_day = models.ForeignKey(MealPlanDay, on_delete=models.CASCADE, related_name="entries")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="meal_entries")
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    portion_multiplier = models.FloatField(default=1.0)

    def __str__(self):
        return f"{self.meal_plan_day.date} - {self.get_meal_type_display()}: {self.recipe.name}"


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shopping_lists")
    week_start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shopping List starting {self.week_start_date} for {self.user.username}"


class ShoppingListItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="items")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="shopping_items")
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ingredient.name} ({self.quantity} {self.unit})"
