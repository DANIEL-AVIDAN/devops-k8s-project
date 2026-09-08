# FROM python:3.12-slim

# WORKDIR /app

# COPY app.py .

# EXPOSE 8000

# CMD ["python", "-u", "app.py"]

FROM nginx:alpine
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]