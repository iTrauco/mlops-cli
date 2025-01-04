"""
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
