# 🐳 Python Microservice with Docker, Helm & Kubernetes

A simple Python HTTP microservice packaged as a Docker image and deployed to Kubernetes using Helm.

This project is intended for learning and demonstrates the basic flow from application code to a running Kubernetes workload.

The application listens on a configurable port using the `APP_PORT` environment variable.

---

## 📋 Project Overview

This project demonstrates how to:

- Create a simple Python HTTP microservice
- Configure the application using environment variables
- Containerize the application with Docker
- Build and run a Docker image locally
- Push the image to Docker Hub
- Deploy the application to Kubernetes
- Use Helm templates and `values.yaml`
- Run multiple replicas of the application
- Expose the Pods through a Kubernetes Service
- Test the deployment locally with Minikube

---

## 📁 Project Structure

```text
.
├── .env
├── .gitignore
├── app.py
├── Dockerfile
├── README.md
└── chart/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── _helpers.tpl
        ├── deployment.yaml
        └── service.yaml
```

> `.env` is used only for local Docker execution and should not be committed to Git.

---

# 🐍 Python Application

The application runs a small HTTP server and stays active while waiting for incoming requests.

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

The application does **not** terminate after printing a message.

It continues running and listens for HTTP requests.

---

# 🔐 Local Environment Configuration

Create a `.env` file in the project root:

```env
APP_PORT=8000
```

Add `.env` to `.gitignore`:

```gitignore
.env
```

This prevents the local environment configuration from being committed to Git.

---

# 🐳 Docker

## Build the Docker Image

From the project root:

```bash
docker build -t tiny-python-app .
```

Verify that the image was created:

```bash
docker images
```

---

## Run Locally with Docker

Run the container and load the environment variables from `.env`:

```bash
docker run --rm --env-file .env -p 8000:8000 tiny-python-app
```

### Command Explanation

| Option | Description |
|---|---|
| `--rm` | Removes the container automatically after it stops |
| `--env-file .env` | Loads environment variables from `.env` |
| `-p 8000:8000` | Maps host port 8000 to container port 8000 |
| `tiny-python-app` | Name of the Docker image |

Test the application:

```bash
curl http://localhost:8000
```

Expected response:

```text
Hello from the Python microservice!
```

You can also open the application in a browser:

```text
http://localhost:8000
```

---

# ☁️ Docker Hub

The Kubernetes deployment uses the following Docker image:

```text
danielavidan/tiny-python-app:latest
```

## Login to Docker Hub

```bash
docker login
```

## Tag the Local Image

```bash
docker tag tiny-python-app:latest danielavidan/tiny-python-app:latest
```

## Push the Image

```bash
docker push danielavidan/tiny-python-app:latest
```

Optionally, verify that the image can be pulled:

```bash
docker pull danielavidan/tiny-python-app:latest
```

---

# ☸️ Kubernetes & Helm

The application is deployed to Kubernetes using a Helm chart.

The Helm chart contains:

```text
chart/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── _helpers.tpl
    ├── deployment.yaml
    └── service.yaml
```

---

## Helm Values

Example `values.yaml`:

```yaml
deployment:
  app: web-server
  replicas: 2

pod:
  image: danielavidan/tiny-python-app
  tag: latest
  target_port: 8000
  port: 8000

service:
  service_type: ClusterIP
```

This configuration tells Helm to:

- Run **2 replicas** of the application
- Use `danielavidan/tiny-python-app:latest`
- Configure the application to listen on port `8000`
- Expose port `8000` through the Kubernetes Service
- Create a Service of type `ClusterIP`

---

# 🔐 APP_PORT in Kubernetes

When running the application directly with Docker, `APP_PORT` comes from the local `.env` file:

```env
APP_PORT=8000
```

Kubernetes does **not** automatically read the local `.env` file.

Instead, the Helm Deployment passes the value from `values.yaml` into the container.

The Deployment template contains:

```yaml
env:
  - name: APP_PORT
    value: {{ .Values.pod.target_port | quote }}
```

Helm reads:

```yaml
target_port: 8000
```

from `values.yaml`.

After Helm renders the template, Kubernetes receives something similar to:

```yaml
env:
  - name: APP_PORT
    value: "8000"
```

The Python application then reads the environment variable using:

```python
os.getenv("APP_PORT")
```

The flow is:

```text
values.yaml
     │
     │ target_port: 8000
     ▼
Helm Template
     │
     ▼
Deployment
     │
     │ APP_PORT="8000"
     ▼
Container
     │
     ▼
app.py
     │
     ▼
HTTP Server :8000
```

---

# 🚀 Helm Deployment

The important container configuration inside `deployment.yaml` is:

```yaml
containers:
  - name: {{ .Release.Name }}
    image: {{ .Values.pod.image }}:{{ .Values.pod.tag }}

    env:
      - name: APP_PORT
        value: {{ .Values.pod.target_port | quote }}

    ports:
      - containerPort: {{ .Values.pod.target_port }}
```

There are two different port-related configurations here.

### Environment Variable

```yaml
env:
  - name: APP_PORT
    value: {{ .Values.pod.target_port | quote }}
```

This passes the port to the Python application.

### Container Port

```yaml
ports:
  - containerPort: {{ .Values.pod.target_port }}
```

This tells Kubernetes which port the container is expected to listen on.

---

# 🌐 Kubernetes Service

The Helm chart also creates a Kubernetes Service.

The Service uses:

```yaml
service_type: ClusterIP
```

The Service forwards traffic to the application Pods.

Conceptually:

```text
               Kubernetes Service
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
          Pod #1             Pod #2
       Python :8000       Python :8000
```

