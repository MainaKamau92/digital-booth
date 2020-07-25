from digitalbooth.apps.core.renderers import DigitalBoothJSONRenderer
from digitalbooth.apps.core.utils import set_metadata


class UserJSONRenderer(DigitalBoothJSONRenderer):
    charset = 'utf-8'

    object_label = 'user'

    def render(self, data, media_type=None, renderer_context=None):
        # If we receive a `token` key as part of the response, it will by a
        # byte object. Byte objects don't serializer well, so we need to
        # decode it before rendering the User object.

        set_metadata(renderer_context=renderer_context, data=data)

        token = data.get('token', None)
        if token is not None and isinstance(token, bytes):
            # Also as mentioned above, we will decode `token` if it is of type
            # bytes.
            data['token'] = token.decode('utf-8')

        return super(UserJSONRenderer, self).render(data)
