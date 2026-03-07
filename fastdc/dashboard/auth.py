"""
FastDC Dashboard — Authentication helpers
"""

from functools import wraps
from typing import Callable, Any
from quart import session, redirect, url_for, Response


def login_required(f: Callable) -> Callable:
    """
    Decorator to protect routes that require dashboard authentication.

    If the user's session lacks the 'authenticated' flag, they are redirected
    to the login page. Otherwise, the requested route executes normally.
    """
    @wraps(f)
    async def decorated(*args: Any, **kwargs: Any) -> Response:
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return await f(*args, **kwargs)
    return decorated
