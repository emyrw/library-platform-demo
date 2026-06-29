# Library platform demo

A prototype for managing library book loans, with Reader and Librarian roles. Made with Django and Postgres
## Quick Start (local)
Install the requirements and perform the DB migrations. A seeder script for local use is provided to populate the DB with dummy data. The app will run on http://localhost:8000.
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed        
python manage.py runserver
```

## Features

**Reader users can:**
- View their active loans with return due dates
- Browse the full book catalogue with availability status
- Search books by title or author

**Librarian users can:**
- Search and view loans by each reader
- Register new loans (select reader, book, due date)
- Register returns of books
- Modify/extend due dates on existing loans

### Admin / backdoor
There is an admin panel where you can manually add more users an books. This is accessible at http://localhost:8000/admin/. You need a superuser account to login to the admin panel. The 'librarian1' user created in the seeder script should have these priviledges. Alternatively, to create a new superuser locally you can run
```bash
python manage.py createsuperuser
```
in the project directory and follow the instructions and prompts for username, pwd, etc.


