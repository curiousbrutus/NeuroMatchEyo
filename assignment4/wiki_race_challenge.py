"""
Bonus task
"""
from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from typing import List


def find_path(start: str, finish: str) -> List[str]:
  """Find the shortest path from `start` to `finish`

  Arguments:
    start (str): wikipedia article URL to start from
    finish (str): wikipedia article URL to stop at

  Returns:
    urls (list[str]):
    List of URLs representing the path from `start` to `finish`.
    The first item should be `start`.
    The last item should be `finish`.
    All items of the list should be URLs for wikipedia articles.
    Each article should have a direct link to the next article in the list.
  """
  path = [start]
  visited = set([start])
  graph = {start: []}
  queue = [start]

  while queue:
    node = queue.pop(0)
    if node == finish:
      break
    try:
      response = requests.get(node)
    except:
      continue
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a"):
      href = link.get("href")
      if href.startswith("/wiki/") and ":" not in href:
        url = "https://en.wikipedia.org" + href
        if url not in visited:
          visited.add(url)
          path.append(url)
          queue.append(url)
          graph[node].append(url)
          graph[url] = []

  if node != finish:
    return []

  shortest_path = [finish]
  while node != start:
    for predecessor in graph[node]:
      if predecessor in visited:
        shortest_path.append(predecessor)
        node = predecessor
        break

  shortest_path.reverse()
  return shortest_path


if __name__ == "__main__":
  start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
  finish = "https://en.wikipedia.org/wiki/Peace"
  path = find_path(start, finish)
  print(path)
