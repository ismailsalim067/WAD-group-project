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

1) Clone the repository

git clone https://github.com/ismailsalim067/recipeasy.git
cd recipeasy

2) Create a virtual environment

**macOS/Linux**
python3 -m venv .venv

**Windows**
py -m venv .venv

3) Activate the virtual environment  
You’ll need to do this each time you reopen the project.

**macOS/Linux**
source .venv/bin/activate

**Windows(Powershell)**
.\.venv\Scripts\Activate.ps1

4) Install dependencies

pip install -r requirements.txt

5) Run the server

python manage.py migrate
python manage.py runserver

To run tests:
python manage.py test

Open: http://127.0.0.1:8000

## Git Workflow

Our `main` branch is protected. Changes should be made on a separate branch and merged via a Pull Request (PR) with **1 approval**.

### How to build a feature

1) Create a new branch for your task  
Choose a short, descriptive name (e.g., `feature/recipe-search`, `fix/login-form`).

git checkout main
git pull
git checkout -b feature/<branch-name>

2) Make your changes and commit regularly

git add . 
git commit -m "Quick description of what you changed"

3) Push your branch to GitHub

git push -u origin feature/<branch-name>

4) Open a PR from your branch -> main
   Request a teammate to review and approve your code before merging it into the main branch.
   When merging, choose **Squash and merge**

## Acknowledgements & External Sources

To be updated — we will list any code snippets, and image sources etc used during development.
