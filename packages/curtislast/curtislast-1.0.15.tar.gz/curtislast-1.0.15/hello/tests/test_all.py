from django.test import SimpleTestCase
from hello.forms import ProjectForm
import pytest
from django.contrib.admin.sites import AdminSite
from mixer.backend.django import mixer
from hello import admin
from hello import models
from django.urls import reverse, resolve
from hello.views import project_create_view, project_views
from django.test import TestCase, Client
from hello.models import Project
from django.urls import reverse


pytestmark = pytest.mark.django_db


class TestViews(TestCase):
    def test_create_list_GET(self):
        client = Client()
        response = client.get(reverse("create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/project_create.html")
         
    def test_project_views_GET(self):
        client = Client()
        response = client.get(reverse("project"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project/project.html")

    def test_hello_views_GET(self):
        client = Client()
        response = client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hello_world.html")

class TestUrls(SimpleTestCase):
    def test_create_url_is_resolved(self):
        url = reverse("create")
        self.assertEqual(resolve(url).func, project_create_view)

    def test_project_url_is_resolved(self):
        url = reverse("project")
        self.assertEqual(resolve(url).func, project_views)


class TestProjectAdmin:
	def test_expect(self):
		 site = AdminSite()


class TestForms(SimpleTestCase):
    def test_project_form_valid(self):
        form = ProjectForm(
            data={"title": "capuchino"}
        )
        self.assertTrue(form.is_valid())

    def test_project_form_no_data(self):
        form = ProjectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors), 3)


class EntryModelTest(TestCase):

    def test_string_representation(self):
        entry = Project(title="title")
        self.assertEqual(str(entry), entry.title)
