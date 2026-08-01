# devops-k8s-project

# 🐳 Minimal Python Docker Example

A tiny example showing how to package a simple Python application into a Docker image.

## 🚀 Features

- Minimal Python application
- Lightweight Docker image (`python:3.12-slim`)
- Easy to build and run
- Great starting point for Docker beginners

---

## 📁 Project Structure

```text
.
├── app.py
├── Dockerfile
└── README.md
```

---

## 📋 Prerequisites

Before you begin, make sure you have:

- Docker installed
- Docker daemon running

Verify your installation:

```bash
docker --version
```

---

## 🔨 Build the Docker Image

Run the following command from the project directory:

```bash
docker build -t tiny-python-app .
```

This command:

- Reads the `Dockerfile`
- Downloads the base image (if necessary)
- Copies the application into the image
- Creates a Docker image named `tiny-python-app`

---

## ▶️ Run the Container

```bash
docker run --rm tiny-python-app
```

Expected output:

```text
Hello from a tiny Python app running in Docker!
```

The `--rm` flag automatically removes the container after it exits.

---

## 🐳 Dockerfile Explained

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

| Instruction | Description |
|------------|-------------|
| `FROM` | Uses the official lightweight Python 3.12 image as the base image. |
| `WORKDIR` | Sets `/app` as the working directory inside the container. |
| `COPY` | Copies the application file into the container. |
| `CMD` | Executes the Python application when the container starts. |

---

## 📂 Project Files

### `app.py`

```python
def main():
    print("Hello from a tiny Python app running in Docker!")

if __name__ == "__main__":
    main()
```

This is a minimal Python application used to demonstrate how Docker packages and runs Python code.

---

## 🧹 Clean Up

To remove the Docker image:

```bash
docker rmi tiny-python-app
```

---

## 🎯 Learning Goals

This project demonstrates:

- Creating a simple Python application
- Writing a basic Dockerfile
- Building Docker images
- Running Docker containers
- Understanding the purpose of common Dockerfile instructions

---

## 📚 Useful Docker Commands

Build the image:

```bash
docker build -t tiny-python-app .
```

Run the container:

```bash
docker run --rm tiny-python-app
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

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, consider giving it a star!