"""
Tests for Vertex AI Configuration 🧪
"""
import os
import pytest
from mlops_catalog.vertex import VertexAIConfig, get_default_config

def test_default_config():
    """Test default configuration loading"""
    config = get_default_config()
    assert config.region == "us-central1"
    assert config.default_container_registry == "gcr.io"

def test_env_vars():
    """Test configuration from environment variables"""
    os.environ["VERTEX_PROJECT_ID"] = "test-project"
    os.environ["VERTEX_REGION"] = "us-west1"
    
    config = VertexAIConfig()
    assert config.project_id == "test-project"
    assert config.region == "us-west1"

def test_staging_bucket():
    """Test staging bucket generation"""
    config = VertexAIConfig(project_id="test-project")
    assert config.get_staging_bucket() == "gs://test-project-vertex-staging"