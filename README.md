# 🎒 CEC Lost & Found: Smart College Lost & Found Management System

CEC Lost & Found is a full-stack web application built to simplify reporting, discovering, and claiming lost items within the college campus. The platform provides a secure and organized workflow where students can upload found/lost items, browse listings, claim belongings, and track item ownership using student authentication.

🌐 **Live Demo:** (Add after deployment)

---

# ✨ Features

## 👤 For Students

🔐 Secure Authentication
Login and signup system using Django Authentication.

📦 Item Management
Post lost or found items with title, description, location, and contact details.

🖼️ Image Upload Support
Upload images to improve item identification.

📍 Location Tracking
Add where the item was found or lost.

🙋 Claim System
Students can claim listed items.

✅ Claim Status Updates
Items automatically change to CLAIMED.

👀 Claim Visibility
The original poster can view who claimed the item.

---

# 💻 Tech Stack

| Layer          | Technology  | Tools                  |
| -------------- | ----------- | ---------------------- |
| Frontend       | HTML, CSS   | Django Templates       |
| Backend        | Django      | Python                 |
| Database       | SQLite      | Django ORM             |
| Authentication | Django Auth | Session Authentication |
| Media Storage  | Pillow      | Image Upload           |
| Deployment     | Render      | Django Hosting         |

---
# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/AswathyyM/lost_and_found_portal.git
```

---

## 2. Navigate to Project Folder

```bash
cd lost_and_found_portal
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Database Migrations

```bash
python manage.py migrate
```

---

## 5. Start Development Server

```bash
python manage.py runserver
```

---

## 6. Open in Browser

```text
http://127.0.0.1:8000/
```
---

# 📂 Project Structure

```text
lost_and_found/
│
├── manage.py
├── db.sqlite3
├── media/
│
├── lost_and_found/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── items/
│   ├── migrations/
│   ├── templates/
│   │   └── items/
│   │       ├── home.html
│   │       ├── add.html
│   │       ├── login.html
│   │       └── signup.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py

```

---

# 🚀 Getting Started

Follow these steps to run the project locally.

## Prerequisites

Python 3.13+
Django
Pillow

---

# 📖 Usage

Student Registration

↓

Login

↓

Add Lost / Found Item

↓

Upload Image

↓

Other Students Browse

↓

Claim Item

↓

Poster Sees Claim Status

---

# 🤝 Contributing

Contributions are welcome.

Fork the repository.

Create feature branch:

```bash
git checkout -b feature/new-feature
```

Commit:

```bash
git commit -m "feat: add feature"
```

Push:

```bash
git push origin feature/new-feature
```

Open Pull Request.

Please ensure your changes follow project structure and coding standards.

IMPORTANT:

All architectural decisions made during development must be documented in `memory.md`.

---

# 🏛️ Architecture Overview

Frontend (Templates)

↓

Views

↓

Django ORM

↓

SQLite Database

↓

Media Storage

---

# 📜 License

This project is licensed under the MIT License.

---

# 📬 Contact



Maintainer:

M Aswathy

📧 Email: aswathym12321@gmail.com
