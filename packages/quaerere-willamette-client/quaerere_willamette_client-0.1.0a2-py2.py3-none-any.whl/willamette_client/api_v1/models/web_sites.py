from quaerere_base_client.model import ModelBase
from willamette_common.schemas.api_v1.mixins import WebSiteFieldsMixin


class WebSiteModel(WebSiteFieldsMixin, ModelBase):
    pass
