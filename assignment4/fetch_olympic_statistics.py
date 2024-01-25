"""
Task 4

collecting olympic statistics from wikipedia
"""

from __future__ import annotations
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import pandas as pd
from requesting_urls import get_html


# Countries to submit statistics for
scandinavian_countries = ["Norway", "Sweden", "Denmark"]

# Summer sports to submit statistics for
summer_sports = ["Sailing", "Athletics", "Handball", "Football", "Cycling", "Archery"]


def report_scandi_stats(url: str, sports_list: list[str], work_dir: str | Path) -> None:
    """
    Given the url, extract and display following statistics for the Scandinavian countries:

      -  Total number of gold medals for for summer and winter Olympics
      -  Total number of gold, silver and bronze medals in the selected summer sports from sport_list
      -  The best country in number of gold medals in each of the selected summer sports from sport_list

    Display the first two as bar charts, and the last as an md. table and save in a separate directory.

    Parameters:
        url (str) : url to the 'All-time Olympic Games medal table' wiki page
        sports_list (list[str]) : list of summer Olympic games sports to display statistics for
        work_dir (str | Path) : (absolute) path to your current working directory

    Returns:
        None
    """

    # Make a call to get_scandi_stats
    # Plot the summer/winter gold medal stats
    # Iterate through each sport and make a call to get_sport_stats
    # Plot the sport specific stats
    # Make a call to find_best_country_in_sport for each sport
    # Create and save the md table of best in each sport stats

    work_dir = Path(work_dir)
    country_dict = get_scandi_stats(url)

    stats_dir = work_dir / "olympic_games_results"
    stats_dir.mkdir(exist_ok=True)

    best_in_sport = []
    # Valid values for medal ["Gold" | "Silver" |"Bronze"]

    for sport in sports_list:
        results: dict[str, dict[str, int]] = {}
        results["Norway"] = get_sport_stats(country_dict["Norway"]["url"], sport)
        results["Sweden"] = get_sport_stats(country_dict["Sweden"]["url"], sport)
        results["Denmark"] = get_sport_stats(country_dict["Denmark"]["url"], sport)
        plot_scandi_stats(results, sport, stats_dir)
        best_in_sport.append((sport, find_best_country_in_sport(results, "Gold")))

    headers = ["Sport", "Best Country"]
    df = pd.DataFrame(best_in_sport, columns=headers)
    df.to_markdown(stats_dir/"best_of_sport_by_Gold.md", index=False)


def get_scandi_stats(
    url: str,
) -> dict[str, dict[str, str | dict[str, int]]]:
    """Given the url, extract the urls for the Scandinavian countries,
       as well as number of gold medals acquired in summer and winter Olympic games
       from 'List of NOCs with medals' table.

    Parameters:
      url (str): url to the 'All-time Olympic Games medal table' wiki page

    Returns:
      country_dict: dictionary of the form:
        {
            "country": {
                "url": "https://...",
                "medals": {
                    "Summer": 0,
                    "Winter": 0,
                },
            },
        }

        with the tree keys "Norway", "Denmark", "Sweden".
    """

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    legend = re.compile(r"^ Special delegates", re. IGNORECASE)
    head = soup.find(class_="legend")
    table = head.find_next("table")
    base_url = "https://en.wikipedia.org"

    rows = table.find_all("tr")

    country_dict: dict[str, dict[str, str | dict[str, int]]] = {}

    for row in rows:
        cols = row.find_all("td")
        if cols and cols[0].a.get_text() in scandinavian_countries:
            country_dict[cols[0].a.get_text(strip=True)] = {"url": base_url + cols[0].a.get("href"), "medals":{"Summer":int(cols[2].get_text(strip=True)), "Winter":int(cols[7].get_text(strip=True))}}

    return country_dict




