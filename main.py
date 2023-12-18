import requests
from bs4 import BeautifulSoup


def main() -> None:
    url = "https://realpython.github.io/fake-jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.prettify())


if __name__ == "__main__":
    main()
