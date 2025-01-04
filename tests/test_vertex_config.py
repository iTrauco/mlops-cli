"""
Test Vertex AI Configuration Module 🧪
"""
import os
import pytest
from pathlib import Path
from mlops_catalog.vertex import VertexAIConfig, get_default_config

@pytest.fixture
def setup_env():
    """Setup test environment variables"""
    # Save original environment
    original_env = {
        'MLOPS_BASE_PATH': os.getenv('MLOPS_BASE_PATH'),
        'VERTEX_PROJECT_ID': os.getenv('VERTEX_PROJECT_ID'),
        'VERTEX_REGION': os.getenv('VERTEX_REGION'),
        'VERTEX_STAGING_BUCKET': os.getenv('VERTEX_STAGING_BUCKET')
    }
    
    # Set test environment
    os.environ['MLOPS_BASE_PATH'] = '/tmp/mlops_test'
    os.environ['VERTEX_PROJECT_ID'] = 'trauco-streaming-dev'
    os.environ['VERTEX_REGION'] = 'us-central1'
    os.environ['VERTEX_STAGING_BUCKET'] = 'gs://trauco-streaming-dev-vertex-staging'
    
    yield
    
    # Restore original environment
    for key, value in original_env.items():
        if value is not None:
            os.environ[key] = value
        else:
            os.environ.pop(key, None)

def test_default_config(setup_env):
    """Test default configuration loading"""
    config = get_default_config()
    assert config.project_id == 'trauco-streaming-dev'
    assert config.region == 'us-central1'
    assert config.staging_bucket == 'gs://trauco-streaming-dev-vertex-staging'
    assert config.default_container_registry == 'gcr.io'

def test_missing_project_id(setup_env):
    """Test configuration validation with missing project ID"""
    os.environ.pop('VERTEX_PROJECT_ID', None)
    os.environ.pop('GOOGLE_CLOUD_PROJECT', None)
    
    with pytest.raises(ValueError, match="Project ID must be set"):
        get_default_config()

def test_staging_bucket_generation(setup_env):
    """Test staging bucket auto-generation"""
    os.environ.pop('VERTEX_STAGING_BUCKET', None)
    config = get_default_config()
    assert config.get_staging_bucket() == 'gs://trauco-streaming-dev-vertex-staging'

def test_yaml_config(setup_env, tmp_path):
    """Test loading configuration from YAML"""
    config_path = tmp_path / "vertex_config.yaml"
    config_data = {
        "project_id": "test-project",
        "region": "us-west1",
        "staging_bucket": "gs://test-bucket",
        "default_container_registry": "gcr.io/test"
    }
    
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
    
    config = VertexAIConfig.from_yaml(config_path)
    assert config.project_id == "test-project"
    assert config.region == "us-west1"
    assert config.staging_bucket == "gs://test-bucket"
    assert config.default_container_registry == "gcr.io/test"