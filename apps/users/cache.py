from django.core.cache import cache

class LoginCache:
    """
    Cache for login
    """

    @classmethod
    def _key(cls, email):
        return 'invalid_login_attempt_{}'.format(email)

    @classmethod
    def _value(cls, lockout_timestamp, time_bucket):
        return {
            'lockout_start': lockout_timestamp,
            'invalid_attempt_timestamps': time_bucket
        }

    @classmethod
    def delete(cls, email):
        try:
            cache.delete(cls._key(email))
        except Exception as e:
            print(e)

    @classmethod
    def set(cls, email, time_bucket, lockout_timestamp=None):
        try:
            key = cls._key(email)
            value = cls._value(lockout_timestamp, time_bucket)
            cache.set(key, value)
        except Exception as e:
            print(e)

    @classmethod
    def get(cls, email):
        try:
            key = cls._key(email)
            return cache.get(key)
        except Exception as e:
            print(e)
