##  Project Directory Structure
This document provides an overview of the directory structure for  project. It outlines the purpose of each file and directory in the project.

    | ./
    | .dockerignore            # Configuration for Docker to ignore specific files
    | .gitignore               # Configuration for Git to ignore specific files
    | api_usage.ipynb          # Jupyter Notebook for API usage examples
    | blacklist.py             # Module for managing blacklisted tokens
    | config.py                # Configuration file for your Flask app
    | dev.env                  # Environment variables for development
    | docker-compose-dev.yaml  # Docker Compose configuration for development environment
    | docker-compose-prd.yaml  # Docker Compose configuration for production environment
    | Dockerfile               # Dockerfile for building your Flask app image
    | prod.env                 # Environment variables for production
    | requirements.txt         # List of Python dependencies for your app
    | run.py                   # Entry point for running your Flask app
    | setup.py                 # Setup script for your Python package
    | __init__.py

    | my_app/                  # Main directory for your Flask app
    |     __init__.py
    |     models/              # Directory for database models
    |     |   user.py          # Model for user data
    |     |   __init__.py
    |     resources/           # Directory for API resources
    |     |   random_array.py  # Resource for generating random arrays
    |     |   user.py          # Resource for user-related endpoints
    |     |   __init__.py
    |     schemas/             # Directory for data schemas
    |     |   user.py          # Schema for user data
    |     |   __init__.py

    | tests/                   # Directory for unit tests
    |     test_endpoints.py    # Tests for API endpoints
    |     __init__.py

Certainly! Here's a more refined and clear "How to run" section for your README file:

## How to Run

You can run this project either in a virtual environment or as a Docker container. Below are instructions for both options:

### Option 1: Virtual Environment

1. **Clone the Repository**: Start by cloning this project's repository from GitHub to your local machine using the following command:

    ```bash
    git clone https://github.com/talk2jaydip/preqlin_app
    ```

2. **Create a Virtual Environment**: Navigate to the project directory and create a virtual environment (you can specify your environment name, e.g., `venv`) using:

    ```bash
    make prepare env=venv
    ```

   This command also installs the project dependencies.

3. **Activate the Virtual Environment**: Activate the virtual environment with the following command:

    ```bash
    source venv/bin/activate
    ```

4. **Run the Flask App**: To run the Flask app locally, execute the following command:

    ```bash
    make start
    ```

   The app will be available at `http://localhost:5000`.

5. **Run Unit Tests**: You can run the project's unit tests using:

    ```bash
    make test
    ```

6. **Deactivate the Virtual Environment**: When you're done, deactivate the virtual environment:

    ```bash
    deactivate
    ```

### Option 2: Docker Container

1. **Clone the Repository**: If you haven't already, clone this project's repository from GitHub:

    ```bash
    git clone https://github.com/talk2jaydip/preqlin_app
    ```

2. **Create a Docker Compose File**: Generate a Docker Compose file for your desired environment (e.g., `dev`) using:

    ```bash
    make compose ENV=dev
    ```


3. **Run the Docker Container**: Start the Docker container with the following command:

    ```bash
    make start or make restart
    ```

   The app will be available at `http://localhost:8000`.

4. **Stop the Docker Container**: To stop the Docker container, use:

    ```bash
    make stop
    ```

These instructions should help you run the project smoothly, whether you choose a virtual environment or a Docker container.

## Components

- **Docker Container**: The application runs within a Docker container for portability and isolation.

- **Flask App**: The core of the application built using Flask, which handles HTTP requests and responses.

- **Database**: The application uses a relational database, either SQLite or PostgreSQL, for data storage.

- **RevokeAccessToken Table**: A table in the database used to store revoked access tokens. (Not using,Alternative to BlackLIST)

- **User Model**: Represents user data and interacts with the database.

- **User Schema**: Handles data serialization and deserialization.

- **API Resources**: Flask-RESTful resources for user registration, login, token management, user retrieval, and random array generation.

- **JWT (JSON Web Tokens)**: Used for user authentication and token management.

## Flow

1. **User Registration**:
   - User sends a POST request to `/register` with user details.
   - The request is processed by the `UserRegister` resource.
   - User data is validated and saved to the database if valid.
2. **User Confirmation**:
   - Users click on an activation link sent via email after registration.
   - The link contains the user ID.
   - The `/user_confirm/<int:user_id>` route is accessed to confirm the user.
3. **User Login**:
   - User sends a POST request to `/login` with credentials.
   - The request is processed by the `UserLogin` resource.
   - If credentials are valid and the user is confirmed, an access token and a refresh token are generated and returned.

4. **User Retrieval**:
   - Users can send a GET request to `/user/<int:user_id>` to retrieve user details by user ID.

5. **Random Array Generation**:
   - Authenticated users can send a POST request to `/generate_random_array` with a sentence.
   - A 500-dimensional random float array is generated and returned in the response.

6. **Token Refresh**:
   - Users can send a POST request to `/refresh` with a valid refresh token to obtain a new access token.

7. **User Logout**:
   - Users send a POST request to `/logout` to log out.
   - The JWT ID (jti) is added to the blacklist, preventing the use of the access token.

7. **User Delete**:
    - Users send a delete request to `/user/<int:user_id>` to log out.


## Notes

- Environment-specific configurations are set, such as the database URL and secret keys.
- The application is containerized using Docker for consistency.
- Authentication and authorization are handled using JWTs.
- User data is stored in the database using the `UserModel`.
- Flask-RESTful resources handle different HTTP endpoints for user management.
- api_usage.ipynb has all endoints with response for demonstration.



