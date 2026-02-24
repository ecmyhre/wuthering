"""
Rotten Tomatoes Verified Audience Reviews — Full Scraper
Movie: Wuthering Heights (2026)

Paginates through ALL reviews using the cursor-based 'after' param.
Output: wuthering_heights_verified_reviews.csv + .json
"""

import requests
import json
import csv
import time

# ── Cookies from browser session ─────────────────────────────
cookies = {
    'akacd_RTReplatform': '2147483647~rv=78~id=9690810e99fb548c46b3e0ff141c7698',
    'akamai_generated_location': '{"zip":"91702","city":"AZUSA","state":"CA","county":"LOSANGELES","areacode":"626","lat":"34.1312","long":"-117.9157","countrycode":"US"}',
    'eXr91Jra': 'BbvRmEOcAQAAR0dWnZjFo2v4urGxDIGcd76PFH4qL2tLaLKvCyRx1RvQhZAHJK5yZtHAf14I5--iwl4IJgAQEqAl1OxQmrGt7apK4g|1|0|f39616d7a18e85c5dba0e5cd39a60d4e4e6915eb',
    'OTGPPConsent': 'DBABLA~BVQqAAAAAACA.QA',
    '_cb': 'By-wYPBYEAV-DY1YC8',
    'usprivacy': '1YNN',
    '_ALGOLIA': 'anonymous-37547f7b-7e6f-4c3f-8bae-0ded085a1c52',
    'krg_uid': '%7B%22v%22%3A%7B%22clientId%22%3A%22cb752632-dc41-4e0e-9fda-b61d0afd8ac7%22%2C%22userId%22%3A%22e28ba08d-358a-46ce-28d0-9073c7ddb9f3%22%2C%22optOut%22%3Afalse%7D%7D',
    'krg_crb': '%7B%22v%22%3A%22eyJjbGllbnRJZCI6ImNiNzUyNjMyLWRjNDEtNGUwZS05ZmRhLWI2MWQwYWZkOGFjNyIsInRkSUQiOm51bGwsImxleElkIjoiZTI4YmEwOGQtMzU4YS00NmNlLTI4ZDAtOTA3M2M3ZGRiOWYzIiwia3RjSWQiOiI5ODRkZWIyYi1iZTM1LTAzZmQtNTI3Yy02Mzg3YWE4NjY4OTciLCJleHBpcmVUaW1lIjoxNzcxNjA4OTA0OTUyLCJsYXN0U3luY2VkQXQiOjE3NzE1MjI1MDQ5NTIsInBhZ2VWaWV3SWQiOiIiLCJwYWdlVmlld1RpbWVzdGFtcCI6MTc3MTUyMjUwMjQxNywicGFnZVZpZXdVcmwiOiJodHRwczovL3d3dy5yb3R0ZW50b21hdG9lcy5jb20vIiwidXNwIjoiMVlOTiJ9%22%7D',
    '__host_color_scheme': '1gCCbpIb-3GINlmLGNfVQENsYWJeB0IuVVrGFNlas-B_T_lexaYM',
    '__host_theme_options': '1771966362156',
    'check': 'true',
    'algoliaUT': '89e9469e-4e83-4a5b-8162-d16a0077846b',
    'AMCVS_8CF467C25245AE3F0A490D4C%40AdobeOrg': '1',
    's_cc': 'true',
    'AMCV_8CF467C25245AE3F0A490D4C%40AdobeOrg': '-408604571%7CMCMID%7C01196527463104786184199506383441324972%7CMCAAMLH-1772571170%7C7%7CMCAAMB-1772571170%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1771973570s%7CNONE%7CvVersion%7C4.6.0%7CMCIDTS%7C20509',
    'OptanonAlertBoxClosed': '2026-02-24T20:52:56.464Z',
    'OneTrustWPCCPAGoogleOptOut': 'false',
    'QSI_HistorySession': '',
    'cto_bundle': 'CLyAzV9Bb1F4QlZSRiUyRnMlMkJvSTl2UHpEQjZIc3p6amROTjdwenV6R0V1OXB0MWREVTBLOTVKc1BXd2RrTiUyRmxmQ0VYWXdaQkQlMkZlaTFhc1VEd05GNnFMQk82eEo5YjVtZmw5d0I1TTFYRjdaR0llWDBlRmFFdVhqSGU0TWUzWlVGNUhGWUxYaElGdGZZM2dUYUF5Mk5saCUyQiUyQlBwRjdvVkl6NldKV05pYVIwQUI3c25FcWxiZnV4ZUU3UlJpakxYd0RDb0NkJTJCeg',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Feb+24+2026+13%3A01%3A14+GMT-0800+(Pacific+Standard+Time)&version=202506.1.0&browserGpcFlag=0&isIABGlobal=false&identifierType=Cookie+Unique+Id&hosts=&consentId=8499220e-b36b-45df-9b89-c9707f705bab&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&GPPCookiesCount=1&gppSid=7&groups=USP%3A1%2COSSTA_BG%3A1%2C1%3A1%2C4%3A1%2C7%3A1%2COOF%3A1&iType=1&intType=1&geolocation=US%3BCA&AwaitingReconsent=false',
    'sailthru_pageviews': '5',
    '_chartbeat2': '.1758287664313.1771966874859.1100010000100001.CfUb_3Bjzacrb_IA_BqLJ5-Cm0Hrn.1',
    '_cb_svref': 'external',
    'mbox': 'PC#145e4512a53048fbbb98257ce9ae90b0.34_0#1835211676|session#445bdfe0de0140e48a6a8b96e3716528#1771968736',
    '__gads': 'ID=84ab78a5c43b19b3:T=1770660616:RT=1771966875:S=ALNI_MZQEIG-atDq4bDvhRSBO23egZHj_w',
    '__gpi': 'UID=0000137391fe6d24:T=1770660616:RT=1771966875:S=ALNI_MZyitrGyxU9iyI-BDvAkrGIGdmtXg',
    '__eoi': 'ID=12a8c2a4d42913b5:T=1770660616:RT=1771966875:S=AA-AfjZofZPqsQb1hiftKPtdeIRQ',
    '_awl': '2.1771966875.5-c2c7f3cf4fcba9418ab6822894e91eb0-6763652d75732d7765737431-0',
    's_sq': 'wbrosrottentomatoes%3D%2526c.%2526a.%2526activitymap.%2526link%253DLOAD%252520MORE%2526page%253Drt%252520%25257C%252520movies%252520%25257C%252520reviews%2526pageIDType%253D1%2526region%253Dmain-page-content%2526.activitymap%2526.a%2526.c',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.rottentomatoes.com/m/wuthering_heights_2026/reviews/verified-audience',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
}

