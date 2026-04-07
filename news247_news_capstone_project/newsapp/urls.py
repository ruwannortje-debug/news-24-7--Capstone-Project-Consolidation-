"""URL routes for the News 24/7 web pages and API endpoints."""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AppLogoutView,
    ApprovedArticleLogCreateAPIView,
    ApproveArticleAPIView,
    ArticleListCreateAPIView,
    ArticleRetrieveUpdateDestroyAPIView,
    HomeView,
    NewsletterListAPIView,
    SubscribedArticleListAPIView,
    approve_article_view,
    article_create_view,
    article_delete_view,
    article_detail_view,
    article_list_view,
    article_update_view,
    dashboard_view,
    newsletter_create_view,
    newsletter_list_view,
    register_view,
    review_articles_view,
)

urlpatterns = [
    path("", HomeView.as_view(), name="login"),
    path("register/", register_view, name="register"),
    path("logout/", AppLogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("articles/", article_list_view, name="article_list"),
    path("articles/create/", article_create_view, name="article_create"),
    path("articles/<int:pk>/", article_detail_view, name="article_detail"),
    path("articles/<int:pk>/edit/", article_update_view, name="article_update"),
    path("articles/<int:pk>/delete/", article_delete_view, name="article_delete"),
    path("review/", review_articles_view, name="review_articles"),
    path("review/<int:pk>/approve/", approve_article_view, name="approve_article"),
    path("newsletters/", newsletter_list_view, name="newsletter_list"),
    path("newsletters/create/", newsletter_create_view, name="newsletter_create"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/articles/", ArticleListCreateAPIView.as_view(), name="api_article_list"),
    path("api/articles/subscribed/", SubscribedArticleListAPIView.as_view(), name="api_subscribed_articles"),
    path("api/articles/<int:pk>/", ArticleRetrieveUpdateDestroyAPIView.as_view(), name="api_article_detail"),
    path("api/articles/<int:pk>/approve/", ApproveArticleAPIView.as_view(), name="api_article_approve"),
    path("api/newsletters/", NewsletterListAPIView.as_view(), name="api_newsletter_list"),
    path("api/approved/", ApprovedArticleLogCreateAPIView.as_view(), name="api_approved_log"),
]