## AWS Deployment stratergy for Flask Application

### Step 1: AWS Setup
**Launch an EC2 Instance**:
-   Choose an EC2 instance type suitable for  application.
-   Configure the security group to allow incoming traffic on ports 22 (SSH) and 80 (HTTP).
-   Launch the instance and create a key pair for SSH access.
- 
### Step 2: SSH into the EC2 Instance

Use the key pair created to SSH into  EC2 instance.
`ssh -i key.pem ec2-user@ec2-instance-ip`

### Step 3: Update and Install Dependencies

Update the package manager and install necessary dependencies:

### Step 4: Set Up  Flask Application

1.  Clone  Flask application repository onto the EC2 instance.
2.  Install  application's dependencies using `pip`.

### Step 5: Set Up uWSGI

1.  Install uWSGI:
    `sudo pip3 install uwsgi`
   
 2. Create a uWSGI configuration file (e.g., `my_app_uwsgi.ini`) :

```pytohn
[uwsgi]
module = wsgi:app
master = true
processes = 4
socket = my_app.sock
chmod-socket = 660
vacuum = true
die-on-term = true
```
> Ensure that `wsgi:app` points to  Flask application object.

### Step 6: Configure Nginx

1.Create an Nginx server block configuration file (e.g., `my_app_nginx.conf`)

```python
server {
    listen 80;
    server_name my-domain.com;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/path/to/app/my_app.sock;
    }
    location @app {
        include uwsgi_params;
        uwsgi_pass unix:/path/to//app/my_app.sock;
    }
}
```

### Step 7: Set Up Database

1. using a database (e.g., PostgreSQL/Sqlite), create a database instance on AWS RDS and update  application configuration accordingly.

### Step 8: Scalability and Load Balancing

1.  **Auto Scaling Groups**: Create an Auto Scaling Group to manage multiple EC2 instances.
    
2.  **Elastic Load Balancer (ELB)**: Set up an Application Load Balancer (ALB) to distribute traffic across  EC2 instances. Configure the ALB to use a target group with  Auto Scaling Group.


### Step 9: Logging and Monitoring

1.  **CloudWatch Logs**: Configure CloudWatch Logs to monitor application logs, including access logs and error logs.
    
2.  **CloudWatch Alarms**: Set up CloudWatch Alarms to monitor server health, CPU usage, and other relevant metrics.

### Step 10: SSL/TLS Certificate (Optional)

If we want to use HTTPS, obtain an SSL/TLS certificate and configure it with  ALB. AWS Certificate Manager (ACM) can help to manage SSL/TLS certificates.

### Step 11: Domain Configuration

Update  domain registrar's DNS settings to point to the ALB's DNS name.
    
## Deployment Workflow:
Sure, here's the deployment workflow explained in Markdown points:

**Deployment Workflow for Flask App on AWS:**

1. **Create a Source Code Repository:**

   - Set up a source code repository to store  Flask app code and configuration files.
   - Use a version control system like  AWS CodeCommit, GitHub, or Bitbucket.

2. **Dockerfile:**
   - The Docker image  include  app code, dependencies, and necessary settings.
   
3. **Create an Amazon ECR Repository:**

   - Establish an Amazon Elastic Container Registry (ECR) repository to store  Docker images.
   - Amazon ECR is a managed container registry service that simplifies image management.
   - Use the AWS CLI or AWS Console to create an ECR repository dedicated to  Flask app.

4. **Create a Buildspec File:**

   - Develop a buildspec file in YAML format to instruct AWS CodeBuild on how to build and test = Flask app.
   - AWS CodeBuild is a managed build service that compiles  code, runs tests, and generates deployment-ready artifacts.
   - Customize the buildspec file according to  app's build and test requirements.

5. **Create an Appspec File:**

   - Design an appspec file in YAML format to specify the deployment process for AWS CodeDeploy.
   - AWS CodeDeploy automates code deployments to EC2 instances or other compute platforms.
   - The appspec file should outline which files to copy and which scripts to execute during deployment.
   - Modify the appspec file to suit  Flask app's deployment needs.

6. **Create an AWS CodePipeline Pipeline:**

   - Establish an AWS CodePipeline pipeline to orchestrate the CI/CD workflow =
   - AWS CodePipeline is a managed continuous delivery service that coordinates build, test, and deployment phases.
   - Configure  pipeline using the AWS Console or AWS CLI.

**Pipeline Stages and Actions:**

- **Source Stage:**
   - Retrieve the Flask app source code from the source code repository.
   - This stage monitors changes to  code repository and triggers the pipeline accordingly.

- **Build Stage:**
   - Use AWS CodeBuild to build the Docker image for  Flask app.
   - AWS CodeBuild will execute the buildspec file to compile code and generate Docker images.
   
- **Test Stage:**
   - Run tests on the Docker image to ensure app functionality.
   - Test scripts defined in the buildspec file should be executed during this stage.
   
- **Deploy Stage:**
   - Employ AWS CodeDeploy to deploy  Flask app to EC2 instances or chosen compute platforms.
   - AWS CodeDeploy will utilize the appspec file to copy files and run deployment scripts.
   

## Additional Considerations

-   Store sensitive environment variables securely on  EC2 instance or use a tool like AWS Secrets Manager.use boto library to read secrete in code
    
-   Configure monitoring and logging tools like CloudWatch to keep an eye on  application's health and performance.
    
-   Implement backup strategies for  database.
    
-   Configure Auto Scaling Groups for  EC2 instances to handle increased traffic.

