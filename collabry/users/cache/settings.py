from pydantic import NonNegativeInt

from collabry.common.cache.settings import BaseCacheSettings


class Settings(BaseCacheSettings):
    oauth2_state_ttl: NonNegativeInt = 120  # in seconds: 2 minutes
    reset_password_code_ttl: NonNegativeInt = 86400  # in seconds: 24 hours
