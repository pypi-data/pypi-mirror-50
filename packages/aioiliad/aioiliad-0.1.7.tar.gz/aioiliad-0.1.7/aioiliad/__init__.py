"""Init of aioiliad."""
import asyncio
import logging
import aiohttp
import async_timeout


BASEURL = 'https://www.iliad.it/account/'

_LOGGER = logging.getLogger(__name__)


class Iliad(object):
    """Representation of Iliad."""

    def __init__(self, username, password, session, loop):
        """Init Iliad."""
        self.username = username
        self.password = password
        self._session = session
        self._loop = loop
        self.page = None

    async def login(self):
        """Login into Iliad."""
        data = {'login-ident': self.username,
                'login-pwd': self.password}
        try:
            async with async_timeout.timeout(10, loop=self._loop):
                await self._session.get(BASEURL + "?logout=user")
                post = await self._session.post(BASEURL, data=data)
                self.page = await post.text()
        except (asyncio.TimeoutError,
                aiohttp.ClientError,
                asyncio.CancelledError) as error:
            _LOGGER.error('%s', error)
        except Exception as error:  # pylint: disable=W0703
            _LOGGER.error('%s', error)

    def is_logged_in(self):
        """Get login status."""
        if self.page is None:
            return False
        if "ID utente o password non corretto." in self.page:
            return False
        return True

    async def update(self):
        """Trigger update."""
        await self.login()
