#
# Gets web data based on requests
#

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import jsonify


class InvalidYearError(Exception):
    pass


main_url = 'https://www.formula1.com'


def get_web_data(url: str) -> BeautifulSoup:
    page = urlopen(url)
    return BeautifulSoup(page, 'html.parser')


def create_race_df(url: str):

    # Get html data from page and Convert into soup
    soup = get_web_data(url)
    rows = soup.find_all('tr')

    # Get content from table cells
    list_rows = []
    for row in rows:
        row_td = row.find_all('td')
        # print(row_td)
        str_cells = str(row_td)
        clean_text = BeautifulSoup(str_cells, 'html.parser').get_text()
        list_rows.append(clean_text)

    # Create dataframe
    df = pd.DataFrame(list_rows)
    df1 = df[0].str.split(',', expand=True)
    df1[3] = df1[3].str.split('\n').str.slice(1, 3).str.join(' ')
    df1 = df1.drop(df1.index[0])

    # Get headers
    col_labels = soup.find_all('th')
    col_str = str(col_labels)
    clean_text2 = BeautifulSoup(col_str, 'html.parser').get_text()
    headers = [clean_text2]
    df2 = pd.DataFrame(headers)
    df3 = df2[0].str.strip('[').str.strip(']').str.split(',', expand=True)

    # Concat dataframes
    frames = [df3, df1]
    df4 = pd.concat(frames)
    df4[1] = df4[1].str.strip()
    df5 = df4.rename(columns=df4.iloc[0])
    df6 = df5.drop(df5.index[0])
    df6 = df6.drop(axis=1, labels='')
    df6 = df6.drop(axis=1, labels=' ')
    # df6.reset_index(drop=True, inplace=True)

    # Write to csv
    # df6.to_csv('f1_results.csv', index=False)          # CHANGE IF WRITING TO CSV
    # return df6.to_string(index=False)
    return df6


def race_by_year(year: str) -> dict:
    """Gives a link to each race for locations in that year"""

    years_dict = dict()

    # Get all the races in that year
    year_url = f'{main_url}/en/results.html/{year}/races.html'
    soup = get_web_data(year_url)
    all_links = soup.find_all('a', class_='dark bold ArchiveLink')

    # Find all links for races in that year and location
    for link in all_links:
        link_href = link.get('href')
        if link_href and 'races' in link_href:                              # Search Year
            years_dict[link.get_text().strip().lower()] = f'{main_url}{link_href}'  # Add location and link to dict

    # Invalid year if nothing in dict
    if len(years_dict) == 0:
        raise InvalidYearError

    return years_dict


if __name__ == '__main__':
    url = 'https://www.formula1.com/en/results.html/2019/races.html'
    location_link = race_by_year('2020')
    # print(location_link['Abu Dhabi'])
    all_loc = create_race_df(url)
    print(location_link)
    # print(a)
    # print(a.split('\n'))

    '''
    pages_list = []
    loc_str = all_loc.split('\n')
    header = loc_str[0]
    body = loc_str[1:]

    for i in range(3):
        pages_list.append('\n'.join([header] + body[7*i: 7*(i+1)]))

    print(len(pages_list))
    for i in pages_list:
        print(i, '\n\n')
    # print('\n'.join([f'{key}\t{value}' for key, value in location_link.items()]))
    '''

    '''
    1) Take length of first line
    2) Subtract length of title from first line
    3) Take that length // 2
    4) ' ' * (length // 2) + title
    '''
