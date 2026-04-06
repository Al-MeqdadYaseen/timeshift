# Timeshift

Timeshift is a Django web app for exploring relativistic and gravitational time dilation. Users can run calculations, review the computed result immediately, and save recent calculations to the database for later reference.

Video demo: <https://youtu.be/i0H7Fupv5Kg>

## Problem / Solution

Physics students and curious learners often understand the idea of time dilation conceptually, but it is harder to experiment with it through simple, interactive examples. Timeshift solves that by providing two focused calculators, one for relativistic time dilation and one for gravitational time dilation, so users can quickly test inputs, compare outcomes, and save recent calculations for reference.

## Technologies Used

- Python
- Django 6
- SQLite
- HTML
- CSS
- JavaScript
- `django-environ`
- WhiteNoise

## Features

- Relativistic time dilation calculator using velocity as a fraction of the speed of light.
- Gravitational time dilation calculator using preset celestial objects.
- Session-backed result persistence across redirects with duplicate-save protection.
- Recent calculation history on the home page.
- Health endpoint at `/health/` for uptime checks and deployment probes.

## How to Run

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set at minimum `SECRET_KEY`.
4. Apply migrations:

```bash
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

6. Open <http://127.0.0.1:8000/>.

## Production Notes

Timeshift is now configured for production-oriented deployment without changing calculator behavior.

- `DEBUG` should remain `False` in production.
- `ALLOWED_HOSTS` must include the deployed hostname or domain.
- `CSRF_TRUSTED_ORIGINS` should include the full HTTPS origin for the deployed site.
- Static files are served through WhiteNoise after running:

```bash
python manage.py collectstatic --noinput
```

- Security settings such as HSTS, secure cookies, and SSL redirect are controlled through environment variables in `.env.example`.
- `/health/` can be used by a reverse proxy, uptime monitor, or platform health check.

## Configuration

Environment variables used by the project:

- `SECRET_KEY`
- `DEBUG`
- `DATABASE_URL`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `USE_X_FORWARDED_HOST`
- `USE_X_FORWARDED_PORT`
- `SECURE_SSL_REDIRECT`
- `SESSION_COOKIE_SECURE`
- `CSRF_COOKIE_SECURE`
- `SECURE_HSTS_SECONDS`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `SECURE_HSTS_PRELOAD`
- `SECURE_REFERRER_POLICY`

## Verification

Run these before deploying:

```bash
python manage.py check --deploy
python manage.py test
```

## Project Behavior

- `/` shows the landing page and recent saved calculations.
- `/relativistic/` handles the special relativity form using PRG flow.
- `/gravitational/` handles the gravitational calculator using preset object data.
- `/save/<calc_type>/` saves the current session result once and prevents duplicate submissions.
