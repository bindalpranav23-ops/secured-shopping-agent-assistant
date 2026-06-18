# ruff: noqa
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

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from functools import cached_property
from google.genai import Client

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


class CustomGemini(Gemini):
    api_key: str | None = None

    @cached_property
    def api_client(self) -> Client:
        api_key = self.api_key or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is required.")
        return Client(api_key=api_key)


# In-memory store for registered user IDs and discount codes
REGISTERED_USER_IDS = {"user123", "user_kaggle", "customer_456"}
VALID_DISCOUNT_CODES = {"WELCOME50", "SUMMER20"}
REDEEMED_DISCOUNT_CODES = set()


def redeem_discount_code(user_id: str, code: str) -> str:
    """Redeems a single-use discount code for a registered user ID.

    Args:
        user_id: The ID of the registered user.
        code: The discount code to redeem (e.g., WELCOME50, SUMMER20).

    Returns:
        A string indicating if the discount code was successfully redeemed or why it failed.
    """
    global REDEEMED_DISCOUNT_CODES

    if not user_id or user_id not in REGISTERED_USER_IDS:
        return f"Error: '{user_id}' is not a registered user ID."

    normalized_code = code.strip().upper()
    if normalized_code not in VALID_DISCOUNT_CODES:
        return f"Error: Discount code '{code}' is invalid."

    if normalized_code in REDEEMED_DISCOUNT_CODES:
        return f"Error: Discount code '{code}' has already been redeemed."

    REDEEMED_DISCOUNT_CODES.add(normalized_code)
    return f"Success: Discount code '{normalized_code}' has been successfully redeemed for user '{user_id}'."


root_agent = Agent(
    name="root_agent",
    model=CustomGemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful AI shopping assistant for our retail store. Assist customers with their shopping needs and help them redeem discount codes using the provided tool.",
    tools=[redeem_discount_code],
)

app = App(
    root_agent=root_agent,
    name="app",
)
