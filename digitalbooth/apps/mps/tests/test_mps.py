import pytest

from digitalbooth.apps.mps.tests.factories import MpFactory


@pytest.mark.django_db
def test_user_can_create_mp_record(authorized_client, base_url):
    mp = {
        'name': 'John Doe',
        'img_url': 'http://image.com/url',
        'county': 'Kiambu',
        'constituency': 'Juja',
        'party': 'JP',
        'field_status': 'Elected'
    }
    response = authorized_client.post(f'{base_url}mps', mp, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_can_update_mp_record(authorized_client, base_url):
    mp = MpFactory()
    data = {
        'county': 'Nairobi'
    }
    response = authorized_client.put(f'{base_url}mps/{mp.id}', data, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_can_get_all_mps(authorized_client, base_url):
    batch = 3
    MpFactory.create_batch(batch)
    response = authorized_client.get(f'{base_url}mps', format='json')
    assert response.status_code == 200
    assert len(response.data.get('results')) == batch


@pytest.mark.django_db
def test_user_can_get_single_mp(authorized_client, base_url):
    mp = MpFactory()
    response = authorized_client.get(f'{base_url}mps/{mp.id}', format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_can_delete_mp_record(authorized_client, base_url):
    mp = MpFactory()
    response = authorized_client.delete(f'{base_url}mps/{mp.id}', format='json')
    response1 = authorized_client.get(f'{base_url}mps/{mp.id}')
    assert response.status_code == 200
    assert response1.status_code == 404
