# 🐳 Python Microservice with Docker, Helm, Kubernetes & Ingress

A simple Python HTTP microservice packaged as a Docker image and deployed to Kubernetes using Helm.

This project is intended for learning and demonstrates the flow from application code to a running Kubernetes workload that is exposed through a Kubernetes **Ingress**.

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
- Expose Pods through a Kubernetes `ClusterIP` Service
- Route external HTTP traffic through a Kubernetes Ingress
- Use an Ingress Controller
- Use `nip.io` for a convenient local hostname
- Access the Ingress locally with Minikube
- Understand the difference between Ingress access and `kubectl port-forward`

---

## 🧭 Application Architecture

The main Kubernetes request flow is:

```text
Browser
   |
   | HTTP :80
   v
Ingress Controller
   |
   | reads the Ingress routing rules
   v
my-app-svc :8000
   |
   | ClusterIP Service
   v
Application Pods :8000
```

The important distinction is:

- **Ingress** — defines HTTP routing rules.
- **Ingress Controller** — receives the actual HTTP traffic and applies the Ingress rules.
- **Service** — provides a stable internal endpoint for the application Pods.
- **Pods** — run the Python application.

The application itself does not need to listen on port `80`.

The Ingress Controller accepts the external HTTP request on port `80` and forwards it to the Service on port `8000`.

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
        ├── service.yaml
        └── ingress.yaml
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

You can also open:

```text
http://localhost:8000
```

in a browser.

---

# ☁️ Docker Hub

The Kubernetes Deployment uses the following Docker image:

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

The chart creates the main Kubernetes resources:

```text
Helm Release
    |
    +-- Deployment
    |      |
    |      +-- Pod #1
    |      +-- Pod #2
    |
    +-- Service (ClusterIP)
    |
    +-- Ingress
```

The Deployment manages the application Pods.

The Service provides a stable internal endpoint for those Pods.

The Ingress defines how HTTP traffic entering the cluster should be routed to the Service.

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
     |
     | target_port: 8000
     v
Helm Template
     |
     v
Deployment
     |
     | APP_PORT="8000"
     v
Container
     |
     v
app.py
     |
     v
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

This documents the port that the container is expected to listen on.

---

# 🌐 Kubernetes Service

The Helm chart creates a Kubernetes Service named:

```text
my-app-svc
```

The Service uses:

```yaml
service_type: ClusterIP
```

A `ClusterIP` Service is internal to the Kubernetes cluster.

It provides a stable endpoint for a dynamic group of Pods:

```text
              my-app-svc :8000
                     |
             +-------+-------+
             |               |
             v               v
          Pod #1           Pod #2
       Python :8000     Python :8000
```

The Service does **not** need to be changed to `LoadBalancer` when it is used behind an Ingress.

The Ingress Controller runs inside the cluster and can reach the `ClusterIP` Service directly.

---

# 🌍 Kubernetes Ingress

The project also contains an `Ingress` resource.

Ingress defines HTTP routing rules such as:

```text
Host: myapp.127.0.0.1.nip.io
Path: /
              |
              v
      my-app-svc:8000
```

Conceptually:

```text
Request
http://myapp.127.0.0.1.nip.io/
              |
              v
      Ingress Controller
              |
              | host matches
              | path starts with /
              v
        my-app-svc:8000
              |
              v
        Application Pod
```

An Ingress resource is **configuration**. It does not receive network traffic by itself.

An **Ingress Controller** watches the Kubernetes API, reads the Ingress rules and performs the actual reverse-proxy routing.

For this project, the Minikube Ingress addon is used.

A simplified Ingress resource looks like:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress

metadata:
  name: my-ingress

spec:
  ingressClassName: nginx

  rules:
    - host: myapp.127.0.0.1.nip.io
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-app-svc
                port:
                  number: 8000
