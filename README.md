# devops-k8s-project

# 🐳 Containerized Python Application

A minimal Python web application running inside a Docker container.

The application listens on **port 8000** and returns a simple message whenever it receives an HTTP request.

---

# 📋 Project Overview

This project demonstrates how to:

- Create a simple Python web application
- Containerize the application using Docker
- Build a Docker image
- Run the application inside a Docker container
- Access the application through a web browser or using `curl`

---

# 📁 Project Structure

```text
.
├── app.py
├── Dockerfile
├── README.md
└── requirements.txt
```

---

# ⚙️ Prerequisites

Before running the project, make sure you have:

- Docker installed
- Docker Engine running

Verify your installation:

```bash
docker --version
```

---

# 🚀 Quick Start

## Build the Docker image

```bash
docker build -t tiny-python-app .
```

## Run the container

```bash
docker run -p 8000:8000 --rm tiny-python-app
```

The application will now be available at:

```
http://localhost:8000
```

---

# 🌐 Test the Application

### Using a browser

Open:

```
http://localhost:8000
```

### Using curl

```bash
curl http://localhost:8000
```

Expected response:

```text
Hello from a tiny Python app running in Docker!
```

---

# 🐳 Dockerfile Explanation

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
```

| Instruction | Description |
|------------|-------------|
| `FROM` | Uses the official lightweight Python 3.12 image as the base image. |
| `WORKDIR` | Sets `/app` as the working directory inside the container. |
| `COPY` | Copies the application into the container. |
| `EXPOSE 8000` | Documents that the application listens on port **8000**. |
| `CMD` | Starts the Python web server when the container runs. |

---

# 🖥️ Application Behavior

The application:

- Starts an HTTP server
- Listens on **port 8000**
- Waits for incoming HTTP requests
- Returns the following message for every request:

```text
Hello from a tiny Python app running in Docker!
```

---

# 📦 Docker Commands

Build the image:

```bash
docker build -t tiny-python-app .
```

Run the container:

```bash
docker run -p 8000:8000 --rm tiny-python-app
```

List local images:

```bash
docker images
```

List running containers:

```bash
docker ps
```

List all containers:

```bash
docker ps -a
```

Stop a running container:

```bash
docker stop <container_id>
```

Remove the Docker image:

```bash
docker rmi tiny-python-app
```

---
