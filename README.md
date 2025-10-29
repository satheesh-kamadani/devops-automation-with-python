# 🚀 DevOps Automation with Python

A collection of **real-world Python scripts** that automate day-to-day **DevOps workflows** — including CI/CD triggers, Docker image scanning, Kubernetes deployments, SonarQube analysis, AWS resource cleanup, and service health monitoring.

These scripts demonstrate how Python can be used effectively to integrate and automate popular DevOps tools like **Jenkins**, **Docker**, **Kubernetes**, **AWS**, **SonarQube**, and **Trivy**.

---

## 🧩 Features

- 🔹 Trigger **Jenkins pipelines** using Python and the Jenkins REST API  
- 🔹 Deploy **Kubernetes workloads** (Deployments, Services, etc.) to EKS using Python  
- 🔹 Run **SonarQube static code analysis** automatically from a Python script  
- 🔹 Scan **Docker images** for vulnerabilities using **Trivy**  
- 🔹 Perform **service health checks** for deployed microservices  
- 🔹 Clean up **stale AWS EBS volumes** and other unused resources using Python  

---

## ⚙️ Prerequisites

Make sure the following tools and libraries are installed before running the scripts:

### 🧰 System Requirements
- Python **3.8+**
- Docker (for image scanning)
- kubectl (for Kubernetes deployments)
- AWS CLI (for AWS cleanup tasks)
- Jenkins server access (for pipeline triggers)
- SonarQube server (for static code analysis)
- Trivy (for vulnerability scanning)

### 📦 Python Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt

Example requirements.txt
``` bash
requests
boto3
```
Usage

### 1. Trigger a Jenkins Pipeline
``` bash
python trigger_jenkins_pipeline.py
```
Edit the Jenkins URL, username, and token inside the script or pass them via environment variables:
``` bash
export JENKINS_URL=http://jenkins.example.com
export JENKINS_USER=jenkins_user
export JENKINS_TOKEN=your_api_token
```
### 2. Deploy to EKS Cluster
``` bash
python deploy_to_eks.py
```
Make sure your kubeconfig path and deployment YAML file are correctly configured.

