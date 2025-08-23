# 📚 Django-Practice(Library-service)

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Environment Variables](#-environment-variables)
- [Simple Installation](#-simple-installation)
- [Docker Installation](#-docker-installation)
- [API Examples](#-api-examples)
- [API Documentation](#-api-documentation)
- [Stripe](#-stripe-integration)
- [Telegram](#-telegram-notifications)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
---

## 🎯 Overview

**Library-service** is a django-practice project. Full task overview given by MateAcademy to check my abilities with real project and unknown technologies.

---

## 🚀 Features

- 👤 User registration and authentication  
- 🔐 JWT authentication (SimpleJWT)  
- 📖 Book Borrowing
- 💻 Telegram real-time updates
- 💳 Stripe integration
- 🧑‍💻 Admin dashboard  
- 📄 Auto-generated API documentation (Swagger & ReDoc)  
- 🐳 Dockerfile and docker-compose
- ✅ Tested using Django’s built-in testing tools

---

## 🛠️ Tech Stack

- Python 3.11+
- Django 5.2
- Django REST Framework
- PostgreSQL
- Stripe API
- SimpleJWT
- Swagger / ReDoc
- Django Test Framework
- Docker

---

## 🔐 Environment Variables

To run this project, you will need to add the environment variables to your .env file
Example file you can find in *[.env.sample](env.sample)*

---

## ⚙️ Simple Installation

[Fork](https://github.com/SkepskyiDanylo/airport-api/fork) the repository

Create a `.env` file with the [required](#-environment-variables) environment variables

---

## 🐳 Docker Installation

▶ [Fork](https://github.com/SkepskyiDanylo/airport-api/fork) the repository

Create a `.env` file with the [required](#-environment-variables) environment variables

▶️ Build and start the containers:

```bash

docker-compose build
docker-compose up -d
```

▶️ To stop containers:

```bash

docker-compose down
```
---

## 🧪 Running Tests

```bash

python manage.py test tests
```

---

## 🌐 API Examples

### 🔐 Login

### JWT HEADER CHANGED TO ''AUTHORIZE'!

```https
POST /api/users/token/
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### 🎟 Borrow a Book

```https
POST /api/borrowings/borrowing/
Authorize: Bearer eyJ0eXAiOiJKV1QiLCJh...
Content-Type: application/json

{
  "book": "uuid",
  "expected_return_date": "datetime.date"
}
```

---

## 📄 API Documentation

You can see all `URIs` by starting the project and using:

- Swagger: [`/swagger/`](http://localhost:8000/swagger/)
- ReDoc: [`/redoc/`](http://localhost:8000/redoc/)

---

## 🔐 Authentication & Access

- JWT-based authentication via `djangorestframework-simplejwt`
- Permissions managed using `BookPermission`, `IsAuthenticated`
- Reworked User model to use `email` instead of `username`
---

## 💳 Stripe Integration

- Stripe Checkout session creation when book is borrowed or returned with delay

---
## 💻 Telegram notifications

- When some borrowing is created, or some payment was successful you will receive a message to your CHAT_ID in [.env](#-environment-variables)

``` Telegram
    📚 New Book Borrowing!
    
    User: Anonymous name, test@test.com
    Book: Test Book
    Borrow Date: 23.08.2025
    Expected Return Date: 28.08.2025
```

``` Telegram
    ✅ New Success Payment!
    User: Anonymous name, admin@admin.com
    Book: 123
    Price: 50.00$
    Type: Payment
```

- By the way each day in the morning you will receive a message if there are any overdue by today

```Telegram
    No borrowings overdue today!
```

---

## 🤝 Contributing

Pull requests are welcome!

Before submitting a PR:

- Make sure all tests pass (`python manage.py test tests`)
- Format your code with `black`

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

For questions or feedback:

- Email: kol230305@gmail.com  
- Telegram: [@ViverTonick](https://t.me/ViverTonick)

---
