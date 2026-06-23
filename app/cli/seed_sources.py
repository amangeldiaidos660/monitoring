from app.db.session import SessionLocal
from app.repositories.sources import seed_tiktok_sources


def main() -> None:
    with SessionLocal() as session:
        inserted = seed_tiktok_sources(session)
    print(f"Inserted {inserted} TikTok sources")


if __name__ == "__main__":
    main()
