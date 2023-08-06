"""
Utils for implementing multi-factor authentication.
"""

from datetime import timedelta
import secrets

__all__ = [
    'create_scoped_session',
    'delete_scoped_session',
    'verify_scoped_session'
]


def create_scoped_session(cache, scope, expire_after=None):
    """
    Create a scoped session (a session which has been authenticated to perform
    the given scope of work.

    The scope should describe the actor and the action, for example:

        (user, request_full_path)

    The function returns a session key that along with the scopr can be used
    to verify the session.
    """

    # Generate the key
    session_key = secrets.token_urlsafe(32)

    # Store the key
    if isinstance(expire_after, timedelta):
        expire_after = int(expire_after.total_seconds())

    cache.set(f'mfa_scoped_session:{session_key}', scope, expire_after)

    return session_key

def delete_scoped_session(cache, session_key):
    """Clear a scoped session"""
    cache.delete(f'mfa_scoped_session:{session_key}')

def verify_scoped_session(cache, session_key, scope):
    """Verify a scoped session"""
    return cache.get(f'mfa_scoped_session:{session_key}') == scope