BASE_URL = 'https://www.rottentomatoes.com/napi/rtcf/v1/movies/02331ca8-9f17-4098-ab08-d90bc8a68926/reviews'
PAGE_SIZE = 20  # RT's default; try 50 or 100 if it works


def fetch_page(after_cursor=''):
    params = {
        'after': after_cursor,
        'before': '',
        'pageCount': str(PAGE_SIZE),
        'topOnly': 'false',
        'type': 'audience',
        'verified': 'true',
    }
    resp = requests.get(BASE_URL, params=params, cookies=cookies, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


def parse_reviews(data):
    """Extract review text, timestamp, and rating from API response."""
    reviews = []
    items = data.get('reviews', data.get('results', data.get('data', [])))
    if isinstance(items, dict):
        items = items.get('reviews', [])

    for item in items:
        # Rating: RT uses 0.5-5 star scale, stored as float or integer
        rating = (
            item.get('rating') or
            item.get('score') or
            item.get('starRating') or
            item.get('userRating') or
            ''
        )
        # Normalize: if it's a dict (e.g. {value: 4.5}), extract value
        if isinstance(rating, dict):
            rating = rating.get('value') or rating.get('score') or ''

        reviews.append({
            'text': (item.get('review') or item.get('reviewText') or item.get('text') or '').strip(),
            'timestamp': (item.get('createDate') or item.get('date') or item.get('timestamp') or '').strip(),
            'rating': rating,
        })
    return reviews


def get_next_cursor(data):
    """Extract the next page cursor from response."""
    # Try common pagination shapes
    page_info = data.get('pageInfo') or data.get('pagination') or data.get('meta') or {}
    cursor = (
        page_info.get('endCursor') or
        page_info.get('nextCursor') or
        page_info.get('after') or
        data.get('nextPageCursor') or
        data.get('cursor') or
        data.get('after') or
        ''
    )
    has_next = (
        page_info.get('hasNextPage') or
        page_info.get('hasMore') or
        data.get('hasNextPage') or
        data.get('hasMore') or
        False
    )
    return cursor, has_next


def scrape_all():
    all_reviews = []
    cursor = ''  # Start from beginning (no cursor = first page)
    page = 1

    print(f"Starting scrape — {BASE_URL}")
    print(f"Page size: {PAGE_SIZE} reviews per request\n")

    while True:
        print(f"  Fetching page {page} (cursor: {cursor[:40] + '...' if len(cursor) > 40 else cursor or 'START'})...")

        try:
            data = fetch_page(after_cursor=cursor)
        except requests.HTTPError as e:
            print(f"  HTTP error: {e}")
            if e.response.status_code == 401:
                print("  ⚠️  Session expired — cookies need refreshing. Re-run the intercept.")
            break
        except Exception as e:
            print(f"  Error: {e}")
            break

        # Debug: print raw keys on first page
        if page == 1:
            print(f"  Response keys: {list(data.keys())}")
            # Save raw first response for inspection
            with open('first_page_raw.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("  Saved first_page_raw.json for inspection")

        reviews = parse_reviews(data)
        if not reviews:
            print(f"  No reviews found in response. Stopping.")
            break

        all_reviews.extend(reviews)
        print(f"  Got {len(reviews)} reviews → Total: {len(all_reviews)}")

        cursor, has_next = get_next_cursor(data)

        if not has_next and not cursor:
            print(f"\n  ✅ Reached last page.")
            break

        page += 1
        time.sleep(1)  # be polite

    return all_reviews


def save(reviews, base='wuthering_heights_verified_reviews'):
    if not reviews:
        print("No reviews to save.")
        return

    # CSV
    csv_path = f'{base}.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'timestamp', 'rating'])
        writer.writeheader()
        writer.writerows(reviews)

    # JSON
    json_path = f'{base}.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*55}")
    print(f"✅  Saved {len(reviews)} reviews")
    print(f"    CSV  → {csv_path}")
    print(f"    JSON → {json_path}")
    print(f"{'='*55}")

    # Preview
    print("\n── Sample ──")
    for r in reviews[:3]:
        print(f"  ⭐ {r['rating']}  📅 {r['timestamp']}")
        print(f"  \"{r['text'][:100]}\"")
        print()


if __name__ == '__main__':
    reviews = scrape_all()
    save(reviews)
