# Django Project Setup & Installation Guide

## Project Structure

```
sociaIexperts/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── sociaIexperts/                    # Django project configuration
│   ├── __init__.py
│   ├── settings.py                   # Project settings
│   ├── urls.py                       # Main URL routing
│   ├── asgi.py                       # ASGI config for async
│   └── wsgi.py                       # WSGI config for production
├── apps/
│   └── core/                         # Main app
│       ├── __init__.py
│       ├── models.py                 # Database models
│       ├── views.py                  # View functions
│       ├── urls.py                   # App URL routing
│       ├── forms.py                  # Django forms
│       ├── admin.py                  # Admin configuration
│       ├── apps.py
│       └── migrations/               # Database migrations
├── templates/                        # HTML templates (extending base.html)
│   ├── base.html                     # Base template with header/footer
│   ├── index.html                    # Home page
│   ├── about.html                    # About page
│   ├── services.html                 # Services page
│   ├── projects.html                 # Projects page
│   ├── blog.html                     # Blog page
│   ├── login.html                    # Login form
│   └── register.html                 # Registration form
├── static/                           # Static files
│   ├── css/
│   │   └── style.css                 # Main stylesheet
│   ├── js/
│   │   └── script.js                 # Main JavaScript
│   └── images/                       # All images (webp, jpeg, png)
└── assets/                           # Original asset files (can be removed after setup)
    ├── css/
    ├── js/
    └── imgs/
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### 2. Create and Activate Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
# Create database tables
python manage.py migrate

# Create a superuser for Django admin
python manage.py createsuperuser
```

### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000`

## Pages & URLs

| Page | URL | View |
|------|-----|------|
| Home | `/` | `core:home` |
| About | `/about/` | `core:about` |
| Services | `/services/` | `core:services` |
| Projects | `/projects/` | `core:projects` |
| Blog | `/blog/` | `core:blog` |
| Login | `/accounts/login/` | `accounts:login` |
| Register | `/accounts/register/` | `accounts:register` |
| Logout | `/accounts/logout/` | `accounts:logout` |
| Admin | `/admin/` | Django admin |

## Features

### 1. **Template Inheritance**
- `base.html` contains header, footer, and navigation
- All pages extend `base.html`
- Consistent layout across all pages
- Dynamic navbar with user authentication status

### 2. **Authentication**
- User registration with validation
- User login with email or username support
- Logout functionality
- Remember me option
- Password confirmation matching
- Email uniqueness validation

### 3. **Newsletter Subscription**
- Newsletter model in database
- Subscribe form in footer (visible on all pages)
- Newsletter admin interface

### 4. **Static Files**
- CSS: Bootstrap 5, custom styles
- JavaScript: AOS animations, Swiper sliders, custom scripts
- Images: All project images properly organized
- All assets served via Django static system

### 5. **Forms**
- `LoginForm`: Username/email + password login
- `RegisterForm`: User registration with password confirmation
- `NewsletterForm`: Email subscription
- CSRF protection on all forms

### 6. **Views**
- Function-based views for all pages
- Authentication decorators
- Message framework for user feedback
- Proper error handling

## Customization

### Change Secret Key (Important for Production)
Edit `sociaIexperts/settings.py`:
```python
SECRET_KEY = 'your-new-secure-key-here'
```

### Add Email Configuration
For email functionality, update in `sociaIexperts/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Debug Mode for Production
In `sociaIexperts/settings.py`, set to `False` for production:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn sociaIexperts.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker (Optional)
Create a `Dockerfile` and `docker-compose.yml` for containerized deployment.

### Key Security Settings
1. Change `SECRET_KEY` to a random secure value
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Enable HTTPS only
6. Set secure cookie flags

## Admin Interface

Access Django admin at: `/admin/`

**Features:**
- Manage newsletter subscriptions
- View and manage users
- Monitor all application data

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Database errors
```bash
python manage.py migrate
```

### Import errors
```bash
pip install -r requirements.txt
```

### Port already in use
```bash
python manage.py runserver 8001
```

## Technology Stack

- **Backend**: Django 4.2.8
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **CSS Framework**: Bootstrap 5.2.3
- **Animations**: AOS (Animate On Scroll)
- **Sliders**: Swiper 11
- **Icons**: Bootstrap Icons
- **Database**: SQLite (development) / PostgreSQL (production recommended)
- **Server**: Gunicorn (production)

## Features Preserved from Original

✅ Responsive design - All breakpoints maintained
✅ Animations - AOS scroll animations working
✅ Sliders - Swiper carousel functional
✅ Navigation - Active states, dropdowns
✅ Search popup - Mobile-friendly
✅ Sidebar offcanvas - Mobile menu
✅ Forms - Login and registration
✅ All styling - Colors, fonts, spacing preserved
✅ All images - WebP, JPEG, PNG formats
✅ All interactions - JavaScript functionality

## Next Steps

1. **Add Database Content**:
   - Create blog posts
   - Add team members
   - Manage projects

2. **Setup Email**:
   - Configure email backend
   - Enable password reset

3. **Add Media**:
   - Configure media uploads
   - Add user profile images

4. **Testing**:
   - Write unit tests
   - Test forms and authentication
   - Performance testing

5. **Deployment**:
   - Choose hosting provider
   - Configure domain
   - Setup SSL certificate
   - Optimize performance

## Support

For Django documentation: https://docs.djangoproject.com/
For Bootstrap documentation: https://getbootstrap.com/docs/
For AOS documentation: https://michalsnik.github.io/aos/
