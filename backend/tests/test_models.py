from django.test import TestCase
from recipes.models import Tag


class TagModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag = Tag.objects.create(
            name='test_name',
            color='BLUE',
            slug='test_slug'
        )
    
    def test_name(self):
        """поле name совпадает с ожидаемым."""
        tag = TagModelTest.tag
        name = tag.name
        self.assertEqual(name, 'test_name')

    def test_title_help_text(self):
        """поле color совпадает с ожидаемым"""
        tag = TagModelTest.tag
        color = tag.color
        self.assertEqual(color, 'BLUE')

    def test_object_name_is_title_fild(self):
        """поле slug совпадает с ожиадемым"""
        tag = TagModelTest.tag
        slug = tag.slug
        self.assertEqual(slug, 'test_slug')
    
    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        tag = TagModelTest.tag
        field_verboses = {
            'name': 'название Тега',
            'color': 'цвет',
            'slug': 'поле Slug'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    tag._meta.get_field(field).verbose_name, expected_value)






