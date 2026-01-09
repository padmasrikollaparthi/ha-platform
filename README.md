# ha-platform
# Highly Available Kubernetes Platform

## Objective

This project demonstrates the design and deployment of a **production-grade, highly available infrastructure on Kubernetes**.
It goes beyond simple stateless applications by deploying a **replicated PostgreSQL database** and a **resilient web application layer**, ensuring business continuity during failures such as pod crashes or infrastructure disruptions.

The goal is to showcase real-world Kubernetes reliability concepts including:

* Deployments with zero-downtime rolling updates
* StatefulSets with persistent storage
* Pod Anti-Affinity
* PodDisruptionBudgets (PDB)
* Liveness and Readiness probes
* Automated database backups using CronJobs

---

## Architecture Overview

```
User
 |
NodePort Service
 |
Web Application (Deployment - 3 Replicas)
 |  - Pod Anti-Affinity
 |  - Liveness & Readiness Probes
 |  - Rolling Updates (Zero Downtime)
 |
PostgreSQL Database (StatefulSet - 3 Replicas)
 |  - Primary + Standby Architecture
 |  - Headless Service for DNS
 |
Persistent Volumes (1Gi per replica)
 |
Automated Backups (CronJob)
```

---

## Prerequisites

* Docker
* Minikube
* kubectl
* Git

---

## Project Structure

```
ha-platform/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── src/
│   ├── app.py
│   └── requirements.txt
├── k8s/
│   ├── namespace.yaml
│   ├── web-deployment.yaml
│   ├── web-service.yaml
│   ├── web-pdb.yaml
│   ├── postgres-configmap.yaml
│   ├── postgres-secret.yaml
│   ├── postgres-headless-service.yaml
│   ├── postgres-statefulset.yaml
│   ├── postgres-pdb.yaml
│   └── postgres-backup-cronjob.yaml
└── screenshots/
    ├── screenshot-namespace.png
    ├── screenshot-pods-running.png
    ├── screenshot-pdb.png
    ├── screenshot-node-drain-recovery.png
    └── screenshot-cronjob.png
```

---

## Deployment Instructions

### 1. Start Minikube (Docker Driver)

```bash
minikube start --driver=docker
```

### 2. Configure Docker to Use Minikube

```bash
eval $(minikube docker-env)
```

### 3. Build the Web Application Image

```bash
docker build -t web-app:latest .
```

### 4. Deploy Kubernetes Resources

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

### 5. Verify Deployment

```bash
kubectl get pods -n ha-platform
kubectl get svc -n ha-platform
```
## 6.To open the web
```bash
  minikube service web-service -n ha-platform
```
---

## High Availability & Reliability Features

### Web Application

* Deployed using a **Deployment with 3 replicas**
* **Pod Anti-Affinity** ensures pods are scheduled on different nodes when possible
* **Liveness and Readiness probes** ensure traffic is routed only to healthy pods
* **RollingUpdate strategy** guarantees zero downtime during application updates
* **PodDisruptionBudget** ensures at least 2 pods are always available

### PostgreSQL Database

* Deployed using a **StatefulSet with 3 replicas**
* Uses a **Headless Service** for stable network identities
* Each replica uses a **PersistentVolumeClaim (1Gi)**
* Designed around a **Primary + Standby** replication model
* **PodDisruptionBudget** ensures database availability during disruptions

---

## Backup Strategy

* Automated daily backups implemented using a **Kubernetes CronJob**
* Uses `pg_dump` to back up the PostgreSQL database
* CronJob verification:

```bash
kubectl get cronjob -n ha-platform
```

---

## Resilience Testing & Failure Simulation

### Important Note (Minikube Limitation)

Minikube runs as a **single-node Kubernetes cluster**.
Because node draining would stop all workloads, **pod deletion** is used to simulate failures instead of node-level outages.

### Failure Simulation Command

```bash
kubectl delete pod web-app-<pod-name> -n ha-platform
kubectl get pods -n ha-platform
```

Kubernetes automatically recreates the pod, demonstrating **self-healing and resilience**.

---

## Evidence of Resilience

The `screenshots/` directory contains evidence of:

* Namespace creation
* All pods running with high availability
* PodDisruptionBudget enforcement
* Automatic pod recovery after simulated failure
* PostgreSQL backup CronJob configuration

These artifacts verify that the platform remains operational during failures.

---

## Docker Compose Verification (Automated Logic Check)

For automated application logic validation:

```bash
docker compose up --build
```

This verifies:

* Web application startup
* Database connectivity
* API availability

Stop with:

```bash
Ctrl + C
```

---

## Conclusion

This project demonstrates a **robust, highly available Kubernetes platform** following industry best practices.
The system is resilient to failures, supports zero-downtime deployments, protects data through persistent storage and automated backups, and is suitable as a foundation for production-grade workloads.
