import pytest

from app.agent import (
    REDEEMED_DISCOUNT_CODES,
    redeem_discount_code,
)


@pytest.fixture(autouse=True)
def reset_redeemed_discount_codes():
    """Reset in-memory discount redemption state before and after each test."""
    REDEEMED_DISCOUNT_CODES.clear()
    yield
    REDEEMED_DISCOUNT_CODES.clear()


def test_valid_discount_code_redeems_successfully():
    """A registered user can redeem a valid discount code."""
    result = redeem_discount_code("user123", "WELCOME50")

    assert "Success" in result
    assert "WELCOME50" in REDEEMED_DISCOUNT_CODES


def test_same_discount_code_cannot_be_redeemed_twice():
    """A single-use discount code cannot be redeemed more than once."""
    first_result = redeem_discount_code("user123", "WELCOME50")
    second_result = redeem_discount_code("customer_456", "WELCOME50")

    assert "Success" in first_result
    assert "already been redeemed" in second_result
    assert "WELCOME50" in REDEEMED_DISCOUNT_CODES


def test_invalid_discount_code_is_rejected():
    """Unknown discount codes are rejected."""
    result = redeem_discount_code("user123", "INVALID99")

    assert "invalid" in result.lower()
    assert "INVALID99" not in REDEEMED_DISCOUNT_CODES


def test_unregistered_user_cannot_redeem_code():
    """Unregistered users cannot redeem valid discount codes."""
    result = redeem_discount_code("unknown_user", "SUMMER20")

    assert "not a registered user ID" in result
    assert "SUMMER20" not in REDEEMED_DISCOUNT_CODES


def test_discount_code_is_normalized_before_redemption():
    """Discount codes are normalized using strip and uppercase."""
    result = redeem_discount_code("customer_456", " summer20 ")

    assert "Success" in result
    assert "SUMMER20" in REDEEMED_DISCOUNT_CODES
