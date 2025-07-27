import asyncio
import inspect
import logging

log = logging.getLogger(__name__)

async def run_maybe_async(func, *args, **kwargs):
    """Run sync or async callable transparently."""
    try:
        result = func(*args, **kwargs)
    except Exception:  # pylint: disable=broad-except
        log.exception("Handler %s raised", func)
        return

    if inspect.isawaitable(result):
        try:
            await result
        except Exception:  # pylint: disable=broad-except
            log.exception("Awaitable handler %s raised", func) 