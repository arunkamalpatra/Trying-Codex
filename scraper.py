from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://tendersodisha.gov.in/nicgep/app"
LATEST_TENDERS_URL = f"{BASE_URL}?page=FrontEndLatestActiveTenders&service=page"


@dataclass
class Tender:
    title: str
    reference_no: str
    closing_date: str
    department: str
    location: str
    link: str


def _extract_table_rows(html: str) -> List[Tender]:
    soup = BeautifulSoup(html, "lxml")
    rows = soup.select("table.list_table tr")

    tenders: List[Tender] = []
    for row in rows:
        columns = row.find_all("td")
        if len(columns) < 5:
            continue

        title_anchor = columns[0].find("a")
        title = title_anchor.get_text(" ", strip=True) if title_anchor else columns[0].get_text(" ", strip=True)
        href = title_anchor.get("href", "") if title_anchor else ""
        if href and href.startswith("/"):
            href = f"https://tendersodisha.gov.in{href}"

        tender = Tender(
            title=title,
            reference_no=columns[1].get_text(" ", strip=True),
            closing_date=columns[2].get_text(" ", strip=True),
            department=columns[3].get_text(" ", strip=True),
            location=columns[4].get_text(" ", strip=True),
            link=href,
        )
        tenders.append(tender)

    return tenders


def fetch_tenders_for_district(district: str = "Nabarangpur") -> List[dict]:
    session = requests.Session()
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
    }

    response = session.get(LATEST_TENDERS_URL, headers=headers, timeout=30)
    response.raise_for_status()

    all_tenders = _extract_table_rows(response.text)
    district_norm = district.strip().lower()

    filtered = [
        asdict(t)
        for t in all_tenders
        if district_norm in t.location.lower()
        or district_norm in t.department.lower()
        or district_norm in t.title.lower()
    ]

    return filtered
