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

## 🏗️ Project Structure

```
Morocco_API/
│
├── Morocco_API/              
│   ├── settings.py           
│   ├── urls.py             
│   ├── asgi.py           
│   └── wsgi.py          
│
├── events/                 
│   ├── models.py       
│   ├── serializers.py   
│   ├── views.py           
│   ├── filters.py           
│   ├── permissions.py      
│   ├── pagination.py        
│   ├── services.py         
│   ├── admin.py        
│   └── urls.py           
│
├── users/              
│   ├── models.py           
│   ├── serializers.py       
│   ├── views.py             
│   ├── permissions.py      
│   ├── signals.py          
│   └── urls.py          
│
├── manage.py             
└── requirements.txt         
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (optional, SQLite included)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/CallMeHoussam/Morocco_API
cd Morocco_API
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create sample data**
```bash
python create_sample_data.py
```

6. **Start development server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📋 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/register/` | User registration |
| POST | `/api/v1/users/login/` | User login |
| POST | `/api/v1/token/refresh/` | Refresh JWT token |

### Events
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/events/` | List all events |
| POST | `/api/v1/events/` | Create new event |
| GET | `/api/v1/events/{id}/` | Get event details |
| PUT | `/api/v1/events/{id}/` | Update event |
| DELETE | `/api/v1/events/{id}/` | Delete event |
| GET | `/api/v1/events/upcoming/` | Upcoming events |
| GET | `/api/v1/events/stats/` | Event statistics |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/me/` | Get user profile |
| PATCH | `/api/v1/users/me/` | Update user profile |
| POST | `/api/v1/users/me/password/` | Change password |
| GET | `/api/v1/users/me/stats/` | User event statistics |

## 🧪 Test Cases

### Health Check
```http
GET http://127.0.0.1:8000/health/
```

### User Registration
```http
POST http://127.0.0.1:8000/api/v1/users/register/
Content-Type: application/json

{
    "username": "learner",
    "email": "backend@alx.com",
    "password": "AlxBackend",
    "password_confirm": "AlxBackend",
    "first_name": "ALX",
    "last_name": "Student"
}
```

### User Login
```http
POST http://127.0.0.1:8000/api/v1/users/login/
Content-Type: application/json

{
    "username": "learner",
    "password": "AlxBackend"
}
```

### Create Event
```http
POST http://127.0.0.1:8000/api/v1/events/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "title": "Tech Conference 2024",
    "description": "Annual technology conference featuring industry leaders",
    "short_description": "Tech conference with workshops and networking",
    "location": "Casablanca Tech Hub",
    "city": 1,
    "category": 6,
    "start_date": "2024-03-15T09:00:00Z",
    "end_date": "2024-03-16T18:00:00Z",
    "image_url": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4",
    "ticket_url": "https://example.com/tickets"
}
```

### Get User Profile
```http
GET http://127.0.0.1:8000/api/v1/users/me/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Update User Profile
```http
PATCH http://127.0.0.1:8000/api/v1/users/me/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "first_name": "Updated",
    "last_name": "Name",
    "email": "updated@email.com"
}
```

### Change Password
```http
POST http://127.0.0.1:8000/api/v1/users/me/password/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "old_password": "AlxBackend",
    "new_password": "NewSecurePassword123",
    "new_password_confirm": "NewSecurePassword123"
}
```

For more tests [Click here](https://docs.google.com/document/d/1q2GH3mEUzL2u7aC-ujAg4uMyPcsqD0-ioJ_4IX-HZHo/edit?usp=sharing)

## 🔧 Configuration

### Environment Variables
```py
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### External API Keys (Optional)
```py
EVENTBRITE_TOKEN=your_eventbrite_token
TICKETMASTER_KEY=your_ticketmaster_key
```

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Admin Interface
Access the Django admin at `http://127.0.0.1:8000/admin/` with superuser credentials.

### Generating Sample Data
```bash
python create_sample_data.py
```

---

**Made For capstone project**