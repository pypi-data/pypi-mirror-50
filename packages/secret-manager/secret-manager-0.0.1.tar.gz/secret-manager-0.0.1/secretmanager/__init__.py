from secretmanager.secret_manager import SecretManager

secret_manager = SecretManager()
secrets = secret_manager.get_secrets()
