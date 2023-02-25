from django.test import TestCase
from django.db import models

from main.models import User
from main.utils import db_utils


class DbUtilsTest(TestCase):
    def test_should_return_integer_field_name(self):
        class Model(models.Model):
            int_field = models.IntegerField()

        self.assertEqual("int_field", db_utils.get_column_name(Model.int_field))

    def test_should_return_integer_field_name_with_custom_name(self):
        class Model(models.Model):
            int_field = models.IntegerField(name="nice_int_field", verbose_name="Nice integer field")

        self.assertEqual("nice_int_field", db_utils.get_column_name(Model.nice_int_field))

    def test_should_return_foreign_key_column_name(self):
        class Model(models.Model):
            user_field = models.ForeignKey(User, on_delete=models.CASCADE)

        self.assertEqual("user_field_id", db_utils.get_column_name(Model.user_field))

    def test_should_return_table_name(self):
        class MyModel(models.Model):
            pass

        self.assertEqual("main_mymodel", db_utils.get_table_name(MyModel))
