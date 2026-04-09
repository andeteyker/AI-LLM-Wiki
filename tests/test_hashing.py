from llm_wiki.utils import sha256_bytes


def test_sha256_stable():
    a = sha256_bytes(b"hello")
    b = sha256_bytes(b"hello")
    c = sha256_bytes(b"hello2")
    assert a == b
    assert a != c
