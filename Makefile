# Define some variables
REPO = "https://github.com/talk2jaydip/preqlin_app"
IMAGE = preqlin_app
TAG = 1.0.0
ENV = dev

# Set the name of your virtual environment
VENV_NAME = venv

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make prepare env=venv           Create a virtual environment"
	@echo "  make install        Install project dependencies"
	@echo "  make run            Run the Flask app in the virtual environment"
	@echo "  make test           Run unit tests"
	@echo "  make git-commit     Commit changes to Git"
	@echo "  make git-push       Push changes to Git"
	@echo "  make git-pull       Pull changes from Git"

# Define a rule for virtualenv prepare
prepare:
	# Check if the virtual environment directory exists
	EXIST = $(shell [ -d "$(ENV)" ] && echo "yes" || echo "no")
	# If not, create the virtual environment
	if [ "$(EXIST)" = "no" ]; then \
		@echo --------------------
		@echo Creating virtualenv
		@echo --------------------
		virtualenv $(ENV)
	fi
	# Activate the virtual environment
	source $(ENV)/bin/activate
	# Install the requirements from the requirements.txt file
	pip install -r requirements.txt


# Alternatively, define a rule for running docker compose with a variable argument
compose:
	# Run docker compose with the specified configuration and environment files
	docker compose -f "docker-compose-$(env).yaml" --env-file $(env).env up -d --build

git-commit:
	@echo "Committing changes to Git..."
	git add .
	git commit -m "Update: `date +'%Y-%m-%d %H:%M:%S'`"

git-push:
	@echo "Pushing changes to Git..."
	git push

git-pull:
	@echo "Pulling changes from Git..."
	git pull





.PHONY: venv install run test docker-build docker-run docker-stop docker-clean git-commit git-push git-pull
