from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ArticleForm, LoginForm, NewsletterForm, RegisterForm
from .models import ApprovedArticleLog, Article, Newsletter, Publisher
from .permissions import IsEditor, IsEditorOrJournalist, IsJournalist, is_effective_editor, is_effective_journalist
from .serializers import ApprovedArticleLogSerializer, ArticleSerializer, NewsletterSerializer

User = get_user_model()


class HomeView(LoginView):
    template_name = "newsapp/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class AppLogoutView(LogoutView):
    next_page = reverse_lazy("login")
    http_method_names = ["get", "post", "options", "head"]

    def get(self, request, *args, **kwargs):
        """Allow logout from the navbar link as well as POST submissions."""
        return self.post(request, *args, **kwargs)



def register_view(request: HttpRequest) -> HttpResponse:
    """Allow users to create an account and get auto-assigned to the right group."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to News 24/7. Your account is ready.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "newsapp/register.html", {"form": form})


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    featured_articles = Article.objects.filter(approved=True)[:6]
    pending_articles = Article.objects.filter(approved=False)[:5] if is_effective_editor(request.user) else []
    newsletters = Newsletter.objects.all()[:4]
    return render(
        request,
        "newsapp/dashboard.html",
        {
            "featured_articles": featured_articles,
            "pending_articles": pending_articles,
            "newsletters": newsletters,
        },
    )


@login_required
def article_list_view(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.filter(approved=True)
    return render(request, "newsapp/article_list.html", {"articles": articles})


@login_required
def article_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(Article, pk=pk)
    if not article.approved and not (is_effective_editor(request.user) or is_effective_journalist(request.user)):
        raise Http404("Article not found.")
    return render(request, "newsapp/article_detail.html", {"article": article})


@login_required
def article_create_view(request: HttpRequest) -> HttpResponse:
    if not is_effective_journalist(request.user):
        messages.error(request, "Only journalists can create articles.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Draft article created successfully.")
            return redirect("article_detail", pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, "newsapp/article_form.html", {"form": form, "page_title": "Create article"})


@login_required
def article_update_view(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(Article, pk=pk)
    if not (is_effective_editor(request.user) or is_effective_journalist(request.user)):
        messages.error(request, "You do not have permission to edit articles.")
        return redirect("article_detail", pk=pk)

    if is_effective_journalist(request.user) and not is_effective_editor(request.user) and article.author != request.user:
        messages.error(request, "Journalists can only edit their own articles.")
        return redirect("article_detail", pk=pk)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            updated_article = form.save(commit=False)
            if is_effective_journalist(request.user) and not is_effective_editor(request.user):
                updated_article.approved = False
                updated_article.approval_notified = False
                updated_article.approved_at = None
                updated_article.approved_by = None
            updated_article.save()
            messages.success(request, "Article updated.")
            return redirect("article_detail", pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, "newsapp/article_form.html", {"form": form, "page_title": "Edit article"})


@login_required
def article_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(Article, pk=pk)
    if not (is_effective_editor(request.user) or is_effective_journalist(request.user)):
        messages.error(request, "You do not have permission to delete articles.")
        return redirect("dashboard")
    if is_effective_journalist(request.user) and not is_effective_editor(request.user) and article.author != request.user:
        messages.error(request, "Journalists can only delete their own articles.")
        return redirect("article_detail", pk=pk)
    if request.method == "POST":
        article.delete()
        messages.success(request, "Article deleted.")
        return redirect("article_list")
    return render(request, "newsapp/article_delete.html", {"article": article})


@login_required
def review_articles_view(request: HttpRequest) -> HttpResponse:
    if not is_effective_editor(request.user):
        messages.error(request, "Only editors can review pending articles.")
        return redirect("dashboard")
    pending_articles = Article.objects.filter(approved=False)
    return render(request, "newsapp/review_articles.html", {"pending_articles": pending_articles})


@login_required
def approve_article_view(request: HttpRequest, pk: int) -> HttpResponse:
    if not is_effective_editor(request.user):
        messages.error(request, "Only editors can approve articles.")
        return redirect("dashboard")
    article = get_object_or_404(Article, pk=pk)
    article.approved = True
    article.approved_by = request.user
    article.approved_at = timezone.now()
    article.save()
    messages.success(request, f'"{article.title}" was approved and distributed.')
    return redirect("review_articles")


@login_required
def newsletter_list_view(request: HttpRequest) -> HttpResponse:
    newsletters = Newsletter.objects.prefetch_related("articles", "author").all()
    return render(request, "newsapp/newsletter_list.html", {"newsletters": newsletters})


@login_required
def newsletter_create_view(request: HttpRequest) -> HttpResponse:
    if not (is_effective_editor(request.user) or is_effective_journalist(request.user)):
        messages.error(request, "Only editors and journalists can create newsletters.")
        return redirect("dashboard")
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()
            messages.success(request, "Newsletter created.")
            return redirect("newsletter_list")
    else:
        form = NewsletterForm()
    return render(request, "newsapp/newsletter_form.html", {"form": form, "page_title": "Create newsletter"})


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(approved=True).select_related("author", "publisher")

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsJournalist()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscribedArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Article.objects.filter(approved=True)
            .filter(
                Q(author__in=user.subscribed_journalists.all())
                | Q(publisher__in=user.subscribed_publishers.all())
            )
            .select_related("author", "publisher")
            .distinct()
        )


class ArticleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.select_related("author", "publisher")
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        article = super().get_object()
        if not article.approved and not (is_effective_editor(self.request.user) or is_effective_journalist(self.request.user)):
            raise Http404
        return article

    def update(self, request, *args, **kwargs):
        article = self.get_object()
        if not (is_effective_editor(request.user) or is_effective_journalist(request.user)):
            return Response({"detail": "You do not have permission to update articles."}, status=status.HTTP_403_FORBIDDEN)
        if is_effective_journalist(request.user) and not is_effective_editor(request.user) and article.author != request.user:
            return Response({"detail": "Journalists can only update their own articles."}, status=status.HTTP_403_FORBIDDEN)
        response = super().update(request, *args, **kwargs)
        if is_effective_journalist(request.user) and not is_effective_editor(request.user):
            article.refresh_from_db()
            article.approved = False
            article.approval_notified = False
            article.approved_at = None
            article.approved_by = None
            article.save()
        return response

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        if not (is_effective_editor(request.user) or is_effective_journalist(request.user)):
            return Response({"detail": "You do not have permission to delete articles."}, status=status.HTTP_403_FORBIDDEN)
        if is_effective_journalist(request.user) and not is_effective_editor(request.user) and article.author != request.user:
            return Response({"detail": "Journalists can only delete their own articles."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class ApproveArticleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEditor]

    def post(self, request, pk: int, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        article.approved = True
        article.approved_by = request.user
        article.approved_at = timezone.now()
        article.save()
        return Response({"detail": "Article approved."}, status=status.HTTP_200_OK)


class NewsletterListAPIView(generics.ListAPIView):
    queryset = Newsletter.objects.prefetch_related("articles").all()
    serializer_class = NewsletterSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApprovedArticleLogCreateAPIView(generics.CreateAPIView):
    queryset = ApprovedArticleLog.objects.all()
    serializer_class = ApprovedArticleLogSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        approved_log, _ = ApprovedArticleLog.objects.update_or_create(
            article=serializer.validated_data["article"],
            defaults=serializer.validated_data,
        )
        headers = self.get_success_headers(serializer.data)
        return Response(ApprovedArticleLogSerializer(approved_log).data, status=status.HTTP_201_CREATED, headers=headers)
