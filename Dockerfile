# Pull base image
FROM python:3.11-alpine

# Set working directory
WORKDIR /

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY Pipfile Pipfile.lock /
RUN pip install pipenv && pipenv install --system --deploy && pip cache purge

# Copy source code
COPY . /

# Run the application
CMD ["python3", "main.py"]
