from django.contrib import admin

from .models import (Favorite, Ingredient,
                     Recipe, RecipeIngredient,
                     RecipeTag, ShoppingList, Tag)


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_filter = ['name']
    search_fields = ('name',)


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ['name']
    search_fields = ('name',)


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeTagsInline(admin.TabularInline):
    model = RecipeTag


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'in_favorite')
    list_filter = ['name', 'author', 'tags']
    search_fields = ('name', 'author__email')
    inlines = (RecipeIngredientsInline, RecipeTagsInline)

    def in_favorite(self, obj):
        return obj.in_favorite.all().count()
    in_favorite.short_description = 'В ИЗБРАННОМ'


@admin.register(Favorite)
class AdminFavorite(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_filter = ['user', 'recipe']
    search_fields = ('user__email', 'recipe__name')


@admin.register(ShoppingList)
class AdminShoppingList(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_filter = ['user', 'recipe']
    search_fields = ('user__email', 'recipe__name')
