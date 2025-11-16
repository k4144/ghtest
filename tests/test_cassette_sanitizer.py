import json
from pathlib import Path

import yaml

from ghtest import cassette_sanitizer


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_sanitize_masks_auth_headers_and_identifiers(tmp_path):
    cassette = {
        "interactions": [
            {
                "request": {
                    "headers": {
                        "Authorization": ["token ghp_realSecretValue"],
                    },
                    "body": {"string": json.dumps({"name": "SensitiveRepo"})},
                },
                "response": {
                    "headers": {
                        "X-GitHub-OTP": ["123456"],
                    },
                    "body": {
                        "string": json.dumps(
                            {
                                "owner": {"login": "real-user", "id": 123456},
                                "full_name": "real-user/private",
                                "node_id": "abc123",
                                "html_url": "https://github.com/real-user/private",
                            }
                        )
                    },
                },
            }
        ]
    }
    cassette_path = tmp_path / "cassette.yaml"
    cassette_path.write_text(yaml.safe_dump(cassette, sort_keys=False), encoding="utf-8")

    changed = cassette_sanitizer.sanitize_file(cassette_path)
    assert changed

    sanitized = _load_yaml(cassette_path)
    request_headers = sanitized["interactions"][0]["request"]["headers"]["Authorization"][0]
    assert request_headers.startswith("token ")
    masked_token = request_headers.split(" ", 1)[1]
    assert set(ch for ch in masked_token if ch.isalnum()) == {"x"}

    response_headers = sanitized["interactions"][0]["response"]["headers"]["X-GitHub-OTP"][0]
    assert set(ch for ch in response_headers if ch.isalnum()) == {"x"}

    body = json.loads(sanitized["interactions"][0]["response"]["body"]["string"])
    assert body["full_name"] != "real-user/private"
    assert body["owner"]["login"] != "real-user"
    assert body["owner"]["id"] != 123456
    assert "node_id" not in body
    assert "html_url" not in body


def test_dry_run_does_not_modify_files(tmp_path):
    cassette = {
        "interactions": [
            {
                "request": {
                    "headers": {"Authorization": ["Bearer realtoken"]},
                }
            }
        ]
    }
    cassette_path = tmp_path / "c.yaml"
    cassette_path.write_text(yaml.safe_dump(cassette), encoding="utf-8")
    changed = cassette_sanitizer.sanitize_file(cassette_path, dry_run=True)
    assert changed  # sanitizer detected sensitive data
    assert _load_yaml(cassette_path) == cassette
