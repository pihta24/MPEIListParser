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


class MAIParser(BaseParser):
    base_url = "https://public.mai.ru/priem/rating/data/{}_1_l1_p1_f1{}.html"
    prefix_url = "https://priem.mai.ru/rating/"
    name = "МАИ"
    update_type = "parallel"

    def __init__(self):
        super().__init__()

    async def __get_prefix(self, session):
        async with session.get(self.prefix_url) as resp:
            html = await resp.text()
            bs = BeautifulSoup(html, "html.parser")
            select = bs.find("select", {"id": "place"})
            option = select.find_all("option")[1]
            return option["value"].split("_")[0]

    async def init(self):
        async with aiohttp.ClientSession() as session:
            prefix = await self.__get_prefix(session)
            async with session.get(self.base_url.format(prefix, "")) as resp:
                html = await resp.text()
                bs = BeautifulSoup(html, "html.parser")
                for i in bs.find_all("option")[1:]:
                    self._specs[i["value"].split("_")[-1]] = {"name": i.text,
                                                              "places": 0,
                                                              "places_target": 0,
                                                              "places_spec": 0,
                                                              "places_sep": 0,
                                                              "count": 0,
                                                              "count_target": 0,
                                                              "count_spec": 0,
                                                              "count_sep": 0,
                                                              "bvi": 0}

    async def _parse_list(self, num: str):
        async with aiohttp.ClientSession() as session:
            prefix = await self.__get_prefix(session)
            async with session.get(self.base_url.format(prefix, f"_{num}")) as resp:
                html = await resp.text()
                bs = BeautifulSoup(html, "html.parser")
                while True:
                    try:
                        p = bs.find_all("p")[1]
                    except IndexError:
                        prefix = await self.__get_prefix(session)
                        async with session.get(self.base_url.format(prefix, f"_{num}")) as new_resp:
                            html = await new_resp.text()
                            bs = BeautifulSoup(html, "html.parser")
                    else:
                        break
                for i in p.text.lower().replace("\t", "").replace("\n\n", "\n").split("\n"):
                    if "количество мест" in i:
                        self._specs[num]["places"] = int(i.split(":")[1].strip())
                    elif "из них по особой квоте" in i:
                        self._specs[num]["places_spec"] = int(i.split(":")[1].strip())
                    elif "из них по отдельной квоте" in i:
                        self._specs[num]["places_sep"] = int(i.split(":")[1].strip())
                    elif "из них по целевой квоте" in i:
                        self._specs[num]["places_target"] = int(i.split(":")[1].strip())
                for table in bs.find_all("table"):
                    table_header = table.find_previous("h4", {"class": "mt-5 mb-3"}).text
                    parsed_table = [[col.text if row.attrs.get("class", "") != "agree"
                                     else col.find("span", {"class": "notagree"})
                                     for col in row.find_all("td")] for row in table.find_all("tr")]
                    filtered = list(filter(lambda x: len(x) > 1, parsed_table))
                    if "Лица, поступающие без вступительных экзаменов" in table_header:
                        self._specs[num]["bvi"] = len(filtered)
                        for row in filtered:
                            app_id = row[1].replace("-", "").replace(" ", "").strip()
                            if app_id not in self._bvi:
                                self._bvi.append(app_id)
                    elif "Лица, поступающие по особой квоте" in table_header:
                        self._specs[num]["count_spec"] = len(filtered)
                    elif "Лица, поступающие в рамках отдельной квоты приема" in table_header:
                        self._specs[num]["count_sep"] = len(filtered)
                    elif "Лица, поступающие в рамках квоты приема на целевое обучение" in table_header:
                        self._specs[num]["count_target"] = len(filtered)
                    elif "Лица, поступающие по общему конкурсу" in table_header:
                        self._specs[num]["count"] = len(filtered)
                        for row in filtered:
                            app_id = row[1].replace("-", "").replace(" ", "").strip()
                            priority = int(row[8])
                            n = int(row[0])
                            if app_id in self._bvi:
                                continue
                            score = int(row[2])
                            if app_id not in self._applicants.keys():
                                self._applicants[app_id] = {}
                            self._applicants[app_id][priority] = [num, score, n]
                            self._concurs_lists[num].append(app_id)
                self._specs[num]["count"] += self._specs[num]["count_spec"] + self._specs[num]["count_sep"] + self._specs[num]["count_target"]


