# ===== Base image =====
FROM python:3.12-slim

# ===== System settings =====
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ===== Workdir =====
WORKDIR /app

# ===== Install dependencies =====
# Ja Tev ir requirements.txt — tas tiks izmantots
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ===== Copy project files =====
COPY . /app

# ===== Expose port =====
EXPOSE 5000

# ===== Run application =====
CMD ["python", "app.py"]