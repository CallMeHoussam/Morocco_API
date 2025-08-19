
---

# 📂 Project Structure

```
Morocco_API/
│
├── Morocco_API/         # Main project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── events/               # Events app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── users/                # Users app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── manage.py
└── requirements.txt
```
## Morocco API 🇲🇦
A Django REST API providing information about Morocco’s cities, culture, and events.

### Features
- JWT Authentication
- Search & Filter
- Pagination
- Swagger Documentation

### Setup
```bash
git clone https://github.com/CallMeHoussam/Morocco_API
cd Morocco_API
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
