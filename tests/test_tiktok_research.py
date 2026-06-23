from datetime import date

from app.collectors.tiktok_research import TikTokQueryWindow, TikTokResearchCollector
from app.seeds.sources import default_tiktok_sources


def test_builds_official_keyword_query_with_kz_region() -> None:
    collector = TikTokResearchCollector(token="token", region_code="KZ", max_count=100)
    body = collector.build_query_body(
        field_name="keyword",
        field_value="казино онлайн",
        window=TikTokQueryWindow(start_date=date(2026, 6, 1), end_date=date(2026, 6, 23)),
    )

    assert body == {
        "query": {
            "and": [
                {"operation": "IN", "field_name": "region_code", "field_values": ["KZ"]},
                {"operation": "EQ", "field_name": "keyword", "field_values": ["казино онлайн"]},
            ]
        },
        "start_date": "20260601",
        "end_date": "20260623",
        "max_count": 100,
        "is_random": False,
    }


def test_builds_official_hashtag_query_without_hash_prefix() -> None:
    collector = TikTokResearchCollector(token="token", region_code="KZ", max_count=50)
    body = collector.build_query_body(
        field_name="hashtag_name",
        field_value="онлайнказино",
        window=TikTokQueryWindow(start_date=date(2026, 6, 1), end_date=date(2026, 6, 7)),
        cursor=100,
        search_id="search-id",
    )

    assert body["query"]["and"][1] == {
        "operation": "EQ",
        "field_name": "hashtag_name",
        "field_values": ["онлайнказино"],
    }
    assert body["cursor"] == 100
    assert body["search_id"] == "search-id"
    assert body["max_count"] == 50


def test_default_tiktok_sources_are_kz_only() -> None:
    sources = default_tiktok_sources()

    assert sources
    assert {source["platform"] for source in sources} == {"tiktok"}
    assert {source["region_code"] for source in sources} == {"KZ"}
    assert {"keyword", "hashtag"} <= {source["source_type"] for source in sources}
