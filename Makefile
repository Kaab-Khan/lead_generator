############################################################
# Lead Generator — Makefile
# Minimal, clean, senior-developer quality
############################################################

PYTHON := python3
VENV_DIR := venv
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip

############################################################
# 1. ENVIRONMENT MANAGEMENT
############################################################

# Check if venv exists; if not, create it
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "✓ Created virtual environment in $(VENV_DIR)"

# Ensure venv is created before running any pip installs
ensure-venv: $(VENV_DIR)
	@echo "✓ Virtual environment ready"
	@echo "To activate, run: source $(VENV_BIN)/activate"

############################################################
# 2. INSTALL DEPENDENCIES
############################################################

requirements: ensure-venv
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	@echo "✓ Installed runtime dependencies"

requirements-dev: ensure-venv
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	@if [ -f requirements-dev.txt ]; then $(PIP) install -r requirements-dev.txt; fi
	@echo "✓ Installed development dependencies"

############################################################
# 3. RUN APPLICATION
############################################################

run:
	@echo "⚠️  Remember to activate the venv if not using this command:"
	@echo "   source $(VENV_BIN)/activate"
	@echo ""
	$(VENV_BIN)/python src/main.py

############################################################
# 4. CODE QUALITY
############################################################

format:
	$(VENV_BIN)/black src/ tests/
	@echo "✓ Code formatted"

lint:
	$(VENV_BIN)/pylint src/
	@echo "✓ Linting complete"

############################################################
# 5. TESTING
############################################################

test:
	$(VENV_BIN)/pytest tests/ -v
	@echo "✓ Tests complete"

############################################################
# 6. UTILITY
############################################################

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned Python caches"

clean-all: clean
	rm -rf $(VENV_DIR)
	@echo "✓ Removed virtual environment"

help:
	@echo "Lead Generator - Available Commands:"
	@echo ""
	@echo "  Environment:"
	@echo "    make ensure-venv       - Create/verify virtual environment"
	@echo "    make requirements      - Install runtime dependencies"
	@echo "    make requirements-dev  - Install dev dependencies"
	@echo ""
	@echo "  Run:"
	@echo "    make run              - Run the application"
	@echo ""
	@echo "  Code Quality:"
	@echo "    make format           - Format code with Black"
	@echo "    make lint             - Lint code with Pylint"
	@echo "    make test             - Run tests with Pytest"
	@echo ""
	@echo "  Utility:"
	@echo "    make clean            - Remove cache files"
	@echo "    make clean-all        - Remove cache + venv"
	@echo "    make help             - Show this help"
	@echo ""

############################################################
# END
############################################################
