# Django Calorie Counter Project using HTML form

## Contents

- [Description](#description)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Pages, Routes, and Views](#pages-routes-and-views)
  - [Authentication Pages](#authentication-pages)
  - [Dashboard and Profile Pages](#dashboard-and-profile-pages)
  - [Calorie Tracking Pages](#calorie-tracking-pages)
- [Django Template Setup](#django-template-setup)
- [Context Data Flow](#context-data-flow)
- [Navigation Page and URL Names](#navigation-page-and-url-names)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Run the Project](#run-the-project)
- [Environment Variables](#environment-variables)
- [Usage / Examples](#usage--examples)
- [Related Possible Functionalities](#related-possible-functionalities)
- [License](#license)
- [Contact](#contact)

## Description

This project is a lightweight Django-based calorie tracking application designed for users who want to manage daily food intake, track consumed calories, and keep a simple profile with calculated Basal Metabolic Rate (BMR). The application uses Django’s built-in authentication system, custom user handling, SQLite for local persistence, and Bootstrap-based HTML templates for a clean and functional interface.

It is best suited for personal health tracking, small demo projects, and learning how to build a complete Django app with templates, URL routing, models, and user-specific data handling.

## Key Features

- **User registration and login flow** using Django authentication with custom `User` model support.
- **Profile management** to store name, age, gender, height, weight, and calculated BMR.
- **Daily calorie tracking** for consumed food items with item name and calorie values.
- **Dashboard summary** showing total consumed calories, required calories, and whether the user needs to eat more or less.
- **CRUD operations** for calorie entries through dedicated add, update, and delete views.
- **Bootstrap-powered templates** for a simple UI across registration, login, dashboard, profile, and calorie pages.
- **Session-aware navigation** with conditional menu items for authenticated and unauthenticated users.
- **Message system integration** to provide user feedback for successful registration, login, and item operations.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Django 6.1 |
| Database | SQLite |
| Frontend | HTML, Bootstrap 5 |
| Auth | Django built-in authentication |
| Media handling | Django `MEDIA_URL` / `MEDIA_ROOT` |
| Dependency management | `requirements.txt` |

## Project Structure

```text
Django-Calorie-Counter-Project-using-HTML-form/
├── CalorieCounter/
│   ├── Templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── calories/
│   │   │   ├── calorie-form.html
│   │   │   └── calorie-list.html
│   │   ├── master/
│   │   │   ├── base.html
│   │   │   ├── message.html
│   │   │   └── nav.html
│   │   ├── profile/
│   │   │   ├── profile-form.html
│   │   │   └── profile.html
│   │   └── dashboard.html
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── Mehedi_101_CalorieCounter/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt
└── LICENSE
```

## Pages, Routes, and Views

The application is organized around a single Django app named `CalorieCounter`. The URL mapping is defined in `CalorieCounter/urls.py`, while the main project-level router is defined in `Mehedi_101_CalorieCounter/urls.py`.

### Authentication Pages

| Route | View | Purpose |
| --- | --- | --- |
| `/` | `register_page` | Registration page |
| `/login/` | `login_page` | Login page |
| `/logout/` | `logout_page` | Logout and redirect to login |

```python
# CalorieCounter/urls.py
urlpatterns = [
    path('', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
]
```

### Dashboard and Profile Pages

| Route | View | Purpose |
| --- | --- | --- |
| `/dashboard/` | `dashboard_page` | Summary of consumed calories, required calories, and suggestions |
| `/profile/` | `profile_page` | Shows stored profile information |
| `/update-profile/` | `update_profile` | Updates profile details and recalculates BMR |

```python
# views.py
@login_required
def dashboard_page(request):
    try:
        current_user = request.user
        bmr = round(request.user.user_info.bmr, 2)
    except:
        current_user = None
        bmr = 0

    today = date.today()
    today_consumed_data = ConsumedCalories.objects.filter(
        consumed_by=current_user,
        created_at=today
    )
```

### Calorie Tracking Pages

| Route | View | Purpose |
| --- | --- | --- |
| `/consumed-calorie-list/` | `consumed_calories_list` | Displays all calorie entries for the logged-in user |
| `/add-calorie/` | `add_calorie` | Adds a new calorie item |
| `/update-calorie/<int:id>/` | `update_calorie` | Updates an existing calorie entry |
| `/delete-calorie/<int:id>/` | `delete_calorie` | Deletes a calorie entry |

```python
# CalorieCounter/urls.py
urlpatterns = [
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('profile/', profile_page, name='profile_page'),
    path('update-profile/', update_profile, name='update_profile'),
    path('consumed-calorie-list/', consumed_calories_list, name='consumed_calories_list'),
    path('add-calorie/', add_calorie, name='add_calorie'),
    path('update-calorie/<int:id>/', update_calorie, name='update_calorie'),
    path('delete-calorie/<int:id>/', delete_calorie, name='delete_calorie'),
]
```

## Django Template Setup

Templates are organized in `CalorieCounter/Templates/` and extend a shared base template. The app uses Bootstrap 5 through CDN and includes a common navigation bar and message renderer.

### Shared Base Template

```html
<!-- CalorieCounter/Templates/master/base.html -->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>Hello, world!</title>
  </head>
  <body>
    {% include 'master/nav.html' %}
    {% include 'master/message.html' %}
    <div class="container">
        {% block body %}
        {% endblock body %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
```

### Navigation Template

```html
<!-- CalorieCounter/Templates/master/nav.html -->
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">CalorieCounter</a>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        {% if request.user.is_authenticated %}
        <li class="nav-item">
          <a class="nav-link" href="{% url 'dashboard_page' %}">Dashboard</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'consumed_calories_list' %}">Consumed Calories</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'profile_page' %}">Profile</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'logout_page' %}">Logout</a>
        </li>
        {% else %}
        <li class="nav-item">
          <a class="nav-link" href="{% url 'login_page' %}">Login</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'register_page' %}">Register</a>
        </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>
```

### Message Template

```html
<!-- CalorieCounter/Templates/master/message.html -->
{% if messages %}
{% for message in messages %}
<div class="alert alert-primary" role="alert">
  {{message}}
</div>
{% endfor %}
{% endif %}
```

## Context Data Flow

This project passes application-specific data directly from the views into the templates. The following examples are taken from the actual code.

### Dashboard Context

```python
context = {
    'required_calories': bmr,
    'today_consumed_data': today_consumed_data,
    'consumed_calories': total_caloire,
    'total_count': total_consumed_calories['total_count'],
    'less_more': less_more,
    'suggestion': suggestion,
}
```

The dashboard uses this data in `Templates/dashboard.html` to display:

- total consumed calories
- required calories
- less/more calories
- daily item list
- suggestion text

### Profile Update Context

```python
context = {
    'profile_data': profile_data
}
```

This is used to pre-populate the profile form in `profile-form.html`.

### Calorie Form Context

```python
context={
    'form_title':'Add Calorie',
    'form_btn':'Add'
}
```

```python
context = {
    'calorie_data':calorie_data,
    'form_title':'Update Calorie',
    'form_btn':'Update'
}
```

These values are used to render the same form template for both add and update actions.

## Navigation Page and URL Names

The application relies on named URL patterns for navigation and redirection. The `name` values defined in `CalorieCounter/urls.py` are used in templates and in `redirect()` calls.

```python
# CalorieCounter/urls.py
urlpatterns = [
    path('', register_page, name='register_page'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page, name='logout_page'),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('profile/', profile_page, name='profile_page'),
    path('update-profile/', update_profile, name='update_profile'),
    path('consumed-calorie-list/', consumed_calories_list, name='consumed_calories_list'),
    path('add-calorie/', add_calorie, name='add_calorie'),
    path('update-calorie/<int:id>/', update_calorie, name='update_calorie'),
    path('delete-calorie/<int:id>/', delete_calorie, name='delete_calorie'),
]
```

Example usage in templates:

```html
<a href="{% url 'dashboard_page' %}">Dashboard</a>
<a href="{% url 'consumed_calories_list' %}">Consumed Calories</a>
<a href="{% url 'profile_page' %}">Profile</a>
<a href="{% url 'logout_page' %}">Logout</a>
```

Example usage in views:

```python
return redirect('login_page')
return redirect('dashboard_page')
return redirect('consumed_calories_list')
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- `pip` and a virtual environment tool
- Git

### Installation

```bash
# Clone the repository
git clone <your-repository-url>
cd Django-Calorie-Counter-Project-using-HTML-form

# Create a virtual environment
python -m venv .venv

# Activate the environment
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Project

```bash
# Apply database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Then open:

- http://127.0.0.1:8000/

## Environment Variables

This project currently does not require any external environment variables. The configuration is kept local and uses the default Django SQLite database and console email backend.

```env
# No external environment variables are required in this project.
# Database: SQLite (db.sqlite3)
# Email backend: console backend
# Debug mode: enabled in settings.py
```

## Usage / Examples

### 1. Register a new account

Open the root route and create a new user with username, email, password, and confirm password.

```text
http://127.0.0.1:8000/
```

### 2. Log in

After registration, login from:

```text
http://127.0.0.1:8000/login/
```

### 3. Update profile

Once logged in, go to the profile page and update your personal information. The app calculates BMR using the provided height, weight, age, and gender.

```text
http://127.0.0.1:8000/profile/
http://127.0.0.1:8000/update-profile/
```

### 4. Add consumed calories

From the calorie list page, add each consumed food item.

```text
http://127.0.0.1:8000/add-calorie/
```

### 5. View the dashboard

The dashboard shows:

- total consumed calories
- required calories
- difference between required and consumed calories
- suggestion text

```text
http://127.0.0.1:8000/dashboard/
```

### Example of field usage in views

```python
# Register flow
User.objects.create_user(
    username=username,
    email=email,
    password=password
)
```

```python
# Calorie item creation
ConsumedCalories.objects.create(
    item_name=item_name,
    calorie=calorie,
    consumed_by=request.user,
)
```

```python
# BMR calculation
if gender == 'Male':
    bmr_calculate = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
else:
    bmr_calculate = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
```

## Animated Data Flow Diagram

The diagram below illustrates how data moves across the app from URL requests to templates and database records.

<div align="center">
<svg width="960" height="430" viewBox="0 0 960 430" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Calorie Counter Data Flow Diagram">
  <defs>
    <linearGradient id="panelGrad" x1="0" x2="1">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" x2="1">
      <stop offset="0%" stop-color="#22c55e" />
      <stop offset="100%" stop-color="#06b6d4" />
    </linearGradient>
    <style>
      .title { font: 700 22px Arial, sans-serif; fill: #0f172a; }
      .label { font: 600 14px Arial, sans-serif; fill: #0f172a; }
      .small { font: 500 12px Arial, sans-serif; fill: #334155; }
      .node {
        fill: #ffffff;
        stroke: #cbd5e1;
        stroke-width: 2;
      }
      .node-dark {
        fill: url(#panelGrad);
        stroke: #0f172a;
        stroke-width: 1.5;
      }
      .line {
        fill: none;
        stroke: url(#accentGrad);
        stroke-width: 3;
        stroke-linecap: round;
        stroke-dasharray: 10 12;
        animation: flow 5s linear infinite;
      }
      .line-soft {
        fill: none;
        stroke: #94a3b8;
        stroke-width: 2;
        stroke-dasharray: 8 10;
        animation: flowSlow 7s linear infinite;
      }
      @keyframes flow {
        from { stroke-dashoffset: 0; }
        to { stroke-dashoffset: -220; }
      }
      @keyframes flowSlow {
        from { stroke-dashoffset: 0; }
        to { stroke-dashoffset: -180; }
      }
    </style>
  </defs>

  <rect x="30" y="25" width="900" height="380" rx="18" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="60" y="60" class="title">Calorie Counter Data Flow</text>

  <rect class="node-dark" x="60" y="90" width="150" height="72" rx="12"/>
  <text x="85" y="120" fill="#f8fafc" class="label">User</text>
  <text x="85" y="142" fill="#cbd5e1" class="small">Register / Login</text>

  <rect class="node" x="285" y="90" width="150" height="72" rx="12"/>
  <text x="310" y="120" class="label">Browser</text>
  <text x="310" y="142" class="small">HTTP Request</text>

  <rect class="node" x="510" y="90" width="150" height="72" rx="12"/>
  <text x="535" y="120" class="label">Django Views</text>
  <text x="535" y="142" class="small">Auth / Profile / Calories</text>

  <rect class="node" x="735" y="90" width="150" height="72" rx="12"/>
  <text x="760" y="120" class="label">SQLite DB</text>
  <text x="760" y="142" class="small">Users &amp; Calories</text>

  <rect class="node" x="260" y="245" width="200" height="90" rx="12"/>
  <text x="288" y="276" class="label">Templates</text>
  <text x="288" y="298" class="small">base.html</text>
  <text x="288" y="315" class="small">nav.html / message.html</text>

  <rect class="node" x="510" y="245" width="180" height="90" rx="12"/>
  <text x="538" y="276" class="label">Context Data</text>
  <text x="538" y="298" class="small">BMR, calories,</text>
  <text x="538" y="315" class="small">item list, suggestions</text>

  <path class="line" d="M210 126 H285"/>
  <path class="line" d="M435 126 H510"/>
  <path class="line" d="M660 126 H735"/>

  <path class="line-soft" d="M330 162 V245"/>
  <path class="line-soft" d="M585 162 V245"/>
  <path class="line-soft" d="M460 290 H510"/>
  <path class="line-soft" d="M690 290 H735"/>

  <text x="230" y="116" class="small">Request</text>
  <text x="445" y="116" class="small">Process</text>
  <text x="680" y="116" class="small">Store</text>
  <text x="478" y="234" class="small">Render</text>
  <text x="690" y="236" class="small">Return</text>
</svg>
</div>

### Diagram explanation

| Flow | Description |
| --- | --- |
| User → Browser | The user interacts with the Django app through the browser using registration, login, dashboard, profile, and calorie forms. |
| Browser → Django Views | The request is routed to the relevant view function in `CalorieCounter/views.py`. |
| Django Views → SQLite DB | Views read and write user and calorie data using Django ORM models. |
| Django Views → Templates | Context data such as BMR, daily totals, and item lists is rendered into HTML templates. |
| Templates → Browser | The final HTML is returned to the browser and displayed to the user. |

## Related Possible Functionalities

The current project is a solid starting point, but it can be extended with professional features that are not yet implemented in this codebase.

- **Daily and weekly calorie charts** using charting libraries such as Chart.js or Plotly.
- **Food database integration** for nutrition lookup by item name or barcode scanning.
- **Goal-based tracking** such as weight loss, maintenance, or muscle gain plans.
- **Admin dashboard analytics** for viewing user activity and calorie patterns.
- **API endpoints** for mobile or frontend clients using Django REST Framework.
- **Email verification and password reset** flows.
- **Dark mode and responsive redesign** for better mobile usability.
- **CSV export/import** for calorie history backups.

## License

This project is licensed under the MIT License.

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contact

This README includes placeholder contact information. Replace the values below with your own project maintainer details before publishing the repository.

- **Project Maintainer:** Mehedi Alam
- **Email:** mehedialam806@gmail.com
- **Repository:** https://github.com/mehedialam49/Django-Calorie-Counter-Project-using-HTML-form
- **Project Link:** https://github.com/mehedialam49/Django-Calorie-Counter-Project-using-HTML-form

Back to [Contents](#contents)
