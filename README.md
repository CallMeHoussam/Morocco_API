
# Morocco Events API 🇲🇦

A comprehensive Django REST API for discovering and managing events across Morocco. Features JWT authentication, advanced search/filtering, and event management capabilities.

## ✨ Features

- **🔐 JWT Authentication** - Secure user registration and login
- **📋 Event Management** - Create, read, update, and soft delete events
- **🔍 Advanced Search** - Filter by city, category, date, and region
- **📱 Pagination** - Efficient data handling with customizable page sizes
- **🌐 External Integration** - Import events from external APIs (Eventbrite, Ticketmaster)
- **👥 User Profiles** - Personal profiles with event statistics
- **⚡ Performance Optimized** - Fast response times with optimized queries
- **🛡️ Admin Moderation** - Event approval system for content control

## Project Structure
```
Morocco_API/
│
├── Morocco_API/         
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── events/               
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── filter.py
│   ├── models.py
│   ├── pagination.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
│
├── users/                
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── views.py
│   ├── tests.py
│   └── urls.py
│
├── manage.py
└── requirements.txt
```

### Setup
```bash
git clone https://github.com/CallMeHoussam/Morocco_API
cd Morocco_API
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Test Cases 
# Health Check
GET http://127.0.0.1:8000/health/

# Register
```http
POST http://127.0.0.1:8000/api/v1/users/register/ 
  Content-Type: application/json
  {
    "username": "learner",
    "email": "Backend@Alx.com",
    "password": "AlxBackend",
    "password_confirm": "AlxBackend"
  }
  ```
# Login
```http
POST http://127.0.0.1:8000/api/v1/users/login/ 
  Content-Type: application/json
  {
    "username": "learner",
    "password": "RegisterPassword"
  }
```
# Events

# Create new event
```http
POST http://127.0.0.1:8000/api/v1/events/
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN

{
    "title": " ",
    "description": " ",
    "short_description": " ",
    "location"  : "Test Location, Casablanca",
    "city": 1,
    "category"  : 1,
    "start_date": "Y-M-DTH:M:SZ",
    "end_date"  : "Y-M-DTH:M:SZ",
    "image_url" : "link here",
    "ticket_url": "link here"
}
```
# User Profile
```http
GET http://127.0.0.1:8000/api/v1/users/me/
Authorization: Bearer ACCESS_TOKEN
```

Update user => 
```http
PATCH http://127.0.0.1:8000/api/v1/users/me/
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN

{
    "first_name": "Updated",
    "last_name": "Name",
    "email": "updated@email.com"
}
```
# Change password
```http
POST http://127.0.0.1:8000/api/v1/users/me/password/
Content-Type: application/json
Authorization: Bearer ACCESS_TOKEN

{
    "old_password": " ",
    "new_password": " ",
    "new_password_confirm": " "
}
```

if you want more tests check : https://docs.google.com/document/d/1q2GH3mEUzL2u7aC-ujAg4uMyPcsqD0-ioJ_4IX-HZHo/edit?usp=sharing