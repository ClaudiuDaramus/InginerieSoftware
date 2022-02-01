FROM python:3.10-slim-bullseye

# flags
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# pip and dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y build-essential libpq-dev &&  rm -rf /var/lib/apt/lists/*

# install env
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && pipenv install --system

# Create and switch to a new user
RUN useradd -U django_admin
COPY --chown=django_admin:django_admin scripts/run_app.sh /bin/run_app.sh
WORKDIR /app
USER django_admin:django_admin
COPY --chown=django_admin:django_admin /source .
RUN chmod +x /bin/run_app.sh
USER django_admin
