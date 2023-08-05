from django.test import TestCase

from .models import Shoppinglist
from .forms import NameForm, DeleteForm


class AppTests(TestCase):

    # to create a sample test database
    def setUp(self):
        Shoppinglist.objects.create()

    # test whether an entry's string representation is equal to its title
    def test_string_representation(self):
        entry = Shoppinglist(title="My entry title")
        self.assertEqual(str(entry), entry.title)

    # test to make sure our homepage returns an HTTP 200 status code
    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    # to test whether the entries show up on the homepage
    def test_one_entry(self):
        Shoppinglist.objects.create(title='1-title', description='1-body',
                                    price=100.00)
        response = self.client.get('')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, 100.00)

    def test_two_entries(self):
        Shoppinglist.objects.create(title='1-title', description='1-body',
                                    price='100.00')
        Shoppinglist.objects.create(title='2-title', description='2-body',
                                    price=500.00)
        response = self.client.get('')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, '100.00')
        self.assertContains(response, '2-title')
        self.assertContains(response, '2-body')
        self.assertContains(response, 500.00)

    # test if form is valid and contains valid data
    def test_valid_data(self):
        form = NameForm({
            'title': "this",
            'description': "this and this",
            'price': "100.00",
        })
        self.assertTrue(form.is_valid())
        shoplist = form.save()
        self.assertEqual(shoplist.title, "this")
        self.assertEqual(shoplist.description, "this and this")
        self.assertEqual(shoplist.price, 100.00)

    def test_delete(self):
        form = DeleteForm({
            'btn': "Yes"
        })
        self.assertTrue(form.is_valid())
'''        response = self.client.get('list_delete/<int:pk>/')
        self.assertContains(response, 'Are you sure you want to remove ?')'''
