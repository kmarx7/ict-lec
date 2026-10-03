import pytest

from src.sources.zoom.url_parser import ZoomURLParser


@pytest.mark.parametrize("url", [
    "https://zoom.us/rec/share/abc",
    "https://us06web.zoom.us/rec/play/xyz?pwd=opaque",
])
def test_valid_zoom_urls(url):
    assert ZoomURLParser().parse(url).canonical_url == url


@pytest.mark.parametrize("url", [
    "https://zoom.us.attacker.com/rec/share/x",
    "https://fakezoom.us/rec/share/x",
    "http://zoom.us/rec/share/x",
    "https://zoom.us/j/123",
])
def test_rejects_untrusted_or_unsupported_urls(url):
    with pytest.raises(ValueError):
        ZoomURLParser().parse(url)


def test_extracts_origin_request_url():
    url = "https://zoom.us/rec/play/wrapper?originRequestUrl=https%3A%2F%2Fus02web.zoom.us%2Frec%2Fshare%2Foriginal"
    assert ZoomURLParser().parse(url).canonical_url.endswith("/rec/share/original")

