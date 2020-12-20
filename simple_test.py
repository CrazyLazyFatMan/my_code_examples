import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_swagger_ok(client):
    """Swagger открывается."""
    swagger_response = client.get(reverse('api:v1:schema-swagger-ui'))
    assert swagger_response.status_code == status.HTTP_200_OK

    openapi_response = client.get(
        reverse('api:v1:schema-swagger-ui'),
        {'format': 'openapi'},
    )
    assert openapi_response.status_code == status.HTTP_200_OK