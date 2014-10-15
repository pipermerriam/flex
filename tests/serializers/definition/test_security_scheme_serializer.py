import pytest

from flex.serializers.definitions import SecuritySchemeSerializer
from flex.constants import (
    BASIC,
    API_KEY,
    OAUTH_2,
    QUERY,
    HEADER,
    IMPLICIT,
    PASSWORD,
    APPLICATION,
    ACCESS_CODE,
)

from tests.utils import assert_error_message_equal


#
# name field validations tests
#
def test_name_required_if_type_is_api_key():
    serializer = SecuritySchemeSerializer(
        data={'type': API_KEY},
    )

    assert not serializer.is_valid()
    assert 'name' in serializer.errors
    assert_error_message_equal(
        serializer.errors['name'][0],
        serializer.error_messages['name_required']
    )


def test_type_as_api_key_with_name_value():
    serializer = SecuritySchemeSerializer(
        data={'type': API_KEY, 'name': 'TestName'},
    )

    assert 'name' not in serializer.errors


@pytest.mark.parametrize(
    'type_',
    (
        BASIC,
        OAUTH_2,
    ),
)
def test_name_optional_for_non_api_key_types(type_):
    assert 'name' not in SecuritySchemeSerializer(
        data={'type': type_},
    ).errors


#
# in field validation tests
#
def test_in_is_required_if_type_is_api_key():
    serializer = SecuritySchemeSerializer(
        data={'type': API_KEY, 'name': 'TestName'},
    )

    assert not serializer.is_valid()
    assert 'in' in serializer.errors
    assert_error_message_equal(
        serializer.errors['in'][0],
        serializer.error_messages['in_required']
    )


@pytest.mark.parametrize(
    'in_',
    (
        QUERY,
        HEADER,
    ),
)
def test_type_as_api_key_with_in_value(in_):
    serializer = SecuritySchemeSerializer(
        data={'type': API_KEY, 'in': in_},
    )

    assert 'in' not in serializer.errors


@pytest.mark.parametrize(
    'type_',
    (
        BASIC,
        OAUTH_2,
    ),
)
def test_in_optional_for_non_api_key_types(type_):
    assert 'in' not in SecuritySchemeSerializer(
        data={'type': type_},
    ).errors


#
# flow validations tests
#
def test_flow_is_required_if_type_oath2():
    serializer = SecuritySchemeSerializer(
        data={'type': OAUTH_2},
    )

    assert not serializer.is_valid()
    assert 'flow' in serializer.errors
    assert_error_message_equal(
        serializer.errors['flow'][0],
        serializer.error_messages['flow_required']
    )


def test_type_as_oath2_with_flow_value():
    serializer = SecuritySchemeSerializer(
        data={'type': OAUTH_2, 'flow': IMPLICIT},
    )

    assert 'flow' not in serializer.errors


def test_flow_optional_for_non_oath_types():
    assert 'flow' not in SecuritySchemeSerializer(
        data={'type': BASIC},
    ).errors
    assert 'flow' not in SecuritySchemeSerializer(
        data={'type': API_KEY},
    ).errors


#
# authorizationUrl validation tests
#
@pytest.mark.parametrize(
    'flow',
    (IMPLICIT, ACCESS_CODE)
)
def test_authorization_url_required_if_type_is_oath2(flow):
    serializer = SecuritySchemeSerializer(
        data={'type': OAUTH_2, 'flow': flow},
    )

    assert not serializer.is_valid()
    assert 'authorizationUrl' in serializer.errors
    assert_error_message_equal(
        serializer.errors['authorizationUrl'][0],
        serializer.error_messages['authorization_url_required']
    )


@pytest.mark.parametrize(
    'flow',
    (PASSWORD, APPLICATION)
)
def test_type_as_oath2_with_authorization_url_value(flow):
    serializer = SecuritySchemeSerializer(
        data={
            'type': OAUTH_2,
            'authorizationUrl': 'http://www.example.com/login/',
            'flow': flow,
        },
    )

    assert 'authorizationUrl' not in serializer.errors


@pytest.mark.parametrize(
    'type_',
    (BASIC, API_KEY)
)
def test_authorization_url_optional_for_non_oath_types(type_):
    assert 'authorizationUrl' not in SecuritySchemeSerializer(
        data={'type': type_},
    ).errors


@pytest.mark.parametrize(
    'flow',
    (PASSWORD, APPLICATION)
)
def test_authorization_url_optional_for_invalid_flows(flow):
    assert 'authorizationUrl' not in SecuritySchemeSerializer(
        data={'type': OAUTH_2, 'flow': flow},
    ).errors


#
# tokenUrl field validation tests
#
@pytest.mark.parametrize(
    'flow',
    (PASSWORD, APPLICATION, ACCESS_CODE)
)
def test_token_url_required_if_type_is_oath2(flow):
    serializer = SecuritySchemeSerializer(
        data={'type': OAUTH_2, 'flow': flow},
    )

    assert not serializer.is_valid()
    assert 'tokenUrl' in serializer.errors
    assert_error_message_equal(
        serializer.errors['tokenUrl'][0],
        serializer.error_messages['token_url_required']
    )


@pytest.mark.parametrize(
    'flow',
    (PASSWORD, APPLICATION, ACCESS_CODE)
)
def test_type_as_oath2_with_token_url_value(flow):
    serializer = SecuritySchemeSerializer(
        data={
            'type': OAUTH_2,
            'flow': flow,
            'tokenUrl': 'http://www.example.com/login/',
        },
    )

    assert 'tokenUrl' not in serializer.errors


@pytest.mark.parametrize(
    'type_',
    (BASIC, API_KEY)
)
def test_token_url_optional_for_non_oath_types(type_):
    assert 'tokenUrl' not in SecuritySchemeSerializer(
        data={'type': type_},
    ).errors


@pytest.mark.parametrize(
    'flow',
    (IMPLICIT,)
)
def test_token_url_optional_for_invalid_flows(flow):
    assert 'tokenUrl' not in SecuritySchemeSerializer(
        data={'type': OAUTH_2, 'flow': flow},
    ).errors
