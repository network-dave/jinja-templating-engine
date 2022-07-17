# Let's use the official Python image
FROM python:3.10-slim-bullseye

# Set the working directory inside the image
WORKDIR /app

# Copy the necessary application files
COPY app.py requirements.txt ./

# Create the templates folder and copy the example template
COPY ./templates/ templates/

# Install the necessary Python packages
RUN pip install -r requirements.txt

# Provide your own templates by mounting your local templates folder and overwrite /app/templates in the container instance
# docker run --name jinja-templating-engine -v $(pwd)/templates:/app/templates -p 80:80 -d jinja-templating-engine:latest

# Allow requests from other containers on port 80
EXPOSE 80

# Run the web application (debug mode)
CMD ["python3", "/app/app.py"]