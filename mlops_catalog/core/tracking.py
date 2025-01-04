"""
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
