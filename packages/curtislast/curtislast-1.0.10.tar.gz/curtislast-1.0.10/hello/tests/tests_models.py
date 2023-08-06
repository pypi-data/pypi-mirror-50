import pytest

from hello.models import Project

pytestmark = pytest.mark.django_db


class TestProjectModel:

    def test_save():
        product = Project.objects.create(
            title='Sample',
            describe='team',
            technology='goood'
        )
        assert product.title == Sample
        assert product.describe == team
        assert product.technology == goood
