from django.core.validators import MinValueValidator
from django.db import models

from users.models import MyUser as User


class Tag(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name='Название тега'
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код', unique=True, max_length=7
    )
    slug = models.SlugField(
        max_length=100, unique=True, verbose_name='Уникальный слаг'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=100, verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор рецепта'
    )
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/', verbose_name='Картинка рецепта'
    )
    text = models.TextField(max_length=200, verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientQuantity', verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1, message='Минимум 1 минута!'
            )
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, message='Количество должно быть больше 0!')
        ]
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredients_in_recipe'
            )
        ]
        verbose_name = 'Количество ингредиента'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites', verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_recipe_in_favorite'
            )
        ]
        verbose_name = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_carts', verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_carts', verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shopping_cart'
            )
        ]
        verbose_name = 'Корзина покупок'
