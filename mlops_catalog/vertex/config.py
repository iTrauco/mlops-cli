"""
Vertex AI Configuration Module 🔧
"""
from typing import Optional
from pathlib import Path
import os
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class VertexAIConfig(BaseSettings):
    project_id: Optional[str] = None
    region: str = Field(default='us-central1')
    staging_bucket: Optional[str] = None
    mlops_base_path: str = Field(default='~/.mlops')
    mlops_db_url: Optional[str] = None
    mlops_log_level: str = Field(default='INFO')
    default_container_registry: str = Field(default='gcr.io')

    model_config = SettingsConfigDict(
        env_prefix="VERTEX_",
        env_file=None,
        extra='allow'
    )

    def get_staging_bucket(self) -> str:
        if os.getenv('VERTEX_STAGING_BUCKET'):
            return os.getenv('VERTEX_STAGING_BUCKET')
        if self.staging_bucket:
            return self.staging_bucket
        return f"gs://{self.project_id}-vertex-staging"
    
    def validate_config(self) -> None:
        project_id = os.getenv('VERTEX_PROJECT_ID') or os.getenv('GOOGLE_CLOUD_PROJECT')
        if not project_id:
            raise ValueError("Project ID must be set via VERTEX_PROJECT_ID or GOOGLE_CLOUD_PROJECT")
        
        self.project_id = project_id
        self.mlops_base_path = os.path.abspath(os.path.expanduser(os.getenv('MLOPS_BASE_PATH', self.mlops_base_path)))
        os.makedirs(self.mlops_base_path, exist_ok=True)

        if container_registry := os.getenv('VERTEX_CONTAINER_REGISTRY'):
            self.default_container_registry = container_registry

    @classmethod
    def from_yaml(cls, config_path: Path) -> "VertexAIConfig":
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)

def get_default_config() -> VertexAIConfig:
    config = VertexAIConfig()
    config.validate_config()
    return config