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
        default_factory=lambda: os.getenv('GOOGLE_CLOUD_PROJECT'),
        description="GCP Project ID"
    )
    region: str = Field(
        default="us-central1",
        description="GCP Region for Vertex AI operations"
    )
    staging_bucket: Optional[str] = Field(
        default=None,
        description="GCS bucket for staging Vertex AI assets"
    )
    default_container_registry: str = Field(
        default="gcr.io",
        description="Default container registry path"
    )

    class Config:
        env_prefix = "VERTEX_"  # Will look for env vars like VERTEX_PROJECT_ID

    def get_staging_bucket(self) -> str:
        """Get or generate staging bucket path 🪣"""
        if self.staging_bucket:
            return self.staging_bucket
        return f"gs://{self.project_id}-vertex-staging"

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
    
    Attempts to load from environment variables first, then falls back to defaults
    
    Returns:
        VertexAIConfig: Default configuration instance
    """
    return VertexAIConfig()