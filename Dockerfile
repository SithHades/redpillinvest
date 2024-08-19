FROM python:3.12

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
# Make sure the script is executable
RUN chmod +x /entrypoint.sh

# Copy the rest of the application
COPY . .

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command

CMD ["gunicorn", "redpillinvest.wsgi:application", "--bind", "0.0.0.0:8000"]