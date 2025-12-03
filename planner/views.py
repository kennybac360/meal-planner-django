from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Recipe, MealPlanDay, ShoppingList


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "planner/recipe_list.html"
    context_object_name = "recipes"

    def get_queryset(self):
        # only show recipes for the logged-in user
        return Recipe.objects.filter(user=self.request.user).order_by("name")


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "planner/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)


class MealPlanDayDetailView(LoginRequiredMixin, DetailView):
    model = MealPlanDay
    template_name = "planner/mealplan_detail.html"
    context_object_name = "day"

    def get_queryset(self):
        return MealPlanDay.objects.filter(user=self.request.user)


class ShoppingListDetailView(LoginRequiredMixin, DetailView):
    model = ShoppingList
    template_name = "planner/shoppinglist_detail.html"
    context_object_name = "shopping_list"

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)


# Create your views here.