The Deployment maintains the Pods, while the Service provides a stable network endpoint for reaching them.

---

# 🧪 Running Locally with Minikube

## Start Minikube

```bash
minikube start
```

Verify that Kubernetes is available:

```bash
kubectl get nodes
```

You should see the Minikube node in a `Ready` state.

---

# 🔍 Validate the Helm Chart

Move into the Helm chart directory:

```bash
cd chart
```

Before installing the application, validate the chart:

```bash
helm lint .
```

You can also render the Kubernetes manifests without installing them:

```bash
helm upgrade --install my-app . --dry-run
```

This is useful for seeing exactly what YAML Helm generates from the templates.

For example:

```text
values.yaml
     │
     ▼
Helm Templates
     │
     ▼
Rendered Kubernetes YAML
```

No Kubernetes resources are actually created when using `--dry-run`.

---

# 🚀 Install the Application with Helm

From the `chart` directory:

```bash
helm upgrade --install my-app .
```

This command works for both the first installation and future upgrades.

If the release does not exist, Helm installs it.

If the release already exists, Helm upgrades it.

The release name is:

```text
my-app
```

---

# ✅ Verify the Deployment

Check installed Helm releases:

```bash
helm list
```

Check the Deployment:

```bash
kubectl get deployments
```

Check the Pods:

```bash
kubectl get pods
```

Because `values.yaml` contains:

```yaml
replicas: 2
```

you should see two application Pods.

Example:

```text
NAME                      READY   STATUS    RESTARTS   AGE
my-app-xxxxxxxxxx-aaaaa   1/1     Running   0          1m
my-app-xxxxxxxxxx-bbbbb   1/1     Running   0          1m
```

Check the Kubernetes Service:

```bash
kubectl get services
```

The Service created by the chart is:

```text
my-app-svc
```

---

# 🌐 Access the Application from Minikube

The Service is currently configured as:

```yaml
service_type: ClusterIP
```

A `ClusterIP` Service is normally accessible only from inside the Kubernetes cluster.

For local testing, use Kubernetes port forwarding:

```bash
kubectl port-forward service/my-app-svc 8000:8000
```

Keep that terminal open.

Then open another terminal and run:

```bash
curl http://localhost:8000
```

Expected response:

```text
Hello from the Python microservice!
```

You can also open:

```text
http://localhost:8000
```

in your browser.

---

# 🔎 Useful Kubernetes Commands

## List Pods

```bash
kubectl get pods
```

## List Deployments

```bash
kubectl get deployments
```

## List Services

```bash
kubectl get services
```

## Get More Information About a Pod

```bash
kubectl describe pod <pod-name>
```

This is especially useful when troubleshooting issues such as:

```text
ImagePullBackOff
ErrImagePull
CrashLoopBackOff
```

---

## View Application Logs

```bash
kubectl logs <pod-name>
```

Follow the logs continuously:

```bash
kubectl logs -f <pod-name>
```

---

## Check APP_PORT Inside a Pod

```bash
kubectl exec <pod-name> -- printenv APP_PORT
```

Expected output:

```text
8000
```

This confirms that Helm/Kubernetes successfully passed the environment variable into the container.

---

# 🔄 Updating the Application

If the Python application changes, rebuild the Docker image:

```bash
docker build -t tiny-python-app .
```

Tag it:

```bash
docker tag tiny-python-app:latest danielavidan/tiny-python-app:latest
```

Push the updated image:

```bash
docker push danielavidan/tiny-python-app:latest
```

Then upgrade the Helm release:

```bash
cd chart
helm upgrade --install my-app .
```

> This project currently uses the `latest` image tag for learning purposes. In production environments, versioned tags such as `v1.0.0`, `v1.1.0`, etc. are generally preferred.

---

# 🗑️ Uninstall the Application

Remove the Helm release:

```bash
helm uninstall my-app
```

Verify that the resources were removed:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

---

# 🛑 Stop Minikube

Stop the local Kubernetes cluster:

```bash
minikube stop
```

If you want to completely delete the Minikube cluster:

```bash
minikube delete
```

---

# 🔄 End-to-End Project Flow

The complete project flow is:

```text
        app.py
           │
           ▼
      Dockerfile
           │
           │ docker build
           ▼
      Docker Image
           │
           │ docker push
           ▼
      Docker Hub
danielavidan/tiny-python-app
           │
           ▼
      values.yaml
           │
           ▼
      Helm Templates
           │
           │ helm upgrade --install
           ▼
   Kubernetes Deployment
           │
           ▼
      ┌───────────┐
      │           │
      ▼           ▼
    Pod #1      Pod #2
      │           │
      └─────┬─────┘
            │
            ▼
     Kubernetes Service
        my-app-svc
            │
            │ kubectl port-forward
            ▼
    http://localhost:8000
            │
            ▼
Hello from the Python microservice!
```

---

# 🎯 Learning Objectives

This project demonstrates:

- Building a Python microservice
- Creating a persistent HTTP server
- Working with application ports
- Using environment variables
- Using `.env` files for local configuration
- Containerizing applications with Docker
- Building Docker images
- Running Docker containers
- Publishing Docker images to Docker Hub
- Running workloads on Kubernetes
- Creating Kubernetes Deployments
- Running multiple Pod replicas
- Creating Kubernetes Services
- Understanding `ClusterIP`
- Using Helm charts
- Using Helm templates
- Using `values.yaml`
- Passing configuration from Helm into containers
- Testing Helm charts with `--dry-run`
- Deploying applications with `helm upgrade --install`
- Testing Kubernetes applications locally with Minikube
- Using `kubectl` for inspection and troubleshooting

---

# 📄 License

This project is intended for educational purposes.