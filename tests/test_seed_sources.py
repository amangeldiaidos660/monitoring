from app.seeds.sources import default_tiktok_sources


def test_default_sources_have_no_duplicates() -> None:
    sources = default_tiktok_sources()
    identities = {(source["source_type"], source["platform"], source["value"]) for source in sources}

    assert len(identities) == len(sources)
