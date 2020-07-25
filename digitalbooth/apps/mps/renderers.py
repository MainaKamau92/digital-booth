from digitalbooth.apps.core.renderers import DigitalBoothJSONRenderer
from digitalbooth.apps.core.utils import set_metadata


class MPsJSONRenderer(DigitalBoothJSONRenderer):
    object_label = 'employee'

    def render(self, data, media_type=None, renderer_context=None):
        set_metadata(renderer_context=renderer_context, data=data)
        return super(MPsJSONRenderer, self).render(data)
