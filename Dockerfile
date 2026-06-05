# Dockfile for this DJango project using non-root user

FROM python:3.12-slim

WORKDIR /app

# Create a non-root user
RUN useradd -m -u 1000 appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change ownership of /app to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 8000

ENTRYPOINT [ "python3" ]

CMD ["manage.py", "runserver", "0.0.0.0:8000"]