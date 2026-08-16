# Flask CI/CD Pipeline with Jenkins

## 📌 Project Overview

This project demonstrates a complete **CI/CD pipeline for a Flask application** using **GitHub, Jenkins, and AWS**.

The pipeline automatically gets the application source code from GitHub, installs the required dependencies, runs the application/tests, and performs the deployment steps. Jenkins also sends an **email notification** after the pipeline execution.

The main objective of this project is to understand how Continuous Integration and Continuous Deployment can be implemented using Jenkins.

---

## 🏗️ CI/CD Architecture

```text
Developer
    |
    | Push Code
    ↓
GitHub Repository
    |
    | Jenkins Checkout
    ↓
Jenkins
    |
    ├── Checkout Source Code
    ├── Install Dependencies
    ├── Run Tests
    ├── Build / Package Application
    ├── Deploy Application
    └── Send Email Notification
            |
            ↓
        Gmail Inbox
```

---

## 🚀 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Flask | Web application framework |
| Git | Version control |
| GitHub | Source code repository |
| Jenkins | CI/CD automation |
| AWS | Cloud infrastructure/deployment |
| Gmail SMTP | Jenkins email notifications |
| Linux | Jenkins/server environment |

---

## 📂 Project Structure

```text
flask-cicd-pipeline/
│
├── app.py
├── requirements.txt
├── Jenkinsfile
├── README.md
└── ...
```

### Important Files

#### `app.py`

Contains the Flask application code.

#### `requirements.txt`

Contains the Python packages required to run the application.

Example:

```text
Flask
```

#### `Jenkinsfile`

Contains the Jenkins Declarative Pipeline configuration.

The Jenkinsfile defines the different stages that Jenkins executes automatically.

---

# 🔄 CI/CD Pipeline

The Jenkins pipeline follows these major stages:

```text
GitHub
   ↓
Checkout
   ↓
Install Dependencies
   ↓
Test
   ↓
Build
   ↓
Deploy
   ↓
Email Notification
```

---

## 1. Source Code Management

The source code is maintained in GitHub.

Jenkins is configured to use the GitHub repository as the source repository.

Repository:

```text
https://github.com/Injamrajesh/flask-cicd-pipeline.git
```

Jenkins checks out the latest version of the code before executing the pipeline.

---

## 2. Jenkins Pipeline

Jenkins reads the `Jenkinsfile` from the GitHub repository.

The Jenkinsfile defines the pipeline stages and commands that need to be executed.

A typical pipeline contains:

```groovy
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest'
            }
        }

        stage('Build') {
            steps {
                echo 'Building Flask application...'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying Flask application...'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
```

> **Note:** The commands in the Jenkinsfile should match the actual configuration of the Jenkins server and deployment environment.

---

# 🧪 Pipeline Stages

## Stage 1: Checkout

Jenkins retrieves the latest source code from GitHub.

Example console output:

```text
Obtained Jenkinsfile from git
[Pipeline] Start of Pipeline
```

---

## Stage 2: Install Dependencies

Jenkins installs the Python packages specified in:

```text
requirements.txt
```

Example:

```bash
pip3 install -r requirements.txt
```

---

## Stage 3: Testing

The pipeline runs the application's tests.

Testing helps identify errors before the application is deployed.

Example:

```bash
python3 -m pytest
```

---

## Stage 4: Build

The build stage prepares the application for deployment.

Depending on the project configuration, this stage may include:

- Installing dependencies
- Creating application packages
- Preparing deployment files
- Validating the application

---

## Stage 5: Deploy

After successful testing and build steps, Jenkins performs the deployment.

The deployment target can be an AWS EC2 instance or another configured AWS environment.

---

# ☁️ AWS Deployment

AWS is used as the cloud environment for hosting/deploying the Flask application.

The general deployment flow is:

```text
Jenkins
   |
   | Deployment
   ↓
AWS
   |
   ↓
Flask Application
```

The Jenkins server requires appropriate AWS credentials/permissions when AWS services are accessed from the pipeline.

AWS credentials should **never be hard-coded inside the Jenkinsfile**.

Instead, Jenkins Credentials should be used.

---

# 🔐 Jenkins Credentials

Sensitive information such as:

- AWS Access Key
- AWS Secret Access Key
- GitHub credentials
- Gmail App Password

