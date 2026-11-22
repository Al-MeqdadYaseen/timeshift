# Timeshift

Timeshift is an interactive web app for calculating time dilation in special and general relativity, showing how motion and gravity affect the passage of time.

I built it because I’m interested in physics and space, especially time as a fourth dimension.

## 🎥 Video Demo

[![Watch the Demo](https://img.youtube.com/vi/i0H7Fupv5Kg/maxresdefault.jpg)](https://youtu.be/i0H7Fupv5Kg)

## ✨ Core Features

- **Special relativity calculator:** Enter velocity as a fraction of the speed of light and proper time to calculate the Lorentz factor (gamma) and dilated time.
- **Gravitational time dilation calculator:** Choose a preset celestial object—Earth, the Sun, a white dwarf, a neutron star, or a black hole near its horizon—and calculate dilated time using its configured factor. These preset values are simplified educational approximations.
- **Physics explanations:** Read brief explanations, formulas, and examples alongside both calculators.
- **Saved calculation history:** Keep calculations in the session while working, save them to the database, and review the 10 most recent entries on the home page.
- **Input and save safeguards:** Form validation, clear error and success messages, and duplicate-save prevention help keep calculations reliable.
- **Interactive controls:** A velocity slider updates its displayed value, and the interface includes responsive styling for smaller screens.

## 🛠️ Tech Stack

- **Python 3.12+** and **Django 6.0**
- **django-environ** for environment-based settings and database configuration
- **SQLite** for the local database
- **Django templates**, HTML, CSS, and vanilla JavaScript for the interface; no frontend framework or build step is required to run the app
- Python’s standard-library `math` module for the special-relativity calculation; no external scientific library is used
- **Developer tools:** Black, Ruff, pre-commit, and Prettier

## 🚀 Local Setup

You’ll need Git and Python 3.12 or newer.

1. Clone the repository and create a virtual environment:

   ```bash
   git clone https://github.com/Al-MeqdadYaseen/timeshift.git
   cd timeshift
   python -m venv .venv
   ```

2. Activate the virtual environment:

   ```powershell
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   ```

   ```bash
   # macOS or Linux
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with local development settings:

   ```dotenv
   SECRET_KEY=replace-with-a-local-development-secret
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. Apply database migrations and start the development server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser and try either calculator.
