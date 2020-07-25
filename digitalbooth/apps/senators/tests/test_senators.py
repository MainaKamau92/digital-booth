import pytest

from digitalbooth.apps.senators.tests.factories import SenatorFactory


@pytest.mark.django_db
def test_user_can_create_senator_record(authorized_client, base_url):
    senator = {
        'name': 'John Doe',
        'img_url': 'http://image.com/url',
        'county': 'Kiambu',
        'party': 'JP',
        'field_status': 'Elected'
    }
    response = authorized_client.post(f'{base_url}senators', senator, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_can_update_senator_record(authorized_client, base_url):
    senator = SenatorFactory()
    data = {
        'county': 'Nairobi'
    }
    response = authorized_client.put(f'{base_url}senators/{senator.id}', data, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_can_get_all_senators(authorized_client, base_url):
    batch = 3
    SenatorFactory.create_batch(batch)
    response = authorized_client.get(f'{base_url}senators', format='json')
    assert response.status_code == 200
    assert len(response.data.get('results')) == batch


@pytest.mark.django_db
def test_user_can_get_single_senators(authorized_client, base_url):
    senator = SenatorFactory()
    response = authorized_client.get(f'{base_url}senators/{senator.id}', format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_can_delete_senator_record(authorized_client, base_url):
    senator = SenatorFactory()
    response = authorized_client.delete(f'{base_url}senators/{senator.id}', format='json')
    response1 = authorized_client.get(f'{base_url}senators/{senator.id}')
    assert response.status_code == 200
    assert response1.status_code == 404
