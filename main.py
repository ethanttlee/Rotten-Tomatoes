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
    for year in range(2000, 2021):
        curr_url = url + str(year)
        result = s.get(curr_url)
        soup = BeautifulSoup(result.text, 'html.parser')
        movies = soup.findAll("a", {"class": "unstyled articleLink"})
        movies_dict[year] = []
        for movie in movies:
            link = movie.get('href')
            if "/m/" in link:
                movies_dict[year].append(("rottentomatoes.com" + link,
                                         link[3:]))

    with open('movies.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['Movie', 'Movie Link',
                                                      'Year'])
        writer.writeheader()
        for key in movies_dict.keys():
            for movie in movies_dict[key]:
                writer.writerow({'Movie': movie[1], 'Movie Link': movie[0],
                                 'Year': key})


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
