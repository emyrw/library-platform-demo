from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Book
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database'

    def handle(self, *args, **kwargs):
        # Librarians
        password = os.environ.get('SEED_PWD') or input('Enter password for demo accounts: ')

        if not User.objects.filter(username='librarian1').exists():
            User.objects.create_superuser('librarian1', 'librarian1@test.com', password, role='librarian',
                                          first_name='Test', last_name='Test')
            self.stdout.write('Created librarian: librarian1')

        # Readers
        readers = [
            ('reader1', 'Test1', 'Test1', 'reader1@test.com'),
            ('reader2', 'Test2', 'Test2', 'reader2@test.com'),
            ('reader3', 'Test3', 'Test3', 'reader3@test.com'),
        ]
        for username, first, last, email in readers:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, email, password,
                                         role='reader', first_name=first, last_name=last)
                self.stdout.write(f'Created reader: {username}')

        # Books
        books = [
            ('To Kill a Mockingbird', 'Harper Lee'),
            ('1984', 'George Orwell'),
            ('The Great Gatsby', 'F. Scott Fitzgerald'),
            ('Sapiens', 'Yuval Noah Harari'),
            ('Dune', 'Frank Herbert'),
            ('The Road', 'Cormac McCarthy'),
            ('Educated', 'Tara Westover'),
            ('The Name of the Wind', 'Patrick Rothfuss'),
            ('Atomic Habits', 'James Clear'),
            ('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams'),
            ('Normal People', 'Sally Rooney'),
            ('Thinking, Fast and Slow', 'Daniel Kahneman'),
        ]
        for title, author in books:
            if not Book.objects.filter(title=title, author=author).exists():
                Book.objects.create(title=title, author=author)
                self.stdout.write(f'Created book: {title}')

        self.stdout.write(self.style.SUCCESS('\n✅ Seed complete!'))
