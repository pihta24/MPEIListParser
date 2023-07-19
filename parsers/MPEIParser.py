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
from enum import Enum

import aiohttp
from bs4 import BeautifulSoup

from parsers.BaseParser import BaseParser


class Types(Enum):
    bvi = "we"
    base = "c"
    spec = "q"
    sep = "qs"
    target = "t"


class MPEIParser(BaseParser):
    base_url = "https://pk-mpei.ru/inform/list{}bac{}.html"
    name = "НИУ МЭИ"

    def __init__(self):
        super().__init__()
        self._specs = {
            581: {
                "name": "Прикладная математика и информатика МПОВМКС",
                "places": 60,
                "places_target": 6,
                "places_spec": 6,
                "places_sep": 6,
                "bvi": 0
            },
            16: {
                "name": "Прикладная математика и информатика ММ",
                "places": 40,
                "places_target": 4,
                "places_spec": 4,
                "places_sep": 4,
                "bvi": 0
            },
            533: {
                "name": "Строительство",
                "places": 25,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 3,
                "bvi": 0
            },
            14: {
                "name": "Информатика и вычислительная техника",
                "places": 190,
                "places_target": 29,
                "places_spec": 19,
                "places_sep": 19,
                "bvi": 0
            },
            35: {
                "name": "Прикладная информатика",
                "places": 30,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 3,
                "bvi": 0
            },
            22: {
                "name": "Информационная безопасность",
                "places": 50,
                "places_target": 15,
                "places_spec": 5,
                "places_sep": 5,
                "bvi": 0
            },
            19: {
                "name": "Беспроводные технологии",
                "places": 100,
                "places_target": 30,
                "places_spec": 10,
                "places_sep": 10,
                "bvi": 0
            },
            10: {
                "name": "Электроника и наноэлектроника",
                "places": 200,
                "places_target": 20,
                "places_spec": 21,
                "places_sep": 21,
                "bvi": 0
            },
            20: {
                "name": "Интеллектуальные системы",
                "places": 85,
                "places_target": 51,
                "places_spec": 9,
                "places_sep": 9,
                "bvi": 0
            },
            15: {
                "name": "Биотехнические системы и технологии, приборостроение",
                "places": 105,
                "places_target": 9,
                "places_spec": 11,
                "places_sep": 11,
                "bvi": 0
            },
            5: {
                "name": "Теплоэнергетика, теплотехника, автоматизация",
                "places": 190,
                "places_target": 28,
                "places_spec": 19,
                "places_sep": 19,
                "bvi": 0
            },
            963: {
                "name": "Экономика и управление на предприятии теплоэнергетики",
                "places": 20,
                "places_target": 4,
                "places_spec": 2,
                "places_sep": 2,
                "bvi": 0
            },
            971: {
                "name": "Промышленная и коммунальная теплоэнергетика",
                "places": 140,
                "places_target": 38,
                "places_spec": 14,
                "places_sep": 14,
                "bvi": 0
            },
            518: {
                "name": "Возобновляемая энергетика",
                "places": 55,
                "places_target": 11,
                "places_spec": 6,
                "places_sep": 6,
                "bvi": 0
            },
            975: {
                "name": "Цифровая электротехника и электроника",
                "places": 225,
                "places_target": 29,
                "places_spec": 23,
                "places_sep": 23,
                "bvi": 0
            },
            13: {
                "name": "Электроэнергетика",
                "places": 320,
                "places_target": 80,
                "places_spec": 32,
                "places_sep": 32,
                "bvi": 0
            },
            4: {
                "name": "Энергетическое машиностроение",
                "places": 96,
                "places_target": 14,
                "places_spec": 11,
                "places_sep": 11,
                "bvi": 0
            },
            7: {
                "name": "Ядерная энергетика и теплофизика",
                "places": 190,
                "places_target": 38,
                "places_spec": 19,
                "places_sep": 19,
                "bvi": 0
            },
            1: {
                "name": "Мехатроника, робототехника и машиностроение",
                "places": 85,
                "places_target": 11,
                "places_spec": 9,
                "places_sep": 9,
                "bvi": 0
            },
            544: {
                "name": "Управление качеством в производственно-технологических системах",
                "places": 25,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 3,
                "bvi": 0
            },
            17: {
                "name": "Управление в технических системах",
                "places": 75,
                "places_target": 8,
                "places_spec": 8,
                "places_sep": 8,
                "bvi": 0
            },
            540: {
                "name": "Экономика",
                "places": 50,
                "places_target": 8,
                "places_spec": 5,
                "places_sep": 5,
                "bvi": 0
            },
            542: {
                "name": "Менеджмент",
                "places": 30,
                "places_target": 2,
                "places_spec": 3,
                "places_sep": 3,
                "bvi": 0
            },
            588: {
                "name": "Бизнес-информатика",
                "places": 10,
                "places_target": 1,
                "places_spec": 1,
                "places_sep": 1,
                "bvi": 0
            }
        }

    async def update_lists(self):
        self._updating_lists = True
        self._processing_lists = True
        self._applicants.clear()
        self._concurs_lists = {i: [] for i in self._specs.keys()}
        self._bvi.clear()
        for i in self._specs.keys():
            self._specs[i]["bvi"] = 0
        coro = []
        for i in self._specs.keys():
            coro.append(self._parse_list(i, Types.base))
            coro.append(self._parse_list(i, Types.bvi))
        await asyncio.gather(*coro)

        self._last_update = datetime.now()

        for i in self._applicants.keys():
            self._applicants[i] = dict(sorted(self._applicants[i].items(), key=lambda x: x[0]))
        self._updating_lists = False

    async def _parse_list(self, num: int, list_type: Types):
        async with aiohttp.ClientSession() as session:
            match list_type:
                case Types.bvi | Types.base:
                    url = self.base_url.format(num, list_type.value)
            async with session.get(url) as resp:
                html = await resp.text()
                bs = BeautifulSoup(html, "html.parser")
                for table in bs.find_all("table"):
                    for n, row in enumerate(table.find_all("tr", {"class": "accepted"}), start=1):
                        cols = row.find_all("td")
                        if len(cols) not in [14, 15]:
                            break
                        app_id = cols[0].text.split(":")[1].strip()
                        priority = int(cols[10].text if list_type == Types.spec else cols[11].text)
                        if list_type == Types.bvi:
                            if priority == 1:
                                self._specs[num]["bvi"] += 1
                                self._bvi.append(app_id)
                                if app_id in self._applicants.keys():
                                    del self._applicants[app_id]
                        else:
                            if app_id in self._bvi:
                                continue
                            score = int(cols[1].text) if list_type != Types.target else int(cols[2])
                            if app_id not in self._applicants.keys():
                                self._applicants[app_id] = {}
                            self._applicants[app_id][priority] = [num, score, n]
                            self._concurs_lists[num].append(app_id)
                    else:
                        break
