from app.core.security import create_access_token, decode_token


def test_token_roundtrip() -> None:
    token = create_access_token("admin")
    subject = decode_token(token)
    assert subject == "admin"
