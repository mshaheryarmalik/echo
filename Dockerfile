# Use the official Python 3.10.12 image from Docker Hub
FROM python:3.10.12-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer output for easier debugging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app into the container
COPY . /app/

# Collect static files (if using Django with static files)
RUN python echoapp/manage.py collectstatic --noinput

# Expose the port the app will run on
EXPOSE 8000

# Set the command to run the app with Gunicorn (or use `python manage.py runserver` for dev)
CMD ["gunicorn", "echoapp.wsgi:application", "--bind", "0.0.0.0:8000"]
