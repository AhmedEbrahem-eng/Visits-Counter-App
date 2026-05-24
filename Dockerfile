FROM python:3.12-alpine

# Set env options to optimize Python container execution
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies before copying source code to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root system user and group for security compliance
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy application files and grant ownership to non-root user
COPY --chown=appuser:appgroup . .

# Switch container context to non-root user
USER appuser

EXPOSE 5000

# Start with Gunicorn WSGI server in production mode
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--log-level", "info", "run:app"]
