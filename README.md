# django_menu_tree

В Django реализовал древовидное меню через template tag. 
Меню хранится и редактируется в БД; отображается на странице по названию. На одной странице может быть несколько меню. На отрисовку каждого меню требуется ровно 1 запрос к БД. Для работы серверной части приложения достаточно Django и Python. В качестве БД, для удобства тестирования на другом компьютере, использовал SQLite3 вместо PostgreSQL.

Логин и пароль администратора: admin/admin.

![alt text](https://github.com/likeprogrsv/django-tree-menu/blob/main/menu_tree_example1.gif)
![alt text](https://github.com/likeprogrsv/django-tree-menu/blob/main/menu_tree_example2.gif)