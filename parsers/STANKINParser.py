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
import asyncio
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

from parsers.BaseParser import BaseParser


class STANKINParser(BaseParser):
    base_url = "https://priem.stankin.ru/pub/site/19/gridspisokpostupayushchikh/?" \
               "PROPERTY_388=Бюджетная+основа&PROPERTY_389=Очная&" \
               "PROPERTY_394={}&" \
               "PROPERTY_402=-&apply_filter=Y&PROPERTY_419=Подано&" \
               "PROPERTY_584=ready&LIST_TYPE=ranked&EDU_LEVEL=bs&PAGEN_1={}"
    stats_url = "https://priem.stankin.ru/bakalavriatispetsialitet/statistika/"
    name = "МГТУ \"СТАНКИН\""

    def __init__(self):
        super().__init__()
        self._specs = {
            "09.03.01": {
                "name": "Информатика и вычислительная техника",
                "places": 115,
                "places_target": 17,
                "places_spec": 12,
                "places_sep": 12,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "09.03.02": {
                "name": "Информационные системы и технологии",
                "places": 115,
                "places_target": 17,
                "places_spec": 12,
                "places_sep": 12,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "09.03.03": {
                "name": "Прикладная информатика",
                "places": 96,
                "places_target": 10,
                "places_spec": 10,
                "places_sep": 10,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "09.03.04": {
                "name": "Программная инженерия",
                "places": 64,
                "places_target": 6,
                "places_spec": 7,
                "places_sep": 7,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "12.03.01": {
                "name": "Приборостроение",
                "places": 69,
                "places_target": 14,
                "places_spec": 7,
                "places_sep": 7,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "15.03.01": {
                "name": "Машиностроение",
                "places": 60,
                "places_target": 12,
                "places_spec": 6,
                "places_sep": 6,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "15.03.02": {
                "name": "Технологические машины и оборудование",
                "places": 25,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 3,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "15.03.04": {
                "name": "Автоматизация технологических процессов и производств",
                "places": 85,
                "places_target": 13,
                "places_spec": 9,
                "places_sep": 9,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "15.03.05": {
                "name": "Конструкторско-технологическое обеспечение машиностроительных производств",
                "places": 85,
                "places_target": 26,
                "places_spec": 9,
                "places_sep": 9,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "15.03.06": {
                "name": "Мехатроника и робототехника",
                "places": 75,
                "places_target": 8,
                "places_spec": 8,
                "places_sep": 8,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "15.05.01": {
                "name": "Проектирование технологических машин и комплексов",
                "places": 75,
                "places_target": 23,
                "places_spec": 8,
                "places_sep": 8,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "20.03.01": {
                "name": "Техносферная безопасность",
                "places": 50,
                "places_target": 5,
                "places_spec": 5,
                "places_sep": 5,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "27.03.01": {
                "name": "Стандартизация и метрология",
                "places": 30,
                "places_target": 9,
                "places_spec": 3,
                "places_sep": 3,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "27.03.02": {
                "name": "Управление качеством",
                "places": 25,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 3,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "27.03.04": {
                "name": "Управление в технических системах",
                "places": 50,
                "places_target": 5,
                "places_spec": 5,
                "places_sep": 5,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "38.03.01": {
                "name": "Экономика",
                "places": 20,
                "places_target": 3,
                "places_spec": 2,
                "places_sep": 2,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "38.03.02": {
                "name": "Менеджмент",
                "places": 20,
                "places_target": 1,
                "places_spec": 2,
                "places_sep": 2,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            },
            "38.03.03": {
                "name": "Управление персоналом	",
                "places": 20,
                "places_target": 3,
                "places_spec": 2,
                "places_sep": 2,
                "count": 0,
                "count_target": 0,
                "count_spec": 0,
                "count_sep": 0,
                "bvi": 0
            }
        }

    async def update_lists(self):
        self._updating_lists = True
        self._processing_lists = True
        self._applicants.clear()
        self._concurs_lists = {i: [] for i in self._specs.keys()}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.stats_url) as resp:
                html = await resp.text()
                bs = BeautifulSoup(html, "html.parser")
                table = bs.find("table")
                for row in table.find_all("tr")[3:]:
                    cols = row.find_all("td")
                    if cols[0].text.strip() in self._specs.keys():
                        self._specs[cols[0].text.strip()]["count"] = int(cols[3].text.strip())
                        self._specs[cols[0].text.strip()]["count_target"] = int(cols[4].text.strip())
                        self._specs[cols[0].text.strip()]["count_spec"] = int(cols[5].text.strip())
                        self._specs[cols[0].text.strip()]["count_sep"] = int(cols[6].text.strip())
                        self._specs[cols[0].text.strip()]["bvi"] = int(cols[7].text.strip())

        coro = []
        for i in self._specs.keys():
            coro.append(self._parse_list(i))
        await asyncio.gather(*coro)

        self._last_update = datetime.now()

        for i in self._applicants.keys():
            self._applicants[i] = dict(sorted(self._applicants[i].items(), key=lambda x: x[0]))
        self._updating_lists = False

    async def _parse_list(self, num: str):
        async with aiohttp.ClientSession() as session:
            for i in range(1, (self._specs[num]["count"] // 50 + 1) if self._specs[num]["count"] % 50 == 0
                           else (self._specs[num]["count"] // 50 + 2)):
                async with session.get(self.base_url.format(f"{num} {self._specs[num]['name']}", i)) as resp:
                    html = await resp.text()
                    bs = BeautifulSoup(html, "html.parser")
                    table = bs.find("table")
                    tbody = table.find("tbody")
                    for row in tbody.find_all("tr", recursive=False)[1:]:
                        cols = row.find_all("td")
                        n = int(cols[0].text.strip())
                        if n == 1 and i != 1:
                            break
                        app_id = cols[1].text.replace("-", "").replace(" ", "").strip()
                        priority = int(cols[3].text.strip())
                        score = int(cols[6].text.strip())

                        if app_id not in self._applicants.keys():
                            self._applicants[app_id] = {}
                        self._applicants[app_id][priority] = [num, score, n]
                        if app_id not in self._concurs_lists[num]:
                            self._concurs_lists[num].append(app_id)
