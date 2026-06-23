KZ_KEYWORDS_RU = [
    "казино онлайн",
    "онлайн казино",
    "казино казахстан",
    "ставки на спорт",
    "букмекер",
    "депозит",
    "бонус за регистрацию",
    "быстрый заработок",
    "заработок онлайн",
    "гарантированный доход",
    "пассивный доход",
    "доход без риска",
    "инвестируй сейчас",
    "инвестиции с гарантией",
    "реферальная ссылка",
    "пригласи друга",
    "финансовая пирамида",
    "удвой депозит",
    "вывод денег",
]

KZ_KEYWORDS_KK_CYR = [
    "қазақстан казино",
    "спортқа бәс тігу",
    "тіркелу бонусы",
    "тез табыс",
    "онлайн табыс",
    "кепілді табыс",
    "пассивті табыс",
    "тәуекелсіз табыс",
    "қазір инвестиция жаса",
    "кепілді инвестиция",
    "реферал сілтеме",
    "досыңды шақыр",
    "қаржы пирамидасы",
    "ақша шығару",
]

KZ_KEYWORDS_KK_LAT = [
    "onlain kazino",
    "qazaqstan kazino",
    "sportqa bas tigu",
    "tez tabys",
    "onlain tabys",
    "kepildi tabys",
    "passivti tabys",
    "tauekelsiz tabys",
    "qazir investiciya jasa",
    "referal silteme",
    "dosyndy shaqyr",
    "qarzhy piramidasy",
    "aqsha shygaru",
]

KZ_HASHTAGS = [
    "казино",
    "онлайнказино",
    "казиноказахстан",
    "ставки",
    "букмекер",
    "заработок",
    "заработоконлайн",
    "гарантированныйдоход",
    "пассивныйдоход",
    "инвестиции",
    "реферал",
    "қазақстанказино",
    "бәстігу",
    "табыс",
    "онлайнтабыс",
    "кепілдітабыс",
    "пассивтітабыс",
    "қаржыпирамидасы",
    "ақшашығару",
]

KZ_REGION_MARKERS = [
    "казахстан",
    "қазақстан",
    "qazaqstan",
    "алматы",
    "астана",
    "шымкент",
    "қарағанды",
    "караганда",
    "ақтөбе",
    "актобе",
    "атырау",
    "ақтау",
    "актау",
    "kaspi",
    "halyk",
    "forte",
    "jusan",
    "bcc",
    "+7 7",
]


def default_tiktok_sources() -> list[dict[str, str]]:
    keyword_sources = [
        {"source_type": "keyword", "platform": "tiktok", "value": keyword, "region_code": "KZ"}
        for keyword in KZ_KEYWORDS_RU + KZ_KEYWORDS_KK_CYR + KZ_KEYWORDS_KK_LAT
    ]
    hashtag_sources = [
        {"source_type": "hashtag", "platform": "tiktok", "value": hashtag, "region_code": "KZ"}
        for hashtag in KZ_HASHTAGS
    ]
    return keyword_sources + hashtag_sources
