# Import necessary libraries
import requests
from bs4 import BeautifulSoup

# Define the base URL for web scraping
base = "https://www.bhphotovideo.com/c/buy/laptops/ci/18818"

# Define sorting types available on the website
sorttypes = [
    "SORT_FEATURED",
    "SORT_BEST_SELLERS",
    "SORT_PRICE_LOW_TO_HIGH",
    "SORT_PRICE_HIGH_TO_LOW",
    "SORT_TOP_RATED",
    "SORT_MOST_RATED",
    "SORT_BRAND_A_TO_Z",
    "SORT_BRAND_Z_TO_A",
    "SORT_NEWEST",
]


# Define lambda functions to construct URLs for search, sort, and pagination
search = lambda uri, keyword: (
    f"{uri}?searchWithin={keyword}"
    if "?" not in uri
    else f"{uri}&searchWithin={keyword}"
)
sort = lambda uri, keyword: (
    f"{uri}?sort={keyword[5:]}" if "?" not in uri else f"{uri}&sort={keyword[5:]}"
)
page = lambda uri, keyword: f"{uri}/pn/{keyword}"


# Define a Laptop class to represent laptop information
class Laptop:
    def __init__(
        self,
        name: str,
        price: str,
        features: list[str],
        rating: float | None = None,
        count: int | None = None,
    ):
        self.name = name
        self.price = price
        self.features = features
        self.rating = rating
        self.count = count

    def __str__(self):
        return (
            f"\n[-] Name: {self.name}\n    Price: {self.price}\n\n    Features:\n    - {'\n    - '.join(self.features)}\n"
            + (
                f"\n    Rating: {self.rating}/5 ({self.count} reviews)\n"
                if self.rating is not None
                else ""
            )
        )

    __repr__ = __str__


# Function to parse the HTML response and extract laptop information
def parse_index(response: requests.Response):
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("div", {"data-selenium": "miniProductPage"})

    for row in rows:
        rating = row.find("div", {"data-selenium": "ratingContainer"})

        if rating is not None:
            total = 0
            count = row.find(
                "span", {"data-selenium": "miniProductPageProductReviews"}
            ).text
            for item in rating.find_all("use"):
                if item["href"] == "#StarIcon":
                    total += 1
                elif item["href"] == "#StarHalfIcon":
                    total += 0.5
            rating = total
        else:
            count = None

        laptop = Laptop(
            name=row.find("span", {"data-selenium": "miniProductPageProductName"}).text,
            price=row.find("span", {"data-selenium": "uppedDecimalPriceFirst"}).text,
            features=[
                item.text
                for item in row.find_all(
                    "li", {"data-selenium": "miniProductPageSellingPointsListItem"}
                )
            ],
            rating=rating,
            count=count,
        )

        yield laptop


# Function to fetch the webpage based on the provided parameters (pagination, search, sorting)
def fetch(
    base: str,
    page_keyword: str | None = None,
    search_keyword: str | None = None,
    sort_keyword: str | None = None,
) -> requests.Response:
    if page_keyword is not None:
        base = page(base, page_keyword)

    if search_keyword is not None:
        base = search(base, search_keyword)

    if sort_keyword is not None:
        base = sort(base, sort_keyword)

    return requests.get(
        base,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
        },
    )
