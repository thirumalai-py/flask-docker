# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install pytest for testing
RUN pip install pytest

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create a script to run tests or the application
RUN echo '#!/bin/bash\n\
if [ "$RUN_TESTS" = "true" ]; then\n\
    pytest\n\
else\n\
    flask run\n\
fi' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Run app.py when the container launches
CMD ["/app/entrypoint.sh"]

