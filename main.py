from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
from script import replacement, replacement_json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

def get_data(urls_file, server_timeout):
    options = webdriver.FirefoxOptions()
    options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    options.headless = True
    with open(urls_file, "r", encoding="utf-8") as f:
        urls_list = [url.strip() for url in f.readlines()]
    for url in urls_list:
        try:

            driver = webdriver.Firefox(
                executable_path="C:Users\kosty\PycharmProjects\similarweb\geckodriver",
                options=options
            )
            driver.get(url=url)

            time.sleep(server_timeout)

            with open("index.html", "w", encoding="UTF-8") as f:
                f.write(driver.page_source)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

        with open("index.html", "r", encoding="utf-8") as f:
            page = f.read()
            soup = BeautifulSoup(page, "lxml")
            # TODO: получаяем кол-во посещений
            if soup.find("div", class_="engagement-list") is not None:
                item_visit = soup.find("div", class_="engagement-list") \
                    .find("div", class_="engagement-list__item") \
                    .find("p", class_="engagement-list__item-value").getText()
            else:
                item_visit = ""
            # TODO: получаяем топ-3 страны

            item_countries = soup.find_all("div", class_="wa-geography__legend wa-geography__chart-legend")
            top_countries = []
            d = 0
            num = 3
            if len(item_countries) != 0:
                if len(item_countries[0].find_all("a", class_="wa-geography__country-name")) < 3:
                    num = len(item_countries[0].find_all("a", class_="wa-geography__country-name"))
                    while d < num:
                        item_coutry = item_countries[0].find_all("a", class_="wa-geography__country-name")[d].getText()
                        top_countries.append(item_coutry)
                        d += 1
                else:
                    while d < num:
                        item_coutry = item_countries[0].find_all("a", class_="wa-geography__country-name")[d].getText()
                        top_countries.append(item_coutry)
                        d += 1
            else:
                top_countries.append("none")

            # TODO: получаяем топ-10 сайтов
            item_sites = soup.find_all("div", class_="wa-competitors__list-item")
            top_sites = []
            k = 0
            num = 10
            if len(item_sites) != 0:
                if len(item_sites) < 10:
                    num = len(item_sites)
                    while k < num:
                        item_site = item_sites[k].find_all("span", class_="wa-competitors__list-item-title")[0].getText()
                        top_sites.append(item_site)
                        k += 1
                else:
                    while k < num:
                        item_site = item_sites[k].find_all("span", class_="wa-competitors__list-item-title")[0].getText()
                        top_sites.append(item_site)
                        k += 1
            else:
                top_sites.append("none")
            all_item = {}
            all_item[url] = []
            all_item[url].append({
                "total visits": item_visit,
                "top coutries": top_countries,
                "top siets": top_sites
            })

            with open("cache", "a") as json_file:
                json.dump(all_item, json_file)



def main():
    with open("cache", "w") as f:
        pass
    get_data(urls_file="urls.txt", server_timeout=9)

    # TODO:запись файла в текстовом формате, построчно

    replacement(file_write="data", file_read="cache")

    # TODO:запись файла в json формате

    # replacement_json(file_write="data", file_read="cache")


if __name__ == "__main__":
    while True:
        main()
        #TODO:можете поставить период в секундах

        #time.sleep(0)
