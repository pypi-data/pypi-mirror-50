import os

from aiohttp import web
from cbpi.api import *

class CBPiUi2(CBPiExtension):

    @request_mapping(path="/", auth_required=False)
    async def hello_world(self, request):
        return web.Response(text="Hello, world")

    def __init__(self, cbpi):
        self.cbpi = cbpi
        path = os.path.dirname(__file__)
        self.cbpi.register(self, "/cbpi_uiplugin", static=os.path.join(path, "static"))

def setup(cbpi):
    print("###### SEUTP UI #####")
    cbpi.plugin.register("UI-plugin", CBPiUi2)
