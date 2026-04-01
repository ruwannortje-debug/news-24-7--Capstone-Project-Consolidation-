from rest_framework import serializers

from .models import ApprovedArticleLog, Article, CustomUser, Newsletter, Publisher


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "slug", "description"]


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(
        source="publisher",
        queryset=Publisher.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "content",
            "author",
            "publisher",
            "publisher_id",
            "created_at",
            "updated_at",
            "approved",
            "approved_at",
        ]
        read_only_fields = ["approved", "approved_at", "created_at", "updated_at"]


class NewsletterSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    articles = ArticleSerializer(many=True, read_only=True)
    article_ids = serializers.PrimaryKeyRelatedField(
        source="articles",
        many=True,
        queryset=Article.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Newsletter
        fields = ["id", "title", "description", "author", "articles", "article_ids", "created_at", "updated_at"]


class ApprovedArticleLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovedArticleLog
        fields = ["id", "article", "title", "author_username", "publisher_name", "approved_at"]
