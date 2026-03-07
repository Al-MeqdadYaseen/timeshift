# Timeshift

A Django project demonstrating relativistic and gravitational time dilation calculators.

---

## Video Demo: [https://youtu.be/i0H7Fupv5Kg]

### Description

#### Introduction

Time dilation is a major concept in Einstein's theory of relativity. It basically describes how time is measured differently by two observers under certain conditions. We have time dilation in special relativity which describes how time changes for a moving observer relative to a stationary observer and there is gravitational time dilation which is about how gravity slows down time due to the curvature a mass causes to spacetime. I made this program because I am interested in Physics and Space and especially intriguied by time as a forth dimension. That's what motivated me to build this project.
Timeshift is an interactive web app built with Django framework. It lets users understand how time dilates under special relativity (high velocities) and general relativity (strong gravity) and optionally save calculations for later review.

#### Purpose

The purpose of this webapp is to help people interested in relativity theory or physics students to be able to calculate and understand time dilation.

#### Features

- **Relativistic Calculator**: Compute time dilation given a fraction of light speed and proper time.
- **Gravitational Calculator**: Choose from preset celestial objects and calculate time dilation near them.
- Results are stored temporarily in session and can be saved to the database.
- Saved history table on the homepage displaying the latest calculations.
- Validation, error messages, and prevention of duplicate saves.

#### Physics Background

As mentioned earlier, time dilation arises from Einstein’s theories of relativity:

- **Special Relativity**: Moving clocks tick slower. The Lorentz factor \(\gamma = 1/\sqrt{1 - v^2/c^2}\) quantifies how much an observer’s time stretches when traveling at velocity \(v\).
- **General Relativity**: Clocks in a gravitational potential run slower relative to distant observers. Stronger gravity (near massive bodies) produces larger effects. The app uses simplified multipliers for familiar objects like Earth, Sun, and black holes.

#### Usage

1. Clone the repository and create a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Start the development server: `python manage.py runserver`.
5. Visit `http://localhost:8000/` to access the calculators.
6. Perform a calculation and optionally save it using the "Save Calculation" button. Refreshing the page clears the current result.

Feel free to explore and extend the project further.

### Detailed Functionality

#### Routing and Views

- `/` : homepage shows a brief introduction, routes to relativistic and gravitational routes.
- `/relativistic/` : special relativity calculator view. Accepts POST from a form, validates input with `RelativisticForm`, performs gamma/dilation calculation handled by `core.utils.calculate_relativistic`, stores results in session, and redirects back (PRG structure).
- `/gravitational/` : gravitational calculator view using `GravitationalForm` to validate proper time and object selection from `GRAVITATIONAL_OBJECTS` dictionary. The calculation logic lives in `core.utils.calculate_gravitational` and uses preconfigured multipliers.
- `/save/<calc_type>/` : generic endpoint handling saving of session results to the `Calculation` model. CSRF-protected and guards against missing results or duplicate submissions.

#### Session & State Management

- Calculations are temporarily kept in the user session under keys like `relativistic_result` or `gravitational_result`.
- A display flag (`*_displayed`) tracks whether the result has been shown; a page refresh clears the stored result and any saved form data.
- After saving a calculation, a separate session flag (`*_saved`) prevents duplicate database entries.
- Form input values are kept in session (`*_form`) to repopulate fields after redirects, enabling persistent inputs until the page is refreshed or a new calculation is made.

### Models & Persistence

- `Calculation` model stores both common fields (`proper_time`, `dilated_time`, `calculation_type`) and type-specific data (velocity/gamma for relativistic; gravitational_factor/object_name for gravitational).
- Objects are capped and validated via model validators. The homepage query returns the 10 most recent entries and displays type-specific details using template logic.

### Templates & Styling

- Shared `base.html` defines navigation, message display, and static files (css and js files) loading.
- Calculators extend base and include form groups, error handling, and result boxes styled with CSS classes such as `form-group`, `result-box`, `btn`, `btn-secondary`, and `table-responsive` for mobile-friendliness.
- Dropdown menus and sliders update using a small vanilla JS file (`static/js/app.js`) which also prevents duplicate save submissions client-side.

### Validation & UX

- Forms enforce numeric ranges and required selections through Django form validators and custom `clean_` methods.
- Server-side messages use Django's messages framework to inform users of success, errors, or duplicate-save attempts.
- When session expires or a save is attempted without a calculation, friendly error messages appear without raising exceptions.
- The application avoids stale state: refreshing the calculator page clears the result and form, while the save endpoint resets display flags to ensure results persist until intentionally cleared.

#### Challenges

I was planning to implement more features like user db, unit conversion, and some visualization effects like clocks ticking beside each other with respect to the dilation factor being calculated. That was the reason I chosen Django framework which is a bit harder than Flask. However due to the fact I have not had enough time, I implemented the MVP features.
Coding with AI tools is a big advantage when it comes to generating many lines of codes, however, they generate buggy code a lot of times and sometimes they break some previously working functionalities. So I spend a lot of debugging and sometimes redoing the whole code myself.
The last challenge was challenge was implementing views and sessions to properly render results and save them

That was it. This it Timeshift.

<!-- Part of this file was made by AI -->