def get_sport_stats(country_url: str, sport: str) -> dict[str, int]:
    """Given the url to country specific performance page, get the number of gold, silver, and bronze medals
      the given country has acquired in the requested sport in summer Olympic games.

    Parameters:
        - country_url (str) : url to the country specific Olympic performance wiki page
        - sport (str) : name of the summer Olympic sport in interest. Should be used to filter rows in the table.

    Returns:
        - medals (dict[str, int]) : dictionary of number of medal acquired in the given sport by the country
                          Format:
                          {"Gold" : x, "Silver" : y, "Bronze" : z}
    """

    html = get_html(html)
    soup = BeautifulSoup(html, "html.parser")

    sport_pattern = re.compile(f"{sport}", re.IGNORECASE)
    table_pattern = re.compile(r"^Medals of the Summer Sports", re.IGNORECASE)

    head = soup.find(class_="mw-headline", string=table_pattern)
    table = head.find_next("table")

    medals = {
        "Gold": 0,
        "Silver": 0,
        "Bronze": 0,
    }

    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if row.a and sport_pattern.search(row.a.get_text()):
            medals["Gold"] = int(cols[0].get_text())
            medals["Silver"] = int(cols[1].get_text())
            medals["Bronze"] = int(cols[2].get_text())

    return medals



def find_best_country_in_sport(
    results: dict[str, dict[str, int]], medal: str = "Gold"
) -> str:
    """Given a dictionary with medal stats in a given sport for the Scandinavian countries, return the country
        that has received the most of the given `medal`.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - medal (str) : medal type to compare for. Valid parameters: ["Gold" | "Silver" |"Bronze"]. Should be used as a key
                          to the medal dictionary.
    Returns:
        - best (str) : name of the country(ies) leading in number of gold medals in the given sport
                       If one country leads only, return its name, like for instance 'Norway'
                       If two countries lead return their names separated with '/' like 'Norway/Sweden'
                       If all or none of the countries lead, return string 'None'
    """
    valid_medals = {"Gold", "Silver", "Bronze"}
    if medal not in valid_medals:
        raise ValueError(
            f"{medal} is invalid parameter for ranking, must be in {valid_medals}"
        )
    

    if results["Norway"][medal] == results["Sweden"][medal] == results["Denmark"][medal]:
        best = "None"
    elif results["Norway"][medal] > results["Sweden"][medal] and results["Norway"][medal] > results["Denmark"][medal]:
        best = "Norway"
    elif results["Sweden"][medal] > results["Norway"][medal] and results["Sweden"][medal] > results["Denmark"][medal]:
        best = "Sweden"
    elif results["Denmark"][medal] > results["Sweden"][medal] and results["Denmark"][medal] > results["Norway"][medal]:
        best = "Denmark"
    elif results["Norway"][medal] == results["Sweden"][medal]:
        best = "Norway/Sweden"
    elif results["Norway"][medal] == results["Denmark"][medal]:
        best = "Norway/Denmark"
    elif results["Denmark"][medal] == results["Sweden"][medal]:
        best = "Denmark/Sweden"
    return best



# Define your own plotting functions and optional helper functions


def plot_scandi_stats(
    country_dict: dict[str, dict[str, str | dict[str, int]]],
    output_parent: str | Path | None = None,
) -> None:
    """Plot the number of gold medals in summer and winter games for each of the scandi countries as bars.

    Parameters:
      results (dict[str, dict[str, int]]) : a nested dictionary of country names and the corresponding number of summer and winter
                            gold medals from 'List of NOCs with medals' table.
                            Format:
                            {"country_name": {"Summer" : x, "Winter" : y}}
      output_parent (str | Path) : parent file path to save the plot in
    Returns:
      None
    """

    all = []
    summer_medals = []
    winter_medals = []

    for country, stats in country_dict.items():
        summer_medals.append(stats["medals"]["Summer"])
        winter_medals.append(stats["medals"]["Winter"])

        all.append(country)


    x_summer = range(0, 12, 4)
    x_winter = range(1, 12, 4)

    bars = plt.bar(x_summer, summer_medals, label="Summer")
    plt.bar_label(bars)
    bars = plt.bar(x_winter, winter_medals, label="Winter")
    plt.bar_label(bars)

    plt.xticks(range(0, 12, 4), all, rotation = 12)
    plt.legend(loc=0)
    plt.grid(False)
    plt.title("Summary of the Gold Medals Received for the Summer/Winter Games for Scandinavian Countries")
    plt.ylabel("Number of Gold Medals")

    file_path = output_parent/"total_medal_ranking.png"
    plt.savefig(file_path)
    plt.clf()