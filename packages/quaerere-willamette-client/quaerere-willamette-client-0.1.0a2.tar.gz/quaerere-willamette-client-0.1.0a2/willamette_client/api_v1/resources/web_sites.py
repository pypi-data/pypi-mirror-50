__all__ = ['WebSiteResource']

from quaerere_base_client.resource import Resource
from willamette_common.schemas.api_v1 import WebSiteSchema


class WebSiteResource(Resource):
    resource_schema = WebSiteSchema
    model_class = None
