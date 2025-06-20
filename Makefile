setup-env:
	@echo "Setting up environment"
	@bash setup.sh

backend-dev:
	@echo "Running backend..."
	@cd backend && python manage.py runserver