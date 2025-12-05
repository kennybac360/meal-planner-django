from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from .models import Recipe, MealPlanDay, ShoppingList
from .forms import RecipeForm, MealPlanDayForm, ShoppingListForm


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "planner/recipe_list.html"
    context_object_name = "recipes"

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user).order_by("name")


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "planner/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "planner/recipe_form.html"

    def form_valid(self, form):
        # tie recipe to current user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("planner:recipe-detail", kwargs={"pk": self.object.pk})


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "planner/recipe_form.html"

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy("planner:recipe-detail", kwargs={"pk": self.object.pk})


class MealPlanDayListView(LoginRequiredMixin, ListView):
    model = MealPlanDay
    template_name = "planner/mealplan_list.html"
    context_object_name = "days"

    def get_queryset(self):
        return MealPlanDay.objects.filter(user=self.request.user).order_by("date")


class MealPlanDayDetailView(LoginRequiredMixin, DetailView):
    model = MealPlanDay
    template_name = "planner/mealplan_detail.html"
    context_object_name = "day"

    def get_queryset(self):
        return MealPlanDay.objects.filter(user=self.request.user)


class MealPlanDayCreateView(LoginRequiredMixin, CreateView):
    model = MealPlanDay
    form_class = MealPlanDayForm
    template_name = "planner/mealplan_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("planner:mealplan-detail", kwargs={"pk": self.object.pk})


class ShoppingListListView(LoginRequiredMixin, ListView):
    model = ShoppingList
    template_name = "planner/shoppinglist_list.html"
    context_object_name = "shopping_lists"

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user).order_by("-week_start_date")


class ShoppingListDetailView(LoginRequiredMixin, DetailView):
    model = ShoppingList
    template_name = "planner/shoppinglist_detail.html"
    context_object_name = "shopping_list"

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = "planner/shoppinglist_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("planner:shoppinglist-detail", kwargs={"pk": self.object.pk})
