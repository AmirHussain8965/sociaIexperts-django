# SOCIAL EXPERTS - Django Project

A production-ready Django web application for SOCIAL EXPERTS - a digital marketing and IT services company.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Installation (5 minutes)

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Run development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

## 📁 Project Structure

```
sociaIexperts/
├── manage.py                    # Django CLI
├── requirements.txt             # Dependencies
├── .env.example                # Environment template
├── DJANGO_SETUP.md             # Detailed setup guide
├── sociaIexperts/              # Project configuration
├── apps/core/                  # Main Django app
├── templates/                  # HTML templates
├── static/                     # CSS, JS, images
└── media/                      # User uploads
```

## 🌐 Website Pages

| Page | URL | Purpose |
|------|-----|---------|
| **Home** | `/` | Landing page with hero section |
| **About** | `/about/` | Company info, team, testimonials |
| **Services** | `/services/` | List of services offered |
| **Projects** | `/projects/` | Portfolio and case studies |
| **Blog** | `/blog/` | Blog articles |
| **Login** | `/login/` | User authentication |
| **Register** | `/register/` | New user signup |
| **Admin** | `/admin/` | Django admin panel |

## ✨ Features

✅ **Responsive Design** - Works on all devices (mobile, tablet, desktop)
✅ **Professional UI** - Bootstrap 5 with custom styling
✅ **Animations** - Smooth AOS scroll animations
✅ **Sliders** - Swiper.js carousels
✅ **Authentication** - User registration and login
✅ **Newsletter** - Email subscription system
✅ **Forms** - CSRF protection, validation
✅ **Admin Panel** - Django admin interface
✅ **SEO Ready** - Meta tags, semantic HTML
✅ **Production Ready** - Gunicorn, WhiteNoise, security configs

## 🛠 Technology Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Bootstrap 5.2
- **Animations**: AOS, Swiper.js
- **Icons**: Bootstrap Icons
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Server**: Gunicorn

## 📋 Admin Features

Access at `/admin/` with your superuser account:

- **Newsletter Management** - View and manage subscriptions
- **User Management** - Manage users and permissions
- **Content Management** - Create/edit pages
- **Analytics** - View user activity

## 🔐 Security

- CSRF protection on all forms
- Secure password hashing
- SQL injection prevention
- XSS protection
- Environment variables for secrets

## 📝 Configuration

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🚀 Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn sociaIexperts.wsgi:application --bind 0.0.0.0:8000
```

### Production Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Change SECRET_KEY to a random value
- [ ] Configure allowed hosts
- [ ] Setup PostgreSQL database
- [ ] Configure email backend
- [ ] Enable HTTPS only
- [ ] Setup SSL certificate
- [ ] Configure static files serving
- [ ] Setup monitoring and logging
- [ ] Backup database regularly

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.core

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📚 Documentation

- [Detailed Setup Guide](DJANGO_SETUP.md)
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Docs](https://getbootstrap.com/docs/)
- [AOS Documentation](https://michalsnik.github.io/aos/)

## 🐛 Troubleshooting

### Static files not loading

```bash
python manage.py collectstatic --noinput
```

### Database errors

```bash
python manage.py migrate
```

### Module not found

```bash
pip install -r requirements.txt
```

### Port already in use

```bash
python manage.py runserver 8001
```

## 📞 Support

For issues or questions:
1. Check [Django Documentation](https://docs.djangoproject.com/)
2. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/django)
3. Open an issue in your repository

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💼 About

SOCIAL EXPERTS is a digital marketing and IT services company with 10+ years of experience. This Django project migrates their website from static HTML to a dynamic web application.

---

**Created**: May 2024  
**Python Version**: 3.8+  
**Django Version**: 4.2.8
