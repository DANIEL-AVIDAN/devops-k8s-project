# 🐳 Python Microservice with Docker

A simple Python microservice running inside a Docker container.

The application starts an HTTP server and listens on a configurable port.
The port is provided through the `APP_PORT` environment variable.

By default, this project uses **port 8000**.

---

## 📋 Project Overview

This project demonstrates how to:

- Create a simple Python HTTP microservice
- Configure the application using environment variables
- Containerize the application using Docker
- Build a Docker image
- Run the application inside a Docker container
- Pass environment variables to a Docker container using a `.env` file
- Access the microservice through an HTTP request

---

## 📁 Project Structure

```text
.
├── .env
├── .gitignore
├── app.py
├── Dockerfile
└── README.md
```

> The `.env` file is used locally and should not be committed to Git.

---

## ⚙️ Prerequisites

Before running the project, make sure Docker is installed and running.

Verify your Docker installation:

```bash
docker --version
```

---

## 🔐 Environment Variables

The application uses an environment variable called:

```text
APP_PORT
```

Create a file named `.env` in the root directory of the project:

```text
.
├── .env
├── app.py
├── Dockerfile
└── README.md
```

Add the following content to the `.env` file:

```env
APP_PORT=8000
```

The Python application reads `APP_PORT` and starts the HTTP server on that port.

---

## 🚫 Git Ignore

The `.env` file should not be committed to the Git repository.

Add the following line to your `.gitignore` file:

```gitignore
.env
```

This prevents Git from tracking the local environment configuration.

> Environment files may contain sensitive configuration in real-world projects, so they should generally not be committed to source control.

---

## 🔨 Build the Docker Image

From the project directory, run:

```bash
docker build -t tiny-python-app .
```

This command:

1. Reads the `Dockerfile`
2. Downloads the Python base image if necessary
3. Copies the Python application into the image
4. Creates a Docker image named `tiny-python-app`

You can verify that the image was created with:

```bash
docker images
```

---

## ▶️ Run the Microservice

Run the container and provide the environment variables from the `.env` file:

```bash
docker run --rm --env-file .env -p 8000:8000 tiny-python-app
```

### Command Explanation

```text
docker run
```

Starts a new container from the Docker image.

```text
--rm
```

Automatically removes the container after it stops.

```text
--env-file .env
```

Reads environment variables from the `.env` file and passes them into the container.

In this project, it provides:

```text
APP_PORT=8000
```

to the Python application.

```text
-p 8000:8000
```

Maps port `8000` on the host machine to port `8000` inside the Docker container.

```text
tiny-python-app
```

Specifies the Docker image that should be used.

---

## 🌐 Access the Application

Once the container is running, the microservice is available at:

```text
http://localhost:8000
```

You can open this address in your browser.

You can also test it from another terminal using:

```bash
curl http://localhost:8000
```

Expected response:

```text
Hello from the Python microservice!
```

---

## 🐍 Application

The Python application creates a small HTTP server.

```python
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = "Hello from the Python microservice!"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))


def main():
    port = int(os.getenv("APP_PORT", "8000"))

    server = HTTPServer(("0.0.0.0", port), RequestHandler)

    print(f"Microservice is listening on port {port}", flush=True)

    server.serve_forever()


if __name__ == "__main__":
    main()
```

The application does not terminate after printing a message.

Instead, it keeps running and listens for incoming HTTP requests on the configured port.

---

## 🐳 Dockerfile

The application is containerized using the following Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

EXPOSE 8000

CMD ["python", "-u", "app.py"]
```

### Dockerfile Explanation

| Instruction | Description |
|---|---|
| `FROM python:3.12-slim` | Uses the lightweight official Python 3.12 image as the base image. |
| `WORKDIR /app` | Sets `/app` as the working directory inside the container. |
| `COPY app.py .` | Copies the Python application into the container. |
| `EXPOSE 8000` | Documents that the application is expected to listen on port 8000. |
| `CMD` | Starts the Python microservice when the container starts. |

---

## 🔄 Application Flow

The complete flow looks like this:

```text
.env
  │
  │ APP_PORT=8000
  ▼
Docker Container
  │
  ▼
Python Application
  │
  │ listens on port 8000
  ▼
HTTP Server
  ▲
  │
  │ GET /
  │
Browser / curl
```

When a request is received, the microservice responds with:

```text
Hello from the Python microservice!
```

---

## 🧪 Useful Docker Commands

### Build the image

```bash
docker build -t tiny-python-app .
```

### Run the container

```bash
docker run --rm --env-file .env -p 8000:8000 tiny-python-app
```

### Test the application

```bash
curl http://localhost:8000
```

### List running containers

```bash
docker ps
```

### List all containers

```bash
docker ps -a
```

### List Docker images

```bash
docker images
```

### Stop a container

```bash
docker stop <container_id>
```

### Remove the image

```bash
docker rmi tiny-python-app
```

---

## 🎯 Learning Objectives

This project demonstrates several important DevOps concepts:

- Building a simple microservice
- Running an HTTP service inside a container
- Creating Docker images
- Running Docker containers
- Exposing application ports
- Mapping host and container ports
- Using environment variables for application configuration
- Using `.env` files with Docker
- Keeping environment-specific configuration outside the application source code
