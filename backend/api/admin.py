from django.contrib import admin

from recipes_and_ingridients.models import (
    Favorite, Ingredient,
    Recipe, Tag, ShoppingCart
)
from users.models import (
    Follow, MyUser
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'quantity_favorites')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)

    def quantity_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('first_name',)
