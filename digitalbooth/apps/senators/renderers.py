from digitalbooth.apps.core.renderers import DigitalBoothJSONRenderer
from digitalbooth.apps.core.utils import set_metadata


class SenatorJSONRenderer(DigitalBoothJSONRenderer):
    object_label = 'senator'

    def render(self, data, media_type=None, renderer_context=None):
        set_metadata(renderer_context=renderer_context, data=data)
        return super(SenatorJSONRenderer, self).render(data)
