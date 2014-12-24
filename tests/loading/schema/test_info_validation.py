from flex.loading.schema import (
    info_validator,
    swagger_schema_validator,
)
from flex.exceptions import ValidationError

from tests.utils import (
    assert_message_in_errors,
)
from tests.factories import (
    RawSchemaFactory,
)


def test_info_field_is_required():
    """
    Test that the info field is required for overall schema validation.
    """
    raw_schema = RawSchemaFactory()
    raw_schema.pop('info', None)

    assert 'info' not in raw_schema

    with pytest.raises(ValidationError) as err:
        swagger_schema_validator(raw_schema)

    assert_message_in_errors(
        err.value.detail,
    )
