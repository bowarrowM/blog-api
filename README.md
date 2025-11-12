# Beginner Friendly Blogging Platform API

A RESTful API built with Django and Django REST Framework for managing a personal blog. 
This project demonstrates fundamental CRUD operations, database relationships, filtering, and API best practices.

This project was  built to teach developers with no backend experience start their journey. Comments were added throughout the project as guidance.
Main files to focus on:

/config/settings.py
/config/urls.py

/blog/models.py
/blog/serializers.py
/blog/urls.py
/blog/admin.py
/blog/views.py

important mention:
"""project-root/.env"""

File is gitignored for safety reasons. Creating and utilizing one is best practice.

## Project Overview

This API provides a complete backend solution for a blogging platform with the following capabilities:

- Create, read, update, and delete blog articles
- Tag system for categorizing articles
- Filter articles by status, author, tags, and date
- Search functionality across titles and content
- Draft and publish workflow
- Built-in admin panel for content management
- RESTful API design with proper HTTP methods

## Tech Stack

- **Backend Framework**: Django 
- **API Framework**: Django REST Framework 
- **Database**: PostgreSQL
- **Additional Libraries**:
  - `psycopg2-binary` - PostgreSQL adapter
  - `django-cors-headers` - CORS support
  - `python-decouple` - Environment variable management
  - `django-filter` - Advanced filtering

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)
- virtualenv (highly recommended)


