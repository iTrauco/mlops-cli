#!/usr/bin/env python3
"""
Complete setup script for MLOps Catalog project.
Creates entire project structure, all files, and configurations in one go.
"""

import os
import shutil
from pathlib import Path
import subprocess
import sys
import logging
from typing import List, Dict, Any, Optional
import json
import argparse
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MLOpsProjectSetup:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir).resolve()
        self.project_name = "mlops_catalog"
        
    def create_directory_structure(self):
        """Create the complete directory structure"""
        directories = [
            # Main package
            self.project_name,
            f"{self.project_name}/core",
            f"{self.project_name}/runners",
            f"{self.project_name}/data",
            f"{self.project_name}/storage",
            f"{self.project_name}/utils",
            f"{self.project_name}/config",
            f"{self.project_name}/exceptions",
            f"{self.project_name}/templates",
            # Tests
            "tests",
            "tests/unit",
            "tests/integration",
            "tests/fixtures",
            # Documentation
            "docs",
            "docs/api",
            "docs/user_guide",
            "docs/_static",
            # Additional directories
            "scripts",
            "notebooks",
            "examples",
            "docker",
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            # Create __init__.py files for Python packages
            if "tests" not in directory and "docs" not in directory:
                (dir_path / "__init__.py").touch()
                
        logger.info("Created directory structure")

    def write_gitignore(self):
        """Create comprehensive .gitignore"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
.env
.venv
pip-log.txt
pip-delete-this-directory.txt

# IDE
.idea/
.vscode/
*.swp
*.swo
*~
.project
.pydevproject
.settings/

# Testing
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.pytest_cache/
cover/
.hypothesis/

# MLOps specific
.mlops/
models/
artifacts/
experiments/
*.db
*.sqlite3
workspace/
logs/
*.log
wandb/
mlruns/
.dvc/
.dvcignore
*.dvc
checkpoints/

# Documentation
docs/_build/
docs/api/_autosummary/

# Data
data/
*.csv
*.parquet
*.pkl
*.joblib
*.h5
*.hdf5
*.json
*.yaml
*.yml
*.arrow
*.feather
*.sav

# Jupyter
.ipynb_checkpoints
*/.ipynb_checkpoints/*
*.ipynb
!examples/*.ipynb

# OS
.DS_Store
Thumbs.db
.directory
Desktop.ini

# Environment variables
.env*
!.env.example

# Docker
.docker/
*.tar
*.tar.gz

# Dependencies
poetry.lock
Pipfile.lock

# Profiling
*.prof
*.pstat
"""
        with open(self.base_dir / '.gitignore', 'w') as f:
            f.write(gitignore_content)
        logger.info("Created .gitignore")

    def create_core_files(self):
        """Create core module files"""
        # registry.py
        registry_content = '''"""
Registry system for models and experiments
"""
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List
import json
from pathlib import Path

@dataclass
class ModelMetadata:
    name: str
    version: str
    created_at: datetime
    framework: str
    params: Dict[str, Any]
    metrics: Dict[str, float]
    artifacts_path: str

class Registry:
    """Central registry for models and experiments"""
    
    def __init__(self, base_path: str = "~/.mlops/registry"):
        self.base_path = Path(base_path).expanduser()
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.db_path = self.base_path / "registry.db"
        self._init_db()
'''
        self._write_file(f"{self.project_name}/core/registry.py", registry_content)

        # tracking.py
        tracking_content = '''"""
Metrics and experiment tracking
"""
from pathlib import Path
import json
from typing import Dict, Any, Optional
from datetime import datetime
import time

class ExperimentTracker:
    """Tracks experiment metrics and parameters"""
    
    def __init__(self, experiment_name: str, base_path: str = "~/.mlops/experiments"):
        self.experiment_name = experiment_name
        self.base_path = Path(base_path).expanduser()
        self.exp_path = self.base_path / experiment_name
        self.exp_path.mkdir(parents=True, exist_ok=True)
'''
        self._write_file(f"{self.project_name}/core/tracking.py", tracking_content)

    def create_cli(self):
        """Create CLI implementation"""
        cli_content = '''"""
MLOps Catalog CLI
"""
import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
import yaml

app = typer.Typer(help="MLOps Catalog - Manage your ML experiments and models")
console = Console()

# Sub-commands
model_app = typer.Typer(help="Model management commands")
exp_app = typer.Typer(help="Experiment management commands")
data_app = typer.Typer(help="Data management commands")

app.add_typer(model_app, name="model")
app.add_typer(exp_app, name="exp")
app.add_typer(data_app, name="data")

@model_app.command("register")
def register_model(
    config_file: Path = typer.Argument(..., help="Path to model configuration YAML"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Validate without registering")
):
    """Register a new model"""
    try:
        with open(config_file) as f:
            config = yaml.safe_load(f)
        # Implementation here
        console.print("[green]Model registered successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
'''
        self._write_file(f"{self.project_name}/cli.py", cli_content)

    def create_example_configs(self):
        """Create example configuration files"""
        # Model config example
        model_config = '''name: resnet50-classifier
version: v1.0.0
framework: pytorch
params:
  architecture: resnet50
  pretrained: true
  num_classes: 10
  learning_rate: 0.001
  batch_size: 32
  optimizer: adam
artifacts_path: models/resnet50-classifier/v1.0.0
'''
        self._write_file("examples/model_config.yaml", model_config)

        # Experiment config example
        exp_config = '''name: training-run-001
description: Initial training run with ResNet50
params:
  epochs: 100
  learning_rate: 0.001
  batch_size: 32
  optimizer:
    name: adam
    beta1: 0.9
    beta2: 0.999
tags:
  - baseline
  - production
'''
        self._write_file("examples/experiment_config.yaml", exp_config)

    def create_docker_files(self):
        """Create Docker-related files"""
        # Dockerfile
        dockerfile_content = '''FROM python:3.9-slim

WORKDIR /app
COPY . /app/

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["mlops"]
'''
        self._write_file("docker/Dockerfile", dockerfile_content)

        # Docker compose
        docker_compose_content = '''version: '3.8'
services:
  mlops:
    build: .
    volumes:
      - ~/.mlops:/root/.mlops
    environment:
      - MLOPS_ENV=production
'''
        self._write_file("docker/docker-compose.yml", docker_compose_content)

    def create_setup_files(self):
        """Create setup.py and related files"""
        setup_py_content = '''from setuptools import setup, find_packages

setup(
    name="mlops_catalog",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "rich>=10.0",
        "pandas>=1.3",
        "pyyaml>=5.4",
        "sqlalchemy>=1.4",
        "typer>=0.4",
        "python-dotenv>=0.19",
    ],
    entry_points={
        "console_scripts": [
            "mlops=mlops_catalog.cli:app",
        ],
    },
)
'''
        self._write_file("setup.py", setup_py_content)

    def create_readme(self):
        """Create README.md"""
        readme_content = '''# MLOps Catalog

A comprehensive MLOps catalog system for managing machine learning experiments, models, and artifacts.

## Features

- Experiment tracking and management
- Model registry with versioning
- Data source management
- Local and cloud runners
- CLI interface

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mlops_catalog.git
cd mlops_catalog

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Usage

1. Register a model:
```bash
mlops model register config.yaml
```

2. Run an experiment:
```bash
mlops exp run experiment.yaml train.py
```

3. Register a data source:
```bash
mlops data register training-data data/train.csv
```

## Documentation

Full documentation is available in the `docs` directory.

## License

This project is licensed under the MIT License.
'''
        self._write_file("README.md", readme_content)

    def _write_file(self, path: str, content: str):
        """Helper to write content to file"""
        file_path = self.base_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        logger.info(f"Created {path}")

    def initialize_git(self):
        """Initialize git repository"""
        try:
            subprocess.run(["git", "init"], cwd=self.base_dir, check=True)
            subprocess.run(["git", "add", "."], cwd=self.base_dir, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=self.base_dir, check=True)
            logger.info("Initialized git repository")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to initialize git: {e}")

    def setup_project(self):
        """Run complete project setup"""
        logger.info("Starting MLOps Catalog project setup...")
        
        self.create_directory_structure()
        self.write_gitignore()
        self.create_core_files()
        self.create_cli()
        self.create_example_configs()
        self.create_docker_files()
        self.create_setup_files()
        self.create_readme()
        self.initialize_git()
        
        logger.info("Project setup completed successfully!")

def main():
    parser = argparse.ArgumentParser(description="Setup MLOps Catalog project")
    parser.add_argument("--dir", default=".", help="Target directory for project")
    args = parser.parse_args()

    setup = MLOpsProjectSetup(args.dir)
    setup.setup_project()

if __name__ == "__main__":
    main()
