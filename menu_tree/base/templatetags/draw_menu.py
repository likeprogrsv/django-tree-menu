from django import template
from django.urls import reverse
from ..models import Category, Menu
from typing import List, Dict
from django.db.models.query import QuerySet


register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context: List[dict], menu_name: str):
    """Return a html content into templates"""
    request = context['request']
    current_url: str = request.path
    if current_url == '/favicon.ico/':
        return ''

    try:
        all_menu_items: QuerySet[Category] = Category.objects.filter(
            menu_name__name=menu_name).select_related(
            'parent').order_by('position_on_curr_category')
    except Menu.DoesNotExist as e:
        raise e(f'Меню с именем {menu_name} не найдено!')
    finally:
        if not all_menu_items:
            print(
                  f'//////////////////////////////////////\n'
                  f'Меню с именем {menu_name} не найдено '
                  f'или в нём нет элементов!\n'
                  f'//////////////////////////////////////\n'
                  )

    active_menu = MenuTemplate(all_menu_items, current_url)
    return active_menu.render_menu()


class MenuTemplate:
    """Class to construct and display tree menu on templates"""
    def __init__(self, all_menu_items: QuerySet[Category], current_url: str):
        self.all_menu_items = all_menu_items
        self.current_url = current_url
        self._checked: set = set()
        self.__categories_to_render: list = []
        self.__urls_dict: Dict[str, Category] = {
            f'/{v.url}/': v for v in self.all_menu_items
            }

    def render_menu(self) -> str:
        """Return a html content"""
        main_page_categories: List[Category] = (
            self.get_main_categories()
        )

        if self.current_url in self.__urls_dict:
            self.__categories_to_render = (
                 main_page_categories
                 + self.get_active_categories()
            )
            return self.__make_html(self.__categories_to_render)
        else:
            return self.__make_html(main_page_categories)

    def get_main_categories(self) -> List[Category]:
        """Return main categories if other not selected"""
        return [category for category in
                self.all_menu_items if category.parent is None]

    def get_active_categories(self) -> List[Category]:
        """Returns the categories that should be displayed
        based on the received url
        """
        categories: List[Category] = []
        active_category: Category = None
        if self.current_url in self.__urls_dict:
            active_category = self.__urls_dict[self.current_url]
        else:
            return []

        for categ in self.all_menu_items:
            if (categ == active_category.parent):
                categories.extend(self.__get_above_categories(categ))
            if (active_category == categ.parent or
                    active_category.parent == categ.parent or
                    active_category == categ):
                categories.append(categ)
        return categories

    def __get_above_categories(self, category: Category) -> List[Category]:
        above_categories: List[Category] = []
        if category.parent is not None:
            above_categories.extend(
                self.__get_above_categories(category.parent))
            for categ in self.all_menu_items:
                if category.parent == categ.parent:
                    above_categories.append(categ)
        return above_categories

    def __make_html(self, menu: List[Category]) -> str:
        html: str = ''
        for category in menu:
            if category in self._checked:
                continue
            html += '<li class="">'
            html += (f'<a class="a-white"'
                     f' href="{reverse("categories", args=[category.url])}"'
                     f' class="">{category.name}</a>')

            child_categories: List[Category] = []
            for categ in self.__categories_to_render:
                if category == categ.parent:
                    child_categories.append(categ)
            if child_categories:
                html += '<ul>'
                html += self.__make_html(child_categories)
                html += '</ul>'

            html += '</li>'
            self._checked.add(category)
        return html
