# Messaging App

A simple Django REST Framework (DRF) based messaging application that supports:

- Custom user model extending Django’s AbstractUser
- Conversations between multiple users
- Messages linked to conversations and senders
- Nested REST API endpoints for conversations and their messages

---

## Features

- Extendable User model with additional fields
- Conversation model tracking participants (many-to-many with users)
- Message model linked to conversations and senders
- RESTful API endpoints to create and list conversations and messages
- Nested routing for messages within conversations using `drf-nested-routers`

---

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- Django REST Framework
- drf-nested-routers

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/messaging_app.git
   cd messaging_app
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Linux/macOS
   env\Scripts\activate     # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

## **API Usage**

**Base URL**

```bash
python manage.py runserver
```

### Endpoints

| Endpoint                        | Method | Description                          |
| ------------------------------- | ------ | ------------------------------------ |
| `/conversations/`               | GET    | List all conversations               |
| `/conversations/`               | POST   | Create a new conversation            |
| `/conversations/{id}/`          | GET    | Retrieve a conversation's details    |
| `/conversations/{id}/messages/` | GET    | List all messages in a conversation  |
| `/conversations/{id}/messages/` | POST   | Send a new message in a conversation |