```

`path: /` with `pathType: Prefix` means that every path under this hostname can be routed to the same Service.

For example:

```text
/
/hello
/users
/api/items
```

all match the `/` prefix.

---

# 🔤 Why `nip.io`?

For local development, it is useful to have a hostname without buying or configuring a real domain.

`nip.io` provides DNS names that resolve to the IP address embedded in the hostname.

For example:

```text
myapp.127.0.0.1.nip.io
```

resolves to:

```text
127.0.0.1
```

This allows the Ingress rule to use a realistic hostname while still running locally.

The hostname also matters to the Ingress Controller because HTTP requests contain a `Host` header.

The host in the request must match the host configured in the Ingress rule.

---

# 🧪 Running Locally with Minikube

## 1. Start Minikube

```bash
minikube start
```

Verify that Kubernetes is available:

```bash
kubectl get nodes
```

The Minikube node should be in the `Ready` state.

---

## 2. Enable the Ingress Controller

Enable the Minikube Ingress addon:

```bash
minikube addons enable ingress
```

You can verify that the addon is enabled with:

```bash
minikube addons list
```

You can also inspect the Ingress Controller Pods:

```bash
kubectl get pods -n ingress-nginx
```

---

# 🔍 Validate the Helm Chart

Move into the Helm chart directory:

```bash
cd chart
```

Validate the chart:

```bash
helm lint .
```

Render the Kubernetes manifests without installing them:

```bash
helm upgrade --install my-app . --dry-run
```

This is useful for seeing exactly what YAML Helm generates from the templates:

```text
values.yaml
     |
     v
Helm Templates
     |
     v
Rendered Kubernetes YAML
```

No Kubernetes resources are created when using `--dry-run`.

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

Check the Ingress:

```bash
kubectl get ingress
```

For more details:

```bash
kubectl describe ingress my-ingress
```

---

# 🚇 Access the Application with `minikube tunnel`

When Minikube runs through Docker Desktop, the Kubernetes network is separated from the host machine.

The application Service is intentionally a `ClusterIP`, so it is not directly exposed to the laptop.

The Ingress Controller is the entry point that should receive the HTTP request.

For local access, open a **separate terminal** and run:

```bash
minikube tunnel
```

The command may ask for administrator privileges because it needs to configure local networking.

Keep this terminal open while accessing the application.

Conceptually, the local flow becomes:

```text
Browser
   |
   | http://myapp.127.0.0.1.nip.io
   | HTTP port 80
   v
Host machine
   |
   | network path provided by Minikube
   v
Ingress Controller
   |
   | Ingress rule
   v
my-app-svc :8000
   |
   v
Application Pod :8000
```

Now test the application:

```bash
curl http://myapp.127.0.0.1.nip.io
```

Expected response:

```text
Hello from the Python microservice!
```

You can also open:

```text
http://myapp.127.0.0.1.nip.io
```

in a browser.

Because the URL uses normal HTTP without an explicit port, the browser connects on port `80`.

The Ingress Controller then forwards the request internally to:

```text
my-app-svc:8000
```

The Service forwards it to one of the application Pods listening on port `8000`.

---

## Using the Minikube IP Instead

On environments where the Minikube node IP is directly reachable from the host, the Ingress hostname can instead contain the Minikube IP.

Get the IP with:

```bash
minikube ip
```

For example:

```text
192.168.49.2
```

A matching `nip.io` hostname would be:

```text
myapp.192.168.49.2.nip.io
```

In that case, the host configured in `ingress.yaml` must match the hostname used in the request.

For Docker Desktop setups where the Minikube node IP is not directly reachable from the host, use the tunnel approach with `127.0.0.1`.

---

# 🔌 `port-forward` vs Ingress

Before adding Ingress, the application could be tested using:

```bash
kubectl port-forward service/my-app-svc 8000:8000
```

That creates a temporary direct path from the laptop to the Service:

```text
Browser
   |
localhost:8000
   |
kubectl port-forward
   |
   v
my-app-svc:8000
   |
   v
Pod:8000
```

This **bypasses the Ingress completely**.

It is still useful for debugging because it can help determine whether the Service and Pods are working independently of the Ingress.

For normal testing of the complete architecture, use:

```text
Browser
   |
   v
Ingress Controller
   |
   v
Service
   |
   v
