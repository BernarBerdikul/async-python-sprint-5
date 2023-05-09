from src.models import ShortUrl
from factory import Faker, Factory


class ShortUrlFactory(Factory):
    """Short URL factory."""

    class Meta:
        model = ShortUrl

    original_url = Faker("url")
    short_url = Faker("pystr", min_chars=15, max_chars=20)
    is_removed = False
    usage_count = 0
