# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
You can add your unit tests here.
This is where you test your business logic, including agent functionality,
data processing, and other core components of your application.
"""

from app.agent import REDEEMED_DISCOUNT_CODES, redeem_discount_code


def test_redeem_discount_code_success() -> None:
    # Clear redeemed codes
    REDEEMED_DISCOUNT_CODES.clear()

    # Test successful redemption for a registered user ID and valid code
    user_id = "user123"
    code = "WELCOME50"

    result = redeem_discount_code(user_id, code)
    assert "Success" in result
    assert "WELCOME50" in result
    assert "user123" in result
    assert "WELCOME50" in REDEEMED_DISCOUNT_CODES


def test_redeem_discount_code_invalid_user() -> None:
    REDEEMED_DISCOUNT_CODES.clear()

    # Test unregistered user ID
    user_id = "invalid_user"
    code = "WELCOME50"

    result = redeem_discount_code(user_id, code)
    assert "Error" in result
    assert "invalid_user" in result
    assert "WELCOME50" not in REDEEMED_DISCOUNT_CODES


def test_redeem_discount_code_invalid_code() -> None:
    REDEEMED_DISCOUNT_CODES.clear()

    # Test invalid discount code
    user_id = "user123"
    code = "INVALIDCODE"

    result = redeem_discount_code(user_id, code)
    assert "Error" in result
    assert "INVALIDCODE" in result
    assert "INVALIDCODE" not in REDEEMED_DISCOUNT_CODES


def test_redeem_discount_code_already_redeemed() -> None:
    REDEEMED_DISCOUNT_CODES.clear()

    user_id = "user123"
    code = "WELCOME50"

    # First redemption should succeed
    result1 = redeem_discount_code(user_id, code)
    assert "Success" in result1

    # Second redemption of same code should fail
    result2 = redeem_discount_code(user_id, code)
    assert "Error" in result2
    assert "already been redeemed" in result2
