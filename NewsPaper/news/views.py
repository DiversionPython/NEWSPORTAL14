# from django.contrib.auth import get_user_model
from datetime import datetime

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
# from django.core.mail import send_mail
# from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# from django.views import View
from django.views.generic import TemplateView
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.utils import timezone
import pytz #  импортируем стандартный модуль для работы с часовыми поясами
from NewsPaper import settings
from .models import Post, Category
from .filters import PostSearch
from .forms import PostForm, UserForm
from django.core.cache import cache
import logging

from django.utils.translation import gettext as _ # импортируем функцию для перевода
# from django.utils.translation import activate, get_supported_language_variant, LANGUAGE_SESSION_KEY

logger = logging.getLogger(__name__)


# class Index(View):
#     def get(self, request):
#         string = _('Hello world')
#
#         # return HttpResponse(string)
#         context = {
#             'string': string
#         }
#         return HttpResponse(render(request, 'index.html', context))

class NewsList(LoginRequiredMixin, ListView):
   model = Post
   ordering = 'title'
   template_name = 'News.html'
   context_object_name = 'news'
   extra_context = {'title': 'Новости'}
   author = 'author'
   # queryset = Post.objects.order_by('-dateCreation')
   paginate_by = 10

   # Переопределяем функцию получения списка товаров
   def get_queryset(self):
       # Получаем обычный запрос
       queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # в этом юните ранее.
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне.
       self.filterset = PostSearch(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
       return self.filterset.qs

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['value1'] = _('Сегодня ( ')
       context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
       value2 = _(') Все новости . общее количество новостей ->>')
       context['value3'] = f"{value2} {Post.objects.all().count()}"
       context['current_time'] = timezone.now()
       print(timezone.now())
       context['timezones'] = pytz.common_timezones  # добавляем в контекст все доступные часовые пояса]
       return context

   def post(self, request):
       request.session['django_timezone'] = request.POST['timezone']
       print(request.session['django_timezone'], timezone.now())
       return redirect('http://127.0.0.1:8000/newsall/')

   def post_search(request):
       f = PostSearch(request.GET,
                      queryset=Post.objects.all())
       return render(request,
                     'search.html',
                     {'filter': f})

   def set_language(request):
       lang = request.POST.get('language', 'en')
       request.session[settings.LANGUAGE_SESSION_KEY] = lang
       response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
       response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
       return response

   # def get(self, request):
   #     curent_time = timezone.now()
   #
   #     # .  Translators: This message appears on the home page only
   #     models = Post.objects.all()
   #
   #     context = {
   #         'models': models,
   #         'current_time': timezone.now(),
   #         'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
   #     }
   #
   #     return HttpResponse(render(request, 'news.html', context))

   #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
   def post(self, request):
       request.session['django_timezone'] = request.POST['timezone']
       return redirect('/')


class NewsDetail(DetailView):
    model = Post
    template_name = 'onenews.html'
    context_object_name = 'onenews'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostSearchView(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'search.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'NewsSearch'
    paginate_by = 10  # поставим постраничный вывод в 10 элементов
    ordering = ['-id']
    queryset = Post.objects.all()  # Default: Model.objects.all()
    # form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_filter(self):
        return PostSearch(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'filter': self.get_filter(),
        }


class PostCreateNW(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'
    permission_required = ('create.Post_Create',)

    def form_valid(self, form):
        post = form.save(commit=True)
        post.categoryType = "NW"
        return super().form_valid(form)


class PostEditNW(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class PostDeleteNW(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')



class PostDeleteAR(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')

class LoginUser(LoginRequiredMixin, LoginView):
    form_class = UserForm
    template_name = 'user_login.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return  reverse_lazy('news')

class UserEdit(LoginRequiredMixin, LoginView):
    form_class = UserForm
    # model = User
    template_name = 'user_edit.html'
    success_url = reverse_lazy('post_list')

    def get_object(self, **kwargs):
        return self.request.user

class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'


class CategoryList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'category.html'
    context_object_name = 'category'
    paginate_by = 10


@login_required
def add_subscribe(request, pk):
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


# class HelloTask(View):
#     def get(self, request):
#         hello.delay()
#         return HttpResponse('Hello!')
#
#
# class SendMail(View):
#     def get(self, request, send_mail_for_sub_test=None):
#         # printer.apply_async([10], countdown=10)
#         # hello.delay()
#         send_mail_for_sub_test.delay()
#         return HttpResponse('Hello!')

# def index(request):
#     return HttpResponse