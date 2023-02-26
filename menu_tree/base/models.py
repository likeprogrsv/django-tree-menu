from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=100
    )
    menu_name = models.ForeignKey(
        Menu,
        null=True, on_delete=models.CASCADE,
        related_name="category"
    )
    parent = models.ForeignKey(
        'self',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )
    position_on_curr_category = models.IntegerField(
        default=0,
        blank=False
    )
    url = models.CharField(max_length=255)

    def __str__(self) -> str:
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return f'{self.menu_name} -> {self.name}'