Pod
```

So:

- `kubectl port-forward` = direct temporary debugging access to a resource
- `minikube tunnel` = enables host-to-Minukube network access needed by the local setup
- `Ingress` = defines HTTP routing rules
- `Ingress Controller` = receives requests and applies those routing rules

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

## List Ingress Resources

```bash
kubectl get ingress
```

## Inspect the Ingress

```bash
kubectl describe ingress my-ingress
```

## Inspect the Ingress Controller

```bash
kubectl get pods -n ingress-nginx
kubectl get services -n ingress-nginx
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

## Check `APP_PORT` Inside a Pod

```bash
kubectl exec <pod-name> -- printenv APP_PORT
```

Expected output:

```text
8000
```

This confirms that Helm/Kubernetes successfully passed the environment variable into the container.

---

# 🛠️ Troubleshooting the Request Path

If the application is not reachable through the Ingress, validate each layer separately.

### 1. Are the Pods running?

```bash
kubectl get pods
```

### 2. Does the Service exist?

```bash
kubectl get service my-app-svc
```

### 3. Does the Service point to healthy Pods?

```bash
kubectl get endpoints my-app-svc
```

### 4. Does direct Service access work?

For debugging only:

```bash
kubectl port-forward service/my-app-svc 8000:8000
```

Then:

```bash
curl http://localhost:8000
```

If this works, the application, Pods and Service are probably healthy.

### 5. Does the Ingress exist?

```bash
kubectl get ingress
kubectl describe ingress my-ingress
```

### 6. Is the Ingress Controller running?

```bash
kubectl get pods -n ingress-nginx
```

### 7. Is the local tunnel running?

```bash
minikube tunnel
```

### 8. Does the hostname match the Ingress rule?

For the tunnel-based setup, verify that both the Ingress and request use:

```text
myapp.127.0.0.1.nip.io
```

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

Verify that the application resources were removed:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get ingress
```

The Minikube Ingress Controller belongs to the Minikube addon, not to the Helm release, so uninstalling the application does not remove the controller itself.

---

# 🛑 Stop Minikube

Stop the local Kubernetes cluster:

```bash
minikube stop
```

If `minikube tunnel` is running, stop it with:

```text
Ctrl+C
```

To completely delete the Minikube cluster:

```bash
minikube delete
```

---

# 🔄 End-to-End Project Flow

The complete project flow is:

```text
                  app.py
                     |
                     v
                 Dockerfile
                     |
                     | docker build
                     v
                Docker Image
                     |
                     | docker push
                     v
                 Docker Hub
       danielavidan/tiny-python-app
                     |
                     v
                 values.yaml
                     |
                     v
              Helm Templates
                     |
                     | helm upgrade --install
                     v
          Kubernetes Deployment
                     |
              +------+------+
              |             |
              v             v
            Pod #1         Pod #2
          Python :8000   Python :8000
              |             |
              +------+------+
                     |
                     v
             my-app-svc :8000
                ClusterIP
                     ^
                     |
               Ingress rule
                     ^
                     |
             Ingress Controller
                  HTTP :80
                     ^
                     |
         local Minikube networking
                     ^
                     |
 http://myapp.127.0.0.1.nip.io
                     ^
                     |
                   Browser
```

The key runtime request flow is therefore:

```text
Browser
  -> Ingress Controller
  -> my-app-svc
  -> Pod
  -> Python HTTP server
```

`kubectl port-forward` is no longer the primary access path once the Ingress is being tested.

It remains useful as a debugging tool.

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
- Understanding Kubernetes Ingress
- Understanding the difference between Ingress and an Ingress Controller
- Routing traffic from an Ingress to a Service
- Understanding external port `80` versus internal application port `8000`
- Using `nip.io` for local hostnames
- Using `minikube tunnel` for local cluster access
- Understanding when `kubectl port-forward` bypasses the Ingress
- Using Helm charts
- Using Helm templates
- Using `values.yaml`
- Passing configuration from Helm into containers
- Testing Helm charts with `--dry-run`
- Deploying applications with `helm upgrade --install`
- Testing Kubernetes applications locally with Minikube
- Using `kubectl` for inspection and troubleshooting

---
