#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="/root/.local/bin:$PATH"

# Configure Poetry
poetry config virtualenvs.create false

# Install dependencies
poetry install --no-interaction --no-ansi --no-root

# Django commands
python manage.py collectstatic --no-input
python manage.py migrate
