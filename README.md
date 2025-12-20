#   CI/CD using GitHub Actions Self-Hosted Runner on EC2 (Docker Hub Enabled)

This project demonstrates a real-world CI/CD pipeline using GitHub Actions with a self-hosted runner running on an AWS EC2 instance.
On every push , the application is automatically built and deployed as a Docker container on EC2.


##  Key Components

GitHub Actions – CI/CD orchestration

Self-hosted Runner – Installed on EC2

Docker – Application containerization

AWS EC2 (Ubuntu) – Deployment host

Sample Python application


## STEP 1️⃣ Create EC2 Instance

 OS: Ubuntu 22.04

 Instance: t2.micro / t3.micro

 Security Group:

 SSH: 22

 HTTP: 80

![ec2-instance](images/ec2-instance.png)

## STEP 2️⃣ Install Docker on EC2
```sh
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
exit
```

## Login again:
```sh
docker ps
```




## STEP 3️⃣ Configure Docker Hub Secrets in GitHub

Go to:

Repo → Settings → Secrets and variables → Actions → New repository secret

Add:

| Secret Name        | Value                  |
|--------------------|------------------------|
| DOCKERHUB_USERNAME | Docker Hub username    |
| DOCKERHUB_TOKEN    | Docker Hub access token|




## STEP 4️⃣ Install GitHub Self-Hosted Runner
4.1 Create Runner in GitHub

Repo → Settings → Actions → Runners → New self-hosted runner
Choose Linux (x64) and copy commands.

4.2 Install Runner on EC2 with the provided commands shown in the GitHub



## STEP 5️⃣ Project Structure

```text
├── app.py
├── requirement.txt
├── Dockerfile
└── .github/
    └── workflows/
        └── deploy.yml
```

## STEP 6️⃣ Application Code

app.py
```sh
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Flask running in Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## requirements.txt
```sh
flask
```

## STEP 7️⃣ Dockerfile
```sh
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

## STEP 8️⃣ GitHub Actions Workflow (Docker Hub Push)

📁 .github/workflows/deploy.yml

```sh
name: Self-Hosted-Ubuntu-Runner-DockerHub

on: [push]

jobs:
  Build:
    runs-on: self-hosted

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login \
          -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      - name: Build Docker image
        run: |
          docker build -t ${{ secrets.DOCKER_USERNAME }}/flask-app:latest .

      - name: Push Docker image
        run: |
          docker push ${{ secrets.DOCKER_USERNAME }}/flask-app:latest

      - name: Stop old container
        run: |
          docker stop flask-app || true
          docker rm flask-app || true

      - name: Run new container
        run: |
          docker run -d -p 80:5000 --name flask-app \
          ${{ secrets.DOCKER_USERNAME }}/flask-app:latest
```


## 📌 Secrets are used ONLY for Docker Hub authentication

## STEP 9️⃣ Push Code to GitHub
```text
git add .
git commit -m "Add Docker Hub CI/CD deployment"
git push origin main
```


## STEP 🔟 Verify GitHub Actions

Repo → Actions

Workflow should run automatically

Runner: self-hosted



## STEP 1️⃣1️⃣ Verify on EC2
```sh
docker images
docker ps
```


Expected:
```text
<dockerhub-username>/flask-app   latest
```

## STEP 1️⃣2️⃣ Access Application

Open browser:
```sh
http://<EC2_PUBLIC_IP>
```


# Conclusion

## This project demonstrates real CI/CD practices using GitHub Actions, Docker, and a self-hosted runner on EC2.
