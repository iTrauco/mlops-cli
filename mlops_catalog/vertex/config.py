"""
Vertex AI Configuration Module 🔧
This module handles configuration settings and environment setup for Vertex AI integration.
Includes default values and configuration validation.
"""
from typing import Optional, Dict, Any
from pathlib import Path
import os
import yaml
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load from MLOPS_BASE_PATH if available
mlops_base_path = os.getenv('MLOPS_BASE_PATH', '~/.mlops')
env_path = os.path.expanduser(os.path.join(mlops_base_path, '.env'))
load_dotenv(env_path)

class VertexAIConfig(BaseSettings):
    """
    Vertex AI Configuration Settings ⚙️
    
    Attributes:
        project_id (str): GCP Project ID
        region (str): GCP Region for Vertex AI operations
        staging_bucket (str): GCS bucket for staging Vertex AI assets
        default_container_registry (str): Default container registry path
    """
    project_id: str = Field(
        default_factory=lambda: os.getenv('VERTEX_PROJECT_ID') or os.getenv('GOOGLE_CLOUD_PROJECT'),
        description="GCP Project ID"
    )
    region: str = Field(
        default_factory=lambda: os.getenv('VERTEX_REGION', 'us-central1'),
        description="GCP Region for Vertex AI operations"
    )
    staging_bucket: Optional[str] = Field(
        default_factory=lambda: os.getenv('VERTEX_STAGING_BUCKET'),
        description="GCS bucket for staging Vertex AI assets"
    )
    default_container_registry: str = Field(
        default_factory=lambda: os.getenv('VERTEX_CONTAINER_REGISTRY', 'gcr.io'),
        description="Default container registry path"
    )
    mlops_base_path: str = Field(
        default_factory=lambda: os.getenv('MLOPS_BASE_PATH', '~/.mlops'),
        description="Base path for MLOps resources"
    )
    
    class Config:
        env_prefix = "VERTEX_"  # Will look for env vars like VERTEX_PROJECT_ID
        env_file = env_path
        env_file_encoding = 'utf-8'

    def get_staging_bucket(self) -> str:
        """Get or generate staging bucket path 🪣"""
        if self.staging_bucket:
            return self.staging_bucket
        return f"gs://{self.project_id}-vertex-staging"
    
    def validate_config(self) -> None:
        """Validate required configuration values are set 🔍"""
        if not self.project_id:
            raise ValueError("Project ID must be set via VERTEX_PROJECT_ID or GOOGLE_CLOUD_PROJECT")
        if not self.region:
            raise ValueError("Region must be set via VERTEX_REGION or defaults to us-central1")
        
        # Ensure MLOPS_BASE_PATH exists
        Path(os.path.expanduser(self.mlops_base_path)).mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_yaml(cls, config_path: Path) -> "VertexAIConfig":
        """
        Load configuration from YAML file 📄
        
        Args:
            config_path (Path): Path to YAML configuration file
            
        Returns:
            VertexAIConfig: Configuration instance
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
        return cls(**config_data)

def get_default_config() -> VertexAIConfig:
    """
    Get default Vertex AI configuration 🎯
    
    Attempts to load from environment variables first, then falls back to defaults.
    Also validates the configuration.
    
    Returns:
        VertexAIConfig: Default configuration instance
        
    Raises:
        ValueError: If required configuration values are missing
    """
    config = VertexAIConfig()
    config.validate_config()
    return config