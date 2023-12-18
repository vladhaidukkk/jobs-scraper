import datetime
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup, Tag


@dataclass(slots=True, frozen=True)
class Job:
    title: str
    company: str
    location: str
    date: datetime.date
    link: str


def extract_job(card: Tag) -> Job:
    title = card.find("h2", class_="title")
    assert title is not None, "title not found"

    company = card.find("h3", class_="company")
    assert company is not None, "company not found"

    location = card.find("p", class_="location")
    assert location is not None, "location not found"

    date = card.find("time")
    assert date is not None, "date not found"

    link: Tag = card.find_all("a")[1]
    href = link["href"]
    assert isinstance(href, str)

    return Job(
        title=title.text.strip(),
        company=company.text.strip(),
        location=location.text.strip(),
        date=datetime.date.fromisoformat(date.text.strip()),
        link=href,
    )


def main() -> None:
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    container = soup.find(id="ResultsContainer")
    assert isinstance(container, Tag), "#ResultsContainer not found"

    cards: list[Tag] = container.find_all("div", class_="card")
    jobs = [extract_job(card) for card in cards]

    for job in jobs:
        print(job)


if __name__ == "__main__":
    main()
