#  Copyright (c) 2023 pihta24 <admin@pihta24.ru>
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import aiohttp
from bs4 import BeautifulSoup

from parsers.BaseParser import BaseParser


class MTUCIParser(BaseParser):
    specs_url = "https://lk.abitur.mtuci.ru/mtuci-lists/view/"
    name = "МТУСИ"
    update_type = "parallel"

    def __init__(self):
        super().__init__()

    async def init(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.specs_url) as resp:
                html = await resp.text()
                bs = BeautifulSoup(html, "html.parser")
                for i, j in enumerate(bs.find("div", {"class": "body-content"}).find_all("a")):
                    self._specs[i] = {"name": j.text,
                                      "url": f'https://lk.abitur.mtuci.ru{j["href"]}',
                                      "places": 0,
                                      "places_target": 0,
                                      "places_spec": 0,
                                      "places_sep": 0,
                                      "bvi": 0}

    async def _parse_list(self, num: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._specs[num]["url"]) as resp:
                html = await resp.text()
                bs = BeautifulSoup(html, "html.parser")

                span = bs.find("span", {"title": "Бюджетное финансирование"})
                self._specs[num]["places"] = int(span.text.strip())
                span = bs.find("span", {"title": "Целевое обучение"})
                self._specs[num]["places_target"] = int(span.text.strip())
                span = bs.find("span", {"title": "Особая квота"})
                self._specs[num]["places_spec"] = int(span.text.strip())
                span = bs.find("span", {"title": "Отдельная квота"})
                self._specs[num]["places_sep"] = int(span.text.strip())
                self._specs[num]["count_bvi"] = 0

                table = bs.find("table")
                parsed_table = [[col.text for col in row.find_all("td")] for row in table.find_all("tr")]
                filtered = list(filter(lambda x: len(x) > 1, parsed_table))
                for row in filtered:
                    app_id = row[1].replace("-", "").replace(" ", "").strip()
                    n = int(row[0])
                    if len(row) != 6:
                        a = len(row) - 11
                        priority = int(row[9 + a].split("/")[0].strip())
                        score = int(row[7 + a].replace("!", "").strip())
                    else:
                        priority = int(row[4].split("/")[0].strip())
                        score = "БВИ"
                        self._specs[num]["count_bvi"] += 1
                    if app_id not in self._applicants.keys():
                        self._applicants[app_id] = {}
                    self._applicants[app_id][priority] = [num, score, n]
                    self._concurs_lists[num].append(app_id)
