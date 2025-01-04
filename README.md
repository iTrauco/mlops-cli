# MLOps Catalog

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
source venv/bin/activate  # On Windows: venv\Scripts\activate

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
