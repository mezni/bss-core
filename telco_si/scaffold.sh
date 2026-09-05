#!/usr/bin/env bash
set -euo pipefail

echo "==> 1. Installing uv (Python package installer & manager)..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Source uv binary for current shell session
    export PATH="$HOME/.local/bin:$PATH"
    echo "uv installed successfully!"
else
    echo "uv is already installed."
fi

echo "==> 2. Creating environment configuration & docs directory..."
touch .env.example
touch .gitignore
mkdir -p docs

echo "==> 3. Creating repository documentation set inside docs/..."
touch docs/BRIEF.md
touch docs/ARCHITECTURE.md
touch docs/PLAN.md
touch docs/API.md
touch docs/DATA_MODEL.md
touch docs/SEEDING.md
touch docs/OPERATIONS.md
touch CONTRIBUTING.md
touch CHANGELOG.md
touch README.md

echo "==> 4. Populating default .gitignore..."
cat << 'EOF' > .gitignore
# Python artifacts
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Environment files
.env

# Database & IDEs
*.sqlite3
.vscode/
.idea/
.DS_Store

# Alembic compiled files
migrations/versions/*.pyc
EOF

echo "==> 5. Initializing Python environment with uv..."
uv venv .venv
echo "==> 6. Installing core dependencies via uv..."
uv pip install fastapi "uvicorn[standard]" sqlmodel asyncpg alembic typer faker pydantic-settings

echo ""
echo "========================================================================="
echo " Scaffolding Complete!"
echo " Next Steps:"
echo "   1. Activate virtual environment: source .venv/bin/activate"
echo "   2. Populate documentation files inside the docs/ folder"
echo "   3. Begin defining SQLModel domain classes"
echo "========================================================================="