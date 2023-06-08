import scrapy
from scrapy.http import Response
import requests
from PIL import Image
import os


def download_image(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


class SpiderWinesSpider(scrapy.Spider):
    name = "spider-wines"
    allowed_domains = ["vino.ua"]

    def start_requests(self):
        for i in range(1, 2):
            url = f"https://vino.ua/ua/vino/filter/page={i}/"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs):
        hrefs = response.css('.catalogCard-main .catalogCard-view a::attr(href)').getall()
        for href in hrefs:
            yield response.follow(href, self.parse_wine)

    @staticmethod
    def parse_wine(response: Response):
        filename = f"wines.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        data = {}

        rows = response.css('table.product-features__table tr')

        for row in rows:
            header = row.css('th::text').get()
            cell = row.css('td')
            print("cell=",  cell)

            if len(cell) > 0:
                if cell.css('a'):
                    value = cell.css('a::text').get()
                    print("value with a=",  value)
                else:
                    value = cell.css('td::text').get()
                    print("value=",  value)

            if header and value:
                header = header.strip()
                value = value.strip()

                if header == "Назва укр.":
                    data["name"] = value
                if header == "Колір":
                    data["color"] = value
                if header == "Тип":
                    data["wine_type"] = value
                if header == "Бренд":
                    data["brand"] = value
                if header == "Літраж":
                    data["capacity"] = value
                if header == "В ящику шт.":
                    data["in_box"] = value
                if header == "Упаковка":
                    data["package"] = value
                if header == "Міцність":
                    data["alcohol_percentage"] = value
                if header == "Країна":
                    data["country"] = value
                if header == "Регіон":
                    data["region"] = value
                if header == "Виробник":
                    data["producer"] = value
                if header == "Форма келиху":
                    data["glass"] = value
                if header == "Подавати за температури, С":
                    data["temperature"] = value
                if header == "Гастрономічне поєднання":
                    data["gastronomic_combination"] = value
                if header == "Виноград":
                    data["grape"] = value
                if header == "Вінтаж":
                    data["vintage"] = value
                if header == "Чи потрібна декантація":
                    data["decantation"] = value
                if header == "Діаметр пляшки":
                    data["diameter"] = value
                if header == "Постачальник":
                    data["supplier"] = value

        image_url = response.css('span.gallery__link::attr(data-href)').get()
        data["image_url"] = "https://vino.ua/" + image_url
        filename = os.path.basename(data["image_url"])
        image_path = os.path.join('images', filename)
        download_image(data["image_url"],  image_path)

        small_image_url = response.css('img.gallery__photo-img::attr(src)').get()
        data["small_image_url"] = "https://vino.ua/" + small_image_url
        filename = os.path.basename(data["small_image_url"])
        image_path = os.path.join('images', filename)
        download_image(data["small_image_url"],  image_path)

        yield data


