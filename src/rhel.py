import re
from bs4 import BeautifulSoup
from common import dates
from common import endoflife
from common import http

# https://regex101.com/r/877ibq/1
VERSION_PATTERN = re.compile(r"RHEL (?P<major>\d)(\. ?(?P<minor>\d+))?(( Update (?P<minor2>\d))| GA)?")

product = endoflife.Product("redhat")
print(f"::group::{product.name}")
response = http.fetch_url("https://access.redhat.com/articles/3078")
soup = BeautifulSoup(response.text, features="html5lib")

for tr in soup.findAll("tr"):
    td_list = tr.findAll("td")
    if len(td_list) == 0:
        continue

    version_str = td_list[0].get_text().strip()
    version_match = VERSION_PATTERN.match(version_str).groupdict()
    version = version_match["major"]
    version += ("." + version_match["minor"]) if version_match["minor"] else ""
    version += ("." + version_match["minor2"]) if version_match["minor2"] else ""
    date = dates.parse_date(td_list[1].get_text())

    product.declare_version(version, date)

product.write()
print("::endgroup::")
