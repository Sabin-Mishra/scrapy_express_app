import scrapy
import json
from datetime import datetime
from scrapy.crawler import CrawlerProcess


class StmoritzSpider(scrapy.Spider):
    name = "stmoritz"
    # allowed_domains = ["booking.stmoritz.com"]
    # start_urls = ["https://booking.stmoritz.com/skitickets/tickettypes"]

    custom_settings = {
        # 'JOBDIR': f'./crawls/{name}', # for resuming of crawlers or to save the scraped state
        'CONCURRENT_REQUESTS': 1,
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_DELAY':0.5,
        'RETRY_TIMES':5,
        'RETRY_HTTP_CODES' : [500, 502, 503, 504, 400, 403, 404, 408, 416],

        'FEED_FORMAT': 'json',
        'FEED_URI': 'scraped_data/' + datetime.now().strftime('%Y_%m_%d__%H_%M_%S') + f'{name}.json',
        # 'FEED_URI' : 'output.json'

        # 'ITEM_PIPELINES': {
        #     '__main__.PostgresPipeline': 300,
        # },


        # 'CLOSESPIDER_ITEMCOUNT': 100,
        'LOG_FILE': 'scrapy_log.txt',
        'LOG_LEVEL': 'DEBUG',  # You can adjust the log level as needed
    }

    headers = {
    'authority': 'api.laax.com',
    'accept': '*/*',
    'accept-language': 'en',
    'authorization': 'Bearer eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5sYWF4LmNvbS8ifQ..tpP4axTjhHQCGUtG.7UWwK6U4vfgcJVdGEuz92lFZoxfXmaKyXX9gJwjBFMumivKvnwcK3x-bWD8mxUtJPlLjxbQiImV01jH1WAHTSCQlF0NflYPhCbMcMr6LEh-ct87g1Rz8M3VjFkzkozU34ZlYPb00M1kdW9rAlVfQEzzeyQRRPc0QdMlDtNFkbISMgvb0Hvss69jXi_ZcCIT7XrvqclLinIbJ4brkXJjxC6nuGZfoY-EYDIU_fgBd3a0f1RTIFuiWAPyDblLqugtw2-04XYHR6gsxpywX0V3lGx0CdwBWIo9F3VwdDOSwF5jXHrltH9_vs-pMZtH9e4vHyqPAHmFjpJTXaaOh0j_p7dsqjICI.yx7D0-TUDisSohpVpo-HUQ',
    'content-type': 'application/json',
    'origin': 'https://tickets.laax.com',
    'referer': 'https://tickets.laax.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'tickets-laax': 'webshop2',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Cookie': 'AWSALB=EwtqfHStq5kvIkI+wNsoY8paRV9/0sHIFCxumfcO7Gz2HLmZOs5Be9V0QTpkg618UI1h1pgqZ4VzeI5sdm3O+QWAulvgtVNbdZ5Mh2/W8DrfnGN/ebk41nXbDrVX; AWSALBCORS=EwtqfHStq5kvIkI+wNsoY8paRV9/0sHIFCxumfcO7Gz2HLmZOs5Be9V0QTpkg618UI1h1pgqZ4VzeI5sdm3O+QWAulvgtVNbdZ5Mh2/W8DrfnGN/ebk41nXbDrVX'
    }

    def start_requests(self):
        url = 'https://api.laax.com/'
        # payload = "{\"query\":\"query GetCalendarForPersonTypes($input: PersonTypeLoadCalendarInput!) {\\n  shopLoadCalendarForPersonTypes(input: $input) {\\n    dates {\\n      date\\n      price\\n      availability\\n      __typename\\n    }\\n    messages {\\n      name\\n      text\\n      icon\\n      style\\n      type\\n      behavior\\n      __typename\\n    }\\n    birthDates\\n    __typename\\n  }\\n}\\n\",\"variables\":{\"input\":{\"productId\":\"day-pass-eco-1\",\"personTypes\":[]}}}"
        payload = "{\"query\":\"query GetBasePriceFromOfferDraftForPersonTypes($input: PersonTypeLoadOfferSummaryInput!) {\\n  shopLoadOfferDraftForPersonTypes(input: $input) {\\n    basePrice\\n    addons {\\n      id\\n      summaryPrice\\n      totalPrice\\n      summaryPriceType\\n      quantityAvailable\\n      __typename\\n    }\\n    upgrades {\\n      id\\n      summaryPrice\\n      totalPrice\\n      summaryPriceType\\n      quantityAvailable\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\",\"variables\":{\"input\":{\"startDate\":\"2023-11-18\",\"endDate\":\"2023-11-18\",\"productId\":\"day-pass-eco-1\",\"personTypes\":[\"adult-v2-all-1\"]}}}"
        payload_data = json.loads(payload)
        date_ = datetime.now().strftime('%Y-%m-%d')
        payload_data['variables']['input']['startDate'] = date_
        payload_data['variables']['input']['endDate'] = date_

        new_payload = json.dumps(payload_data)
        print("---------------------------------|||||||||||||||||||||||||||||")
        yield scrapy.Request(
            url=url,
            method='POST',
            dont_filter=True,
            headers=self.headers,
            body = new_payload,
            callback=self.parse,
            meta={
                # 'proxy': PROXY,
                'date': date_
            }
        )

    def parse(self,response):
        data = json.loads(response.text)
        price = data['data']['shopLoadOfferDraftForPersonTypes']['basePrice']
        if price == None:
            price = 0
        else: price = price / 100
        print('-----------------||||||||||||||||||||||||||||||||||||||||||||')
        print("Scrapy script completed... ")
        yield{
            "skigebiet" : 'Laax',
            "preis":price,
            "valid_date": response.meta['date'].replace('-','/'),
            "scraped_at":datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        }
settings = {
    'USER_AGENT': 'your_user_agent',
    # Other settings like FEED_EXPORT, ITEM_PIPELINES, etc.
}

# Create a CrawlerProcess with the settings
process = CrawlerProcess(settings=settings)

# Add the spider to the process
process.crawl(StmoritzSpider)

# Start the crawling process
process.start()