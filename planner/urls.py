from django.urls import path
from . import views

app_name = "planner"

urlpatterns = [
    # Recipes
    path("recipes/", views.RecipeListView.as_view(), name="recipe-list"),
    path("recipes/<int:pk>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("recipes/new/", views.RecipeCreateView.as_view(), name="recipe-create"),
    path("recipes/<int:pk>/edit/", views.RecipeUpdateView.as_view(), name="recipe-edit"),

    # Meal plans
    path("meal-plans/", views.MealPlanDayListView.as_view(), name="mealplan-list"),
    path("meal-plans/<int:pk>/", views.MealPlanDayDetailView.as_view(), name="mealplan-detail"),
    path("meal-plans/new/", views.MealPlanDayCreateView.as_view(), name="mealplan-create"),

    # Shopping lists
    path("shopping-lists/", views.ShoppingListListView.as_view(), name="shoppinglist-list"),
    path("shopping-lists/<int:pk>/", views.ShoppingListDetailView.as_view(), name="shoppinglist-detail"),
    path("shopping-lists/new/", views.ShoppingListCreateView.as_view(), name="shoppinglist-create"),
]