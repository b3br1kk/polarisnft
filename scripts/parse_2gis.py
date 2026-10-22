#!/usr/bin/env python3
"""Раз в сутки берёт со страницы организации в 2ГИС рейтинг, число оценок и число отзывов
и записывает их в data/rating.json. Без API-ключа, только стандартная библиотека Python."""
import datetime
import html
import json
import pathlib
import re
import sys
import urllib.request

FIRM_ID = "70000001006653739"          # номер организации из ссылки 2ГИС
CITY = "nefteyugansk"
URLS = [
    f"https://2gis.ru/{CITY}/firm/{FIRM_ID}/tab/reviews",
    f"https://2gis.ru/{CITY}/firm/{FIRM_ID}",
]
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "rating.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.9",
}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(raw):
    """Ищет цифры в описании страницы (meta description) и в её тексте."""
    t = html.unescape(raw).replace("\xa0", " ")
    out = {}
    # «74 отзыва о ... Рейтинг 4.8 на основе 107 оценок»
    m = re.search(r"Рейтинг\s+([0-5](?:[.,]\d)?)\s+на основе\s+(\d+)\s+оцен", t)
    if m:
        out["rating"], out["ratings"] = float(m.group(1).replace(",", ".")), int(m.group(2))
    m = re.search(r"(\d+)\s+отзыв\w*\s+о\s", t)
    if m:
        out["reviews"] = int(m.group(1))
    # запасные варианты: «Оценка 4.8, 30 фото, 74 отзыва»
    if "rating" not in out:
        m = re.search(r"Оценка\s+([0-5](?:[.,]\d)?)", t)
        if m:
            out["rating"] = float(m.group(1).replace(",", "."))
    if "reviews" not in out:
        m = re.search(r"Оценка[^\n]{0,80}?(\d+)\s+отзыв", t)
        if m:
            out["reviews"] = int(m.group(1))
    if "ratings" not in out:
        m = re.search(r"(\d+)\s+оцен(?:ка|ки|ок)\b", t)
        if m:
            out["ratings"] = int(m.group(1))
    return out


def main():
    found, errors = {}, []
    for url in URLS:
        try:
            for k, v in parse(fetch(url)).items():
                found.setdefault(k, v)
        except Exception as e:  # сеть, блокировка, 403 и т.д.
            errors.append(f"{url}: {e}")
        if {"rating", "ratings", "reviews"} <= found.keys():
            break

    if "rating" not in found or not ({"ratings", "reviews"} & found.keys()):
        print("Не удалось получить данные с 2ГИС (страница недоступна или изменилась):", *errors, found, sep="\n  ")
        return 1

    old = json.loads(OUT.read_text("utf-8")) if OUT.exists() else {}
    new = {k: found.get(k, old.get(k)) for k in ("rating", "ratings", "reviews")}

    if not all(isinstance(new[k], (int, float)) for k in new) or not 1 <= new["rating"] <= 5:
        print("Не удалось получить данные с 2ГИС:", *errors, found, sep="\n  ")
        return 1
    missing = [k for k in ("rating", "ratings", "reviews") if k not in found]
    if missing:
        print("Предупреждение: не нашёл", missing, "— оставил прежние значения")

    if all(old.get(k) == new[k] for k in new):
        print("Без изменений:", new)
        return 0
    new["updated"] = datetime.date.today().isoformat()
    new["source"] = f"https://2gis.ru/{CITY}/firm/{FIRM_ID}"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(new, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print("Обновлено:", new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
