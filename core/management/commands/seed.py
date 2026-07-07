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
            ('To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott & Co.', Book.BOOK),
            ('1984', 'George Orwell', 'Secker & Warburg', Book.BOOK),
            ('The Great Gatsby', 'F. Scott Fitzgerald', 'Charles Scribner\'s Sons', Book.BOOK),
            ('Sapiens', 'Yuval Noah Harari','Harvill Secker', Book.BOOK),
            ('Dune', 'Frank Herbert', 'Chilton Books', Book.BOOK),
            ('The Road', 'Cormac McCarthy', 'Alfred A. Knopf', Book.BOOK),
            ('Educated', 'Tara Westover', 'Random House', Book.BOOK),
            ('Atomic Habits', 'James Clear', 'Avery', Book.BOOK),
            ('The Hitchhiker\'s Guide to the Galaxy', 'Douglas Adams', 'Pan Books', Book.BOOK),
            ('Normal People', 'Sally Rooney', 'Faber & Faber', Book.BOOK),
            ('Thinking, Fast and Slow', 'Daniel Kahneman', 'Farrar, Straus and Giroux', Book.BOOK),
            # CDs
            ('Kind of Blue', 'Miles Davis', 'Columbia Records', Book.CD),
            ('Rumours', 'Fleetwood Mac', 'Warner Bros. Records', Book.CD),
            ('Back to Black', 'Amy Winehouse', 'Island Records', Book.CD),
            # DVDs
            ('Planet Earth II', 'BBC', 'BBC Studios', Book.DVD),
            ('2001: A Space Odyssey', 'Stanley Kubrick', 'MGM', Book.DVD),
        ]

        for title, author, publisher, media_type in books:
            obj, created = Book.objects.update_or_create(
                title=title,
                author=author,
                defaults=dict(
                    publisher=publisher,
                    media_type=media_type
                )
            )
        action = 'Created' if created else 'Updated'

        self.stdout.write(self.style.SUCCESS('\n✅ Seed complete!'))
