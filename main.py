import datetime
import pandas
import collections
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def year(how_long):
    return {
        how_long % 10 == 0: 'лет',
        how_long % 10 == 1: 'год',
        1 < how_long % 10 < 5: 'года',
        how_long % 10 > 4: 'лет',
        10 < how_long % 100 < 20: 'лет',
        how_long < 0: 'ошибка'
    }[True]


def main():
    today = datetime.date.today()
    past_year = datetime.datetime(year=1920, month=10, day=10)
    how_long = today.year - past_year.year

    excel_data_wine = pandas.read_excel("wine.xlsx", na_values=['N/A', 'NA'], keep_default_na=False)
    wines = excel_data_wine.to_dict(orient="records")

    wine_dict = collections.defaultdict(list)
    for wine in wines:
        if wine.get("Категория") == "Белые вина":
            wine_dict["Белые вина"].append(wine)
        if wine.get("Категория") == "Красные вина":
            wine_dict["Красные вина"].append(wine)
        if wine.get("Категория") == "Напитки":
            wine_dict["Напитки"].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template("template.html")
    rendered_page = template.render(
        how_longer=f"Уже {how_long} {year(how_long)} с нами",
        white_wine=wine_dict["Белые вина"],
        red_wine=wine_dict["Красные вина"],
        drinks=wine_dict["Напитки"]
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()