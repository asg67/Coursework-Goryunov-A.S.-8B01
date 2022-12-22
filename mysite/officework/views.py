from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

class ProjectHome(DataMixin, ListView):
    model = Project
    template_name = 'officework/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))


    def get_queryset(self):
        return Project.objects.filter(is_published=True)


# def index(request):
#     posts = Project.objects.all()
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'officework/index.html', context=context)


# class AreaPersonal(DataMixin,ListView):
#     template_name = 'officework/AreaPersonal.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=" страница")
#         return dict(list(context.items()) + list(c_def.items()))



# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             try:
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка добавления поста')
#     else:
#         form = AddPostForm()
#     return render(request, 'officework/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление товара или услуги'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'officework/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление услуги или товара")
        return dict(list(context.items()) + list(c_def.items()))

# def contact(request):
#     return HttpResponse('Обратная связь')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'officework/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



# def show_post(request, post_slug):
#     post = get_object_or_404(Project, slug=post_slug)
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'officework/post.html', context=context)

class ShowPost(DataMixin, DetailView, FormView):
    form_class = ContactFormPost
    model = Project
    template_name = 'officework/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')



# def login(request):
#     return HttpResponse('Авторизация')


def register(request):
    return HttpResponse('Регистрация')


class ProjectCategory(DataMixin, ListView):
    model = Project
    template_name = 'officework/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Project.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


# def show_category(request, cat_id):
#     posts = Project.objects.filter(cat_id=cat_id)
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'officework/index.html', context=context)



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    # form_class = UserCreationForm
    template_name = 'officework/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    # form_class = AuthenticationForm
    template_name = 'officework/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')



def logout_user(request):
    logout(request)
    return redirect('login')