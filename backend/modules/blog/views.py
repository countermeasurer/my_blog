from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class ArticleDetailView(DeleteView):
    model = Article
    template_name = 'blog/articles_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class ArticleByCategoryListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    category = None

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Article.objects.all().filter(category__slug=self.category.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статья из категории: {self.category.title}'
        return context


from django.views.generic import CreateView, UpdateView

from .models import Article
from .forms import ArticleCreateForm, ArticleUpdateForm
from ..services.mixins import AuthorRequiredMixin


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Article
    template_name = 'blog/articles_create.html'
    form_class = ArticleCreateForm
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статей на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class ArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Article
    template_name = 'blog/articles_update.html'
    context_object_name = 'article'
    form_class = ArticleUpdateForm
    login_url = 'home'
    success_message = 'Материал был успешно обновлен'
    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи:{self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: для удаления материала
    """

    model = Article
    success_url = reverse_lazy('home')
    context_object_name = 'article'
    template_name = 'blog/articles_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {self.object.title}'
        return context



from django.shortcuts import render
from django.core.paginator import Paginator


def articles_list(request, page):
    articles = Article.objects.all()
    paginator = Paginator(articles, per_page=2)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'page_obj': page_object}
    return render(request, 'blog/articles_func_list.html', context)