should be stored securely using:

```text
Jenkins → Manage Jenkins → Credentials
```

Credentials should not be committed to GitHub.

### ⚠️ Important

Never put credentials directly inside:

```text
Jenkinsfile
README.md
Python source files
GitHub repository
```

For example, do **not** use:

```text
AWS_ACCESS_KEY_ID=xxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxx
```

in source code.

---

# 📧 Jenkins Email Notification

Jenkins is configured to send email notifications after the pipeline execution.

The email flow is:

```text
Jenkins Pipeline
       |
       ↓
Email Extension / Mailer
       |
       ↓
Gmail SMTP
       |
       ↓
User Gmail Inbox
```

A successful pipeline can generate an email notification such as:

```text
Subject:
Jenkins Build Successful

Message:
The Jenkins pipeline completed successfully.
```

---

## Gmail SMTP Configuration

For Gmail SMTP, the following configuration is used:

```text
SMTP Server: smtp.gmail.com
SMTP Port: 587
Security: STARTTLS / TLS
Username: Your Gmail address
Password: Gmail App Password
```

### Important

The normal Gmail account password should **not** be used for Jenkins SMTP authentication.

A Google **App Password** should be used when applicable.

The App Password should be stored securely in Jenkins and should never be committed to GitHub.

---

# 📩 Email Notification Flow

```text
                 Jenkins
                    |
             Pipeline Execution
                    |
             ┌──────┴──────┐
             ↓             ↓
          SUCCESS        FAILURE
             |             |
             └──────┬──────┘
                    ↓
              Email Plugin
                    |
                    ↓
              Gmail SMTP
                    |
                    ↓
             Gmail Inbox
```

---

# ✅ Successful Pipeline

When all stages complete successfully, Jenkins marks the build as:

```text
SUCCESS
```

The Jenkins console contains output similar to:

```text
[Pipeline] End of Pipeline
Finished: SUCCESS
```

The configured recipient then receives the Jenkins email notification.

---

# ❌ Failed Pipeline

If any stage fails, Jenkins marks the build as:

```text
FAILURE
```

The failure can be investigated from:

```text
Jenkins → Build → Console Output
```

The console output helps identify which stage caused the failure.

---

# 🔍 Jenkins Console Output

A successful Jenkins execution contains messages similar to:

```text
Started by user

Obtained Jenkinsfile from git

[Pipeline] Start of Pipeline

[Pipeline] stage
[Pipeline] { (Checkout)

[Pipeline] stage
[Pipeline] { (Install Dependencies)

[Pipeline] stage
[Pipeline] { (Test)

[Pipeline] stage
[Pipeline] { (Build)

[Pipeline] stage
[Pipeline] { (Deploy)

Finished: SUCCESS
```

---

# 🛠️ How to Run the Project

## Step 1: Clone the Repository

```bash
git clone https://github.com/Injamrajesh/flask-cicd-pipeline.git
```

Move into the project directory:

```bash
cd flask-cicd-pipeline
```

---

## Step 2: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

---

## Step 3: Run the Flask Application

```bash
python3 app.py
```

The Flask application can then be accessed using the configured host and port.

For a local Flask application, the default URL is usually:

```text
http://127.0.0.1:5000
```

---

# ⚙️ Jenkins Job Configuration

Create a new Jenkins Pipeline job.

### Configure:

```text
Jenkins
   ↓
New Item
   ↓
Pipeline
```

Configure the GitHub repository:

```text
https://github.com/Injamrajesh/flask-cicd-pipeline.git
```

Then configure the pipeline to use the Jenkinsfile from source control.

Typical configuration:

```text
Definition:
Pipeline script from SCM

SCM:
Git

Repository:
https://github.com/Injamrajesh/flask-cicd-pipeline.git

Script Path:
Jenkinsfile
```

---

# ▶️ Running the Jenkins Pipeline

The pipeline can be started manually using:

```text
Build Now
```

Jenkins then:

1. Downloads the source code.
2. Reads the Jenkinsfile.
3. Executes the pipeline stages.
4. Runs tests.
5. Performs deployment steps.
6. Sends the email notification.

---

# 📊 CI/CD Benefits

This project demonstrates several important benefits of CI/CD.

### Continuous Integration

Developers can continuously push code to GitHub and Jenkins can automatically validate the changes.

