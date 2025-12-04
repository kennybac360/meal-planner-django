from django import forms
from .models import Recipe, MealPlanDay, ShoppingList


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "meal_type", "instructions", "servings"]
        widgets = {
            "instructions": forms.Textarea(attrs={"rows": 3}),
        }


class MealPlanDayForm(forms.ModelForm):
    class Meta:
        model = MealPlanDay
        fields = ["date", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 2}),
        }


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ["week_start_date"]
