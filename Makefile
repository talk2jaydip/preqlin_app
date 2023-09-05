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
	@echo "  make compose ENV=dev" Create Docker Compose file ENV=prd/test

# Define a rule for virtualenv prepare
prepare:
	# Check if the virtual environment directory exists
	if [ ! -d "$(ENV)" ]; then \
		echo "-------------------"; \
		echo "Creating virtualenv"; \
		echo "-------------------"; \
		virtualenv $(ENV); \
	fi
	# Activate the virtual environment and install requirements using the script
	./init.sh $(ENV)



start:
	# Run docker compose with the specified configuration and environment files
	docker compose -f "./app/docker-compose-$(ENV).yaml" --env-file ./app/$(ENV).env up -d --build
stop:
	docker compose -f "./app/docker-compose-$(ENV).yaml" --env-file ./app/$(ENV).env down
restart:
	docker compose -f "./app/docker-compose-$(ENV).yaml" --env-file ./app/$(ENV).env down
	docker compose -f "./app/docker-compose-$(ENV).yaml" --env-file ./app/$(ENV).env up -d --build




git-commit:
	@echo "Committing changes to Git..."
	git add .
	git commit -m "Update: `'%Y-%m-%d %H:%M:%S'`"

git-push:
	@echo "Pushing changes to Git..."
	git push

git-pull:
	@echo "Pulling changes from Git..."
	git pull

test:
	python -m pytest app/tests

run:
	python app/run.py


.PHONY: venv install run test docker-build docker-run docker-stop docker-clean git-commit git-push git-pull
