from .models import Category

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "Добавить", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        # {'title': "Личный кабинет", 'url_name': 'AreaPersonal'},
]


class DataMixin:
    paginate_by = 4
    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.annotate(Count('women'))

        user_menu = menu.copy()
        if (not self.request.user.is_superuser) and (not self.request.user.is_staff):
            # not self.request.user.is_authenticated
            user_menu.pop(1)
        cats = Category.objects.all()
        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
