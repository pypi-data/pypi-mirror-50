
from logging import getLogger
from aiohttp import ClientSession


class PostmarkClient(object):
    """

    Example:

    curl "https://api.postmarkapp.com/email" \
        -X POST \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -H "X-Postmark-Server-Token: server token" \
        -d "{From: 'sender@example.com', To: 'receiver@example.com', Subject: 'Postmark test', HtmlBody: '<html><body><strong>Hello</strong> dear Postmark user.</body></html>'}"

    """

    def __init__(self, server_token):
        self.__log = getLogger('aiopm')
        self._server_token = server_token

    async def send(self, From, To, Subject, HtmlBody):
        """ Send a single email

        @see: https://postmarkapp.com/developer/api/email-api
        """
        url = 'https://api.postmarkapp.com/email'
        payload = {
            'From': From,
            'To': To,
            'Subject': Subject,
            'HtmlBody': HtmlBody,
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Postmark-Server-Token': self._server_token,
        }
        #
        async with ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                self.__log.debug("status = {status!r}".format(status=resp.status))
                if resp.status != 200:
                    content = await resp.text()
                    raise RuntimeError('Postmark response code {status} and content {content}'.format(status=resp.status, content=content))
                values = await resp.json()
                return values

    async def sendWithTemplate(self, From, To, TemplateAlias, TemplateModel, Tag=None):
        """ Send email with template

        @see: https://postmarkapp.com/developer/api/templates-api#email-with-template
        """
        url = 'https://api.postmarkapp.com/email/withTemplate'
        payload = {
            'TemplateAlias': TemplateAlias,
            'TemplateModel': TemplateModel,
            'From': From,
            'To': To,
            'Tag': Tag,
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Postmark-Server-Token': self._server_token,
        }
        #
        async with ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                self.__log.debug("status = {status!r}".format(status=resp.status))
                if resp.status != 200:
                    content = await resp.text()
                    raise RuntimeError('Postmark response code {status} and content {content}'.format(status=resp.status, content=content))
                values = await resp.json()
                return values
