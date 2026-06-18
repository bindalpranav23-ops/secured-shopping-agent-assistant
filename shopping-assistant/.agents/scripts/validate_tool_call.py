import sys
import json
import re

def main():
    try:
        input_data = sys.stdin.read()
    except Exception as e:
        print(f"Error reading stdin: {e}", file=sys.stderr)
        sys.exit(1)

    if not input_data.strip():
        print("Approval: Empty tool call input, allowing.")
        sys.exit(0)

    try:
        tool_call = json.loads(input_data)
    except json.JSONDecodeError:
        tool_call = {}

    # Extract command string
    command = ""
    if isinstance(tool_call, dict):
        arguments = tool_call.get("arguments", {})
        if isinstance(arguments, dict):
            command = arguments.get("CommandLine", "")
        if not command:
            command = tool_call.get("CommandLine", "")

    # Fallback to scanning raw input string if no command was parsed
    if not command:
        command = input_data

    # Destructive pattern detection (case-insensitive)
    destructive_patterns = [
        r"rm\s+-rf\s+/",
        r"rm\s+-rf\s+/\*",
        r"rm\s+-rf\s+[a-zA-Z]:\\",
        r"rmdir\s+/s\s+/q\s+/",
        r"rmdir\s+/s\s+/q\s+[a-zA-Z]:\\",
        r"del\s+/s\s+/q\s+[a-zA-Z]:\\",
        r"format\s+[a-zA-Z]:"
    ]

    for pattern in destructive_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            print(f"Violation: Destructive command detected in tool call: '{command.strip()}'", file=sys.stderr)
            sys.exit(1)

    # Clean up display of command
    cleaned_cmd = command.strip().replace("\n", " ")
    print(f"Approval: Tool call looks safe: '{cleaned_cmd[:100]}'")
    sys.exit(0)

if __name__ == "__main__":
    main()
