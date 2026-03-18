# RecipEasy

## Overview

RecipEasy is a student-focused recipe web application built with Django. Anyone can browse and search recipes, but logged-in users can contribute and interact with the community by uploading recipes, saving favourites, rating recipes (1–5 stars), and leaving comments.

The app is designed around quick, practical cooking for students — helping users discover reliable meals, keep a personal collection of saved recipes, and use community feedback (ratings/comments) to find the best options.

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS + Bootstrap, JavaScript
- **Database:** SQLite (Django ORM)

## Local Setup

To run RecipEasy locally, follow the steps below. Please make sure you have Python 3.11 installed.

1. **Clone the repository**

```bash
git clone https://github.com/ismailsalim067/recipeasy.git
cd recipeasy
```

2. **Create a virtual environment**

**macOS/Linux**
```bash
python3 -m venv .venv
```

**Windows**
```bash
py -m venv .venv
```

3. **Activate the virtual environment**  
You’ll need to do this each time you reopen the project.

**macOS/Linux**
```bash
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
.\.venv\Scripts\Activate.ps1
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Run the server**

```bash
python manage.py runserver
```

To run tests:

```bash
python manage.py test
```

Open in browser:

```text
http://127.0.0.1:8000
```

## Git Workflow

Our `main` branch is protected. Changes should be made on a separate branch and merged via a Pull Request (PR) with **1 approval**.

### How to build a feature

1. **Create a new branch for your task**  
   Choose a short, descriptive name (e.g. `feature/recipe-search`, `fix/login-form`).

```bash
git checkout main
git pull
git checkout -b feature/your-branch-name
```

2. **Make your changes and commit regularly**

```bash
git add .
git commit -m "Short description of what you changed"
```

3. **Push your branch to GitHub**

```bash
git push -u origin feature/your-branch-name
```

4. **Open a Pull Request**  
   Open a PR from your branch to `main`. Request a teammate to review and approve your code before merging. When merging, choose **Squash and merge**.

## Acknowledgements & External Sources

To be updated — we will list any code snippets, and image sources etc used during development.
