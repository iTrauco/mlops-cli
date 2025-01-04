"""
Manual test for Vertex AI Configuration 📝
"""
from mlops_catalog.vertex import get_default_config

def main():
    try:
        config = get_default_config()
        print("\n🔧 Vertex AI Configuration:")
        print(f"Project ID: {config.project_id}")
        print(f"Region: {config.region}")
        print(f"Staging Bucket: {config.get_staging_bucket()}")
        print(f"Container Registry: {config.default_container_registry}")
        print(f"MLOps Base Path: {config.mlops_base_path}")
        print("\n✅ Configuration loaded successfully!")
    except Exception as e:
        print(f"\n❌ Error loading configuration: {str(e)}")

if __name__ == "__main__":
    main()