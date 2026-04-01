from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import ApprovedArticleLog, Article, Newsletter, Publisher

User = get_user_model()


class NewsAppAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.reader = User.objects.create_user(
            username="reader1",
            password="StrongPass123!",
            email="reader@example.com",
            role=User.ROLE_READER,
        )
        self.editor = User.objects.create_user(
            username="editor1",
            password="StrongPass123!",
            email="editor@example.com",
            role=User.ROLE_EDITOR,
        )
        self.journalist = User.objects.create_user(
            username="journo1",
            password="StrongPass123!",
            email="journo@example.com",
            role=User.ROLE_JOURNALIST,
        )
        self.other_journalist = User.objects.create_user(
            username="journo2",
            password="StrongPass123!",
            email="journo2@example.com",
            role=User.ROLE_JOURNALIST,
        )
        self.publisher = Publisher.objects.create(name="City Gazette", slug="city-gazette", description="Local news")
        self.publisher.editors.add(self.editor)
        self.publisher.journalists.add(self.journalist)
        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

        self.approved_article = Article.objects.create(
            title="Approved story",
            summary="Public summary",
            content="Approved content",
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
            approval_notified=True,
        )
        self.unapproved_article = Article.objects.create(
            title="Draft story",
            summary="Draft summary",
            content="Draft content",
            author=self.journalist,
            publisher=self.publisher,
        )
        self.other_article = Article.objects.create(
            title="Other story",
            summary="Other summary",
            content="Other content",
            author=self.other_journalist,
            approved=True,
            approval_notified=True,
        )
        self.newsletter = Newsletter.objects.create(
            title="Morning Brief",
            description="Daily roundup",
            author=self.journalist,
        )
        self.newsletter.articles.add(self.approved_article)

    def authenticate(self, username: str, password: str):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": username, "password": password},
            format="json",
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_reader_can_view_approved_articles(self):
        self.authenticate("reader1", "StrongPass123!")
        response = self.client.get(reverse("api_article_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [article["title"] for article in response.data]
        self.assertIn("Approved story", titles)
        self.assertNotIn("Draft story", titles)

    def test_reader_only_gets_subscribed_articles(self):
        self.authenticate("reader1", "StrongPass123!")
        response = self.client.get(reverse("api_subscribed_articles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [article["title"] for article in response.data]
        self.assertEqual(titles, ["Approved story"])

    def test_journalist_can_create_article(self):
        self.authenticate("journo1", "StrongPass123!")
        response = self.client.post(
            reverse("api_article_list"),
            {
                "title": "Brand new story",
                "summary": "Breaking summary",
                "content": "Fresh copy",
                "publisher_id": self.publisher.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Article.objects.filter(title="Brand new story", author=self.journalist).exists())

    def test_reader_cannot_create_article(self):
        self.authenticate("reader1", "StrongPass123!")
        response = self.client.post(
            reverse("api_article_list"),
            {"title": "Invalid", "summary": "Nope", "content": "Readers cannot do this."},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_approve_and_delete_article(self):
        self.authenticate("editor1", "StrongPass123!")
        with patch("newsapp.signals.requests.post") as mock_post:
            response = self.client.post(reverse("api_article_approve", args=[self.unapproved_article.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unapproved_article.refresh_from_db()
        self.assertTrue(self.unapproved_article.approved)
        self.assertTrue(mock_post.called)

        delete_response = self.client.delete(reverse("api_article_detail", args=[self.unapproved_article.id]))
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


    def test_editor_group_member_can_approve_article(self):
        reviewer = User.objects.create_user(
            username="group_editor",
            password="StrongPass123!",
            email="group_editor@example.com",
            role=User.ROLE_READER,
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        reviewer.groups.add(editor_group)
        self.authenticate("group_editor", "StrongPass123!")

        with patch("newsapp.signals.requests.post"):
            response = self.client.post(reverse("api_article_approve", args=[self.unapproved_article.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unapproved_article.refresh_from_db()
        self.assertTrue(self.unapproved_article.approved)

    def test_newsletter_endpoint_returns_expected_data(self):
        self.authenticate("reader1", "StrongPass123!")
        response = self.client.get(reverse("api_newsletter_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Morning Brief")
        self.assertEqual(response.data[0]["articles"][0]["title"], "Approved story")

    @patch("newsapp.signals.requests.post")
    def test_signal_sends_email_and_logs_approved_article(self, mock_post):
        article = Article.objects.create(
            title="Signal story",
            summary="Signal summary",
            content="Signal content",
            author=self.journalist,
            publisher=self.publisher,
        )
        article.approved = True
        article.approved_by = self.editor
        article.save()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Signal story", mail.outbox[0].subject)
        self.assertTrue(mock_post.called)
        self.assertTrue(ApprovedArticleLog.objects.filter(article=article).exists())

    def test_failed_request_examples(self):
        response = self.client.get(reverse("api_article_list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.authenticate("journo2", "StrongPass123!")
        response = self.client.delete(reverse("api_article_detail", args=[self.approved_article.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
