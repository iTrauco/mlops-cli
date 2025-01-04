"""
Test Vertex AI Configuration Module 🧪
Tests configuration loading, validation, and environment variable handling
"""
import os
import pytest
import yaml
from pathlib import Path
from mlops_catalog.vertex import VertexAIConfig, get_default_config

@pytest.fixture
def setup_env():
    """Setup test environment variables"""
    # Save original environment
    original_env = {
        'MLOPS_BASE_PATH': os.getenv('MLOPS_BASE_PATH'),
        'VERTEX_PROJECT_ID': os.getenv('VERTEX_PROJECT_ID'),
        'GOOGLE_CLOUD_PROJECT': os.getenv('GOOGLE_CLOUD_PROJECT'),
        'VERTEX_REGION': os.getenv('VERTEX_REGION'),
        'VERTEX_STAGING_BUCKET': os.getenv('VERTEX_STAGING_BUCKET'),
        'MLOPS_DB_URL': os.getenv('MLOPS_DB_URL'),
        'MLOPS_LOG_LEVEL': os.getenv('MLOPS_LOG_LEVEL')
    }
    
    # Set test environment
    os.environ['MLOPS_BASE_PATH'] = '/tmp/mlops_test'
    os.environ['VERTEX_PROJECT_ID'] = 'trauco-streaming-dev'
    os.environ['VERTEX_REGION'] = 'us-central1'
    os.environ['VERTEX_STAGING_BUCKET'] = 'gs://trauco-streaming-dev-vertex-staging'
    os.environ['MLOPS_DB_URL'] = 'sqlite:////tmp/mlops_test/registry.db'
    os.environ['MLOPS_LOG_LEVEL'] = 'INFO'
    
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
    assert config.mlops_base_path == os.path.abspath(os.path.expanduser('/tmp/mlops_test'))
    assert config.mlops_log_level == 'INFO'

def test_missing_project_id(setup_env):
    """Test configuration validation with missing project ID"""
    os.environ.pop('VERTEX_PROJECT_ID', None)
    os.environ.pop('GOOGLE_CLOUD_PROJECT', None)
    os.environ.pop('VERTEX_REGION', None)  # Also remove region to trigger validation
    
    with pytest.raises(ValueError, match="Project ID must be set"):
        get_default_config()

def test_staging_bucket_generation(setup_env):
    """Test staging bucket auto-generation"""
    # Remove explicit staging bucket to test auto-generation
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

def test_yaml_config_missing_file(setup_env):
    """Test loading configuration from non-existent YAML file"""
    with pytest.raises(FileNotFoundError):
        VertexAIConfig.from_yaml(Path("nonexistent.yaml"))

def test_mlops_path_creation(setup_env, tmp_path):
    """Test MLOPS_BASE_PATH directory creation"""
    test_path = tmp_path / "mlops_test"
    os.environ['MLOPS_BASE_PATH'] = str(test_path)
    config = get_default_config()
    # Force directory creation through validate_config
    config.validate_config()
    assert test_path.exists()
    assert test_path.is_dir()

def test_environment_override(setup_env):
    """Test environment variable override of defaults"""
    os.environ['VERTEX_REGION'] = 'europe-west1'
    os.environ['VERTEX_CONTAINER_REGISTRY'] = 'eu.gcr.io'
    config = get_default_config()
    assert config.region == 'europe-west1'
    assert config.default_container_registry == 'eu.gcr.io'

def test_config_validation(setup_env):
    """Test configuration validation logic"""
    os.environ.pop('VERTEX_REGION', None)
    config = get_default_config()
    assert config.region == 'us-central1'  # Should use default value
    config.validate_config()  # Should not raise any errors

def test_staging_bucket_precedence(setup_env):
    """Test staging bucket explicit setting takes precedence"""
    explicit_bucket = "gs://explicit-bucket"
    os.environ['VERTEX_STAGING_BUCKET'] = explicit_bucket
    config = get_default_config()
    assert config.get_staging_bucket() == explicit_bucket