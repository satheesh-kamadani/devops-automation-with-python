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
- 🔹 Build **Docker image build and push to Amazon ECR** using Python
- 🔹 Upload **Upload build jar file to artifactory** using Python

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
requests
boto3

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

### 3. Run SonarQube Analysis
``` bash
python sonar_qube_analysis.py
```
Ensure your SonarQube server and authentication token are valid.

### 4. Scan Docker Images with Trivy
``` bash
python trivy_scan_image.py
```
This will scan Docker images defined in the script and generate a consolidated report:
trivy_scan_report.txt

### 5. Check Service Health
``` bash
python service_health_check.py
```
The script checks /health endpoints of services and logs their status.

### 6. AWS Resource Cleanup
``` bash
python aws_cleanup_stale_resources.py
```
This script identifies and deletes unused EBS volumes and other stale resources

### 7. Build docker image and push to amazon ECR
``` bash
python aws_cleanup_stale_resources.py
```
This script will build the docker image and push to amazon ECR

### 8. Upload build jar files to artifactory
``` bash
python upload_to_artifactory.py
```
This script will upload the build jar files to artifactory

