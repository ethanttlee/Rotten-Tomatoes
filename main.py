from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd


def main():
    # session and url
    s = requests.session()
    url = "https://www.rottentomatoes.com/top/bestofrt/?year="

    # years
    movies_dict = {}
    years = []
    for year in range(2000, 2021):
        years.append(str(year))
        curr_url = url + str(year)
        result = s.get(curr_url)
        soup = BeautifulSoup(result.text, 'html.parser')
        movies = soup.findAll("a", {"class": "unstyled articleLink"})
        movies_dict[year] = []
        for movie in movies:
            link = movie.get('href')
            if "/m/" in link:
                movies_dict[year].append("rottentomatoes.com" + link)

    with open('movies.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['Year', 'Movie Link'])
        writer.writeheader()
        for key in movies_dict.keys():
            writer.writerow({'Year': key, 'Movie Link': movies_dict[key]})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
