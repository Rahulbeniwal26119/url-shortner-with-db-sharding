FROM python:3.12.4-slim

WORKDIR /app

COPY ./requirements.txt /app
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
