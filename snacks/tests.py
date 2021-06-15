from django.http import response
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Snack
# Create your tests here.

class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="mugh", email="mugh98@email.com", password="pass123"
        )

        self.snack = Snack.objects.create(
            title="tomato", description="cool", purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "tomato")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "tomato")
        self.assertEqual(f"{self.snack.purchaser}", "mugh")
        self.assertEqual(self.snack.description, 'cool')

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tomato")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "purchaser :mugh")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "carrot",
                "description": "nice",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_list"))
        self.assertContains(response, "carrot")



    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated title","description":"alrighte","purchaser":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_list"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)