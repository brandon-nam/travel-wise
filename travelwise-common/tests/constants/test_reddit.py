import pytest

from constants.reddit import SUBREDDIT_COUNTRY_MAPPING, ClassificationType


@pytest.mark.parametrize(
    "test_input, expected_output", [("japantravel", "japan"), ("koreatravel", "korea")]
)
def test_subreddit_country_mapping(test_input: str, expected_output: str) -> None:
    assert SUBREDDIT_COUNTRY_MAPPING[test_input] == expected_output


@pytest.mark.parametrize(
    "test_input, expected_output",
    [
        (ClassificationType.travel_tip, "travel_tip"),
        (ClassificationType.travel_suggestion, "travel_suggestion"),
        (ClassificationType.other, "other"),
    ],
)
def test_classification_type(
    test_input: ClassificationType, expected_output: str
) -> None:
    assert test_input.value == expected_output
    assert expected_output in ClassificationType.__members__
