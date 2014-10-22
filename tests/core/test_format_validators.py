import pytest

from flex.formats import (
    date_time_format_validator,
)


#
# date_time_format_validator tests
#
@pytest.mark.parametrize(
    'value',
    (1, True, None, 2.0, [], {}),
)
def test_date_time_format_validator_skips_non_string_types(value):
    date_time_format_validator(value)


@pytest.mark.parametrize(
    'value',
    (
        '2011-13-18T10:29:47+03:00',  # Invalid month 13
        '2011-08-32T10:29:47+03:00',  # Invalid day 32
        '2011-08-18T25:29:47+03:00',  # Invalid hour 25
        '2011-08-18T10:65:47+03:00',  # Invalid minute 65
        '2011-08-18T10:29:65+03:00',  # Invalid second 65
        '2011-08-18T10:29:65+25:00',  # Invalid offset 25 hours
    )
)
def test_date_time_format_validator_detects_invalid_values(value):
    from django.core.exceptions import ValidationError
    with pytest.raises(ValidationError):
        date_time_format_validator(value)


@pytest.mark.parametrize(
    'value',
    (
        '2011-08-18T10:29:47+03:00',
        '2011-08-18',
        '1985-04-12T23:20:50.52Z',
        '1996-12-19T16:39:57-08:00',
        # Leap second should be valid but iso8601 doesn't correctly parse.
        pytest.mark.xfail('1990-12-31T23:59:60Z'),
        # Leap second should be valid but iso8601 doesn't correctly parse.
        pytest.mark.xfail('1990-12-31T15:59:60-08:00'),
        # Weird netherlands time from strange 1909 law.
        pytest.mark.xfail('1937-01-01T12:00:27.87+00:20'),
    )
)
def test_date_time_format_validator_with_valid_dateties(value):
    from django.core.exceptions import ValidationError
    date_time_format_validator(value)