### Automated Testing

Tests can be executed automatically instead of manually testing every change.

### Continuous Deployment

The application can be deployed automatically after successful validation.

### Faster Feedback

Jenkins provides immediate feedback when a build succeeds or fails.

### Email Notifications

Developers can receive email notifications about pipeline results.

---

# 🧰 Troubleshooting

## Jenkins Build Fails

Check:

```text
Jenkins → Build → Console Output
```

Look for the first error reported in the console.

---

## GitHub Checkout Problem

Verify:

- Repository URL
- Git installation
- Jenkins Git configuration
- Repository permissions

---

## Python Dependency Error

Run:

```bash
pip3 install -r requirements.txt
```

and verify that all required packages are listed in `requirements.txt`.

---

## Gmail Authentication Error

If Jenkins displays:

```text
535-5.7.8 Username and Password not accepted
```

verify:

- Gmail address is correct.
- Gmail App Password is correct.
- App Password is entered without spaces if required.
- SMTP username matches the Gmail account.
- Port is configured correctly.

For Gmail SMTP:

```text
SMTP Server: smtp.gmail.com
Port: 587
TLS/STARTTLS: Enabled
```

---

## STARTTLS Error

If Jenkins displays:

```text
530-5.7.0 Must issue a STARTTLS command first
```

make sure the SMTP configuration uses:

```text
Port: 587
STARTTLS/TLS: Enabled
```

Do not configure port 587 as SSL-on-connect.

---

# 📸 Screenshots

Add project screenshots to this section after uploading them to the repository.

Recommended screenshots:

### 1. GitHub Repository

```text
Screenshot showing the GitHub project repository
```

### 2. Jenkins Pipeline

```text
Screenshot showing Jenkins pipeline stages
```

### 3. Successful Build

```text
Screenshot showing:

Finished: SUCCESS
```

### 4. Jenkins Console Output

```text
Screenshot showing the successful pipeline execution
```

### 5. Email Notification

```text
Screenshot showing the Jenkins build success email received in Gmail
```

### 6. AWS Deployment

```text
Screenshot showing the deployed Flask application/AWS resource
```

---

# 🎯 Project Objective

The objective of this project is to implement a practical CI/CD workflow using Jenkins.

The project demonstrates how source code can move through the following automated process:

```text
Code
 ↓
GitHub
 ↓
Jenkins
 ↓
Checkout
 ↓
Dependencies
 ↓
Testing
 ↓
Build
 ↓
Deployment
 ↓
Email Notification
```

---

# 📚 Key Learning Outcomes

Through this project, the following concepts were practiced:

- Git and GitHub
- GitHub repository management
- Jenkins installation and configuration
- Jenkins Pipeline
- Jenkinsfile
- Declarative Pipeline syntax
- Automated testing
- CI/CD concepts
- AWS deployment
- Jenkins credentials
- Gmail SMTP configuration
- Jenkins email notifications
- Pipeline troubleshooting
- Console log analysis

---

# 🔒 Security Best Practices

The following security practices should be followed:

- Never commit passwords to GitHub.
- Never expose AWS secret keys.
- Use Jenkins Credentials for secrets.
- Use Gmail App Passwords instead of normal Gmail passwords where required.
- Do not place secrets directly inside the Jenkinsfile.
- Rotate credentials if they are accidentally exposed.
- Use minimum required AWS IAM permissions.

---

# 🏁 Conclusion

This project successfully demonstrates a basic **Flask CI/CD pipeline using Jenkins, GitHub, and AWS**.

Whenever the application source code is updated, Jenkins can automatically retrieve the latest code, execute the defined pipeline stages, perform testing/build/deployment activities, and notify the configured recipient through email.

The project provides practical experience with **DevOps automation, CI/CD, Jenkins Pipeline, GitHub integration, AWS deployment, and automated notifications**.

---

## 👨‍💻 Author

**Rajesh Injam**

GitHub:

```text
https://github.com/Injamrajesh
```

Project Repository:

```text
https://github.com/Injamrajesh/flask-cicd-pipeline
```

---

## ⭐ Project Status

```text
CI/CD Pipeline: Implemented
GitHub Integration: Implemented
Jenkins Pipeline: Implemented
Flask Application: Implemented
Email Notification: Implemented
AWS Integration: Configured
```
