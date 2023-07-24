from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Борис')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        users_notes = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        url = reverse('notes:list')
        for user, note_in_list in users_notes:
            with self.subTest(user=user, note_in_list=note_in_list):
                response = user.get(url)
                if note_in_list:
                    self.assertContains(response, self.note.title)
                else:
                    self.assertNotContains(response, self.note.title)

    def test_pages_contains_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for page, args in urls:
            with self.subTest(page=page):
                url = reverse(page, args=args)
                response = self.author_client.get(url)
                self.assertIsInstance(response.context['form'], NoteForm)
                self.assertIn('form', response.context)
