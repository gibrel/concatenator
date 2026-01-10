from concatenator.core.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.app_name == "concatenator"
