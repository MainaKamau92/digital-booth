from rest_framework.settings import api_settings


def set_metadata(renderer_context, data):
    """
    Sets pagination data as metadata in the request
    :param renderer_context:
    :param data:
    :return:
    """
    if renderer_context is not None and 'count' in data:
        response = renderer_context.get('response')
        page_size = api_settings.PAGE_SIZE
        response['Count'] = data['count']
        response['Pages'] = int(data['count'] / page_size) if int(data['count'] / page_size) > 0 or data[
            'count'] == 0 else 1
        response['Previous'] = data['previous']
        response['Next'] = data['next']
        response['Access-Control-Expose-Headers'] = 'Previous, Next, Count, Pages'
