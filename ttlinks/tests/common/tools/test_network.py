import pytest
from ttlinks.common.tools.network import BinaryTools


def test_expand_by_mask_mixed():
    digits = [0, 1, 0]
    mask = [1, 1, 0]
    result = BinaryTools.expand_by_mask(digits, mask)
    expected_result = [(0, 1, 0), (0, 1, 1)]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_expand_by_mask_all_fixed():
    digits = [1, 0, 1]
    mask = [1, 1, 1]
    result = BinaryTools.expand_by_mask(digits, mask)
    expected_result = [(1, 0, 1)]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_expand_by_mask_all_variable():
    digits = [0, 1, 0]
    mask = [0, 0, 0]
    result = BinaryTools.expand_by_mask(digits, mask)
    expected_result = [
        (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
        (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)
    ]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_expand_by_mask_empty_input():
    digits = []
    mask = []
    result = BinaryTools.expand_by_mask(digits, mask)
    expected_result = [()]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_expand_by_mask_single_variable():
    digits = [1]
    mask = [0]
    result = BinaryTools.expand_by_mask(digits, mask)
    expected_result = [(0,), (1,)]
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_is_binary_in_range_valid():
    # Test where compared_digits are within the range
    id_digits = [1, 0, 1, 0, 1, 1]
    mask_digits = [1, 1, 1, 0, 0, 0]
    compared_digits = [1, 0, 1, 1, 0, 0]
    assert BinaryTools.is_binary_in_range(id_digits, mask_digits, compared_digits) is True

    # Test where compared_digits are not within the range
    id_digits = [1, 1, 0, 0, 0, 1]
    mask_digits = [1, 1, 1, 1, 0, 0]
    compared_digits = [0, 1, 0, 0, 1, 1]
    assert BinaryTools.is_binary_in_range(id_digits, mask_digits, compared_digits) is False


def test_is_binary_in_range_no_match():
    # Test where compared_digits do not match in masked positions
    id_digits = [1, 0, 0, 0, 1, 1]
    mask_digits = [1, 1, 0, 0, 0, 0]
    compared_digits = [0, 0, 0, 1, 1, 1]
    assert BinaryTools.is_binary_in_range(id_digits, mask_digits, compared_digits) is False


def test_is_binary_in_range_exact_match():
    # Test where id_digits and compared_digits are exactly the same
    id_digits = [1, 0, 1, 0, 1, 1]
    mask_digits = [1, 1, 1, 1, 1, 1]
    compared_digits = [1, 0, 1, 0, 1, 1]
    assert BinaryTools.is_binary_in_range(id_digits, mask_digits, compared_digits) is True


def test_is_binary_in_range_empty_mask():
    # Test where mask_digits are all zero, meaning any compared_digits should match
    id_digits = [1, 0, 1, 0, 1, 1]
    mask_digits = [0, 0, 0, 0, 0, 0]
    compared_digits = [0, 1, 0, 1, 0, 0]
    assert BinaryTools.is_binary_in_range(id_digits, mask_digits, compared_digits) is True


def test_is_binary_in_range_invalid_length():
    # Test where input lists have different lengths
    id_digits = [1, 0, 1]
    mask_digits = [1, 1, 0, 0]
    compared_digits = [1, 0, 1]

    with pytest.raises(ValueError, match="The lengths of id_digits, mask_digits, and compared_digits must be the same."):
        BinaryTools.is_binary_in_range(id_digits, mask_digits, compared_digits)


def test_is_binary_in_range_edge_case():
    # Test edge case where all inputs are empty
    id_digits = []
    mask_digits = []
    compared_digits = []

    assert BinaryTools.is_binary_in_range(id_digits, mask_digits, compared_digits) is True
