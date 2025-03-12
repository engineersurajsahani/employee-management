# Django Project

A web application built with Django, featuring image handling with Pillow and a customized admin interface.

## Setup Instructions

Follow these steps to set up and run the project locally:

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Environment Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/your-repository-name.git
   cd your-repository-name
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

### Installation

4. Install required packages:
   ```
   pip install django
   pip install Pillow
   pip install django-admin-interface
   ```

### Database Setup

5. Apply database migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

### Running the Server

6. Start the development server:
   ```
   python manage.py runserver
   ```
   The application will be available at http://127.0.0.1:8000/

## Admin Interface

The project uses `django-admin-interface` for an enhanced admin experience. To access the admin panel:

1. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

2. Navigate to http://127.0.0.1:8000/admin/ and log in with your superuser credentials.
