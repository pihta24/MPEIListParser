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


class MIREAParser(BaseParser):
    name = "РТУ МИРЭА"
    update_type = "series"

    def __init__(self):
        super().__init__()
        self._specs = {
            1: {
                "name": "Прикладная математика и информатика (ИИИ)",
                "places": 96,
                "places_target": 8,
                "places_spec": 11,
                "places_sep": 11,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748193468849593654",
                "bvi_url": None,
                "bvi": 0
            },
            2: {
                "name": "Прикладная математика (ИИТ)",
                "places": 24,
                "places_target": 0,
                "places_spec": 3,
                "places_sep": 3,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205377727503670",
                "bvi_url": None,
                "bvi": 0
            },
            3: {
                "name": "Статистика (ИТУ)",
                "places": 30,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 3,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205371509447990",
                "bvi_url": None,
                "bvi": 0
            },
            4: {
                "name": "Фундаментальная информатика и информационные технологии (ИКБ)",
                "places": 40,
                "places_target": 4,
                "places_spec": 4,
                "places_sep": 4,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205364832116022",
                "bvi_url": None,
                "bvi": 0
            },
            5: {
                "name": "Химия (ИТХТ)",
                "places": 100,
                "places_target": 10,
                "places_spec": 10,
                "places_sep": 10,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205351209016630",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205351207968054",
                "bvi": 0
            },
            6: {
                "name": "Картография и геоинформатика (ИРИ)",
                "places": 25,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 3,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205344227597622",
                "bvi_url": None,
                "bvi": 0
            },
            7: {
                "name": "Информатика и вычислительная техника (ИИИ)",
                "places": 150,
                "places_target": 23,
                "places_spec": 15,
                "places_sep": 15,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205333570919734",
                "bvi_url": None,
                "bvi": 0
            },
            8: {
                "name": "Информатика и вычислительная техника (ИИТ)",
                "places": 85,
                "places_target": 17,
                "places_spec": 9,
                "places_sep": 9,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205461187861814",
                "bvi_url": None,
                "bvi": 0
            },
            9: {
                "name": "Информационные системы и технологии (ИКБ)",
                "places": 200,
                "places_target": 24,
                "places_spec": 22,
                "places_sep": 22,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205454286134582",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205454285086006",
                "bvi": 0
            },
            10: {
                "name": "Информационные системы и технологии (ИРИ)",
                "places": 50,
                "places_target": 7,
                "places_spec": 5,
                "places_sep": 5,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205448598658358",
                "bvi_url": None,
                "bvi": 0
            },
            11: {
                "name": "Информационные системы и технологии - Компьютерный дизайн (ИПТИП)",
                "places": 50,
                "places_target": 2,
                "places_spec": 5,
                "places_sep": 5,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205442851413302",
                "bvi_url": None,
                "bvi": 0
            },
            12: {
                "name": "Информационные системы и технологии - Фулстек разработка (ИПТИП)",
                "places": 90,
                "places_target": 9,
                "places_spec": 9,
                "places_sep": 9,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205436693126454",
                "bvi_url": None,
                "bvi": 0
            },
            13: {
                "name": "Прикладная информатика (ИИТ)",
                "places": 183,
                "places_target": 16,
                "places_spec": 19,
                "places_sep": 19,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205428624334134",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205428623285558",
                "bvi": 0
            },
            14: {
                "name": "Программная инженерия (ИИТ)",
                "places": 246,
                "places_target": 40,
                "places_spec": 25,
                "places_sep": 25,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205422769085750",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205422768037174",
                "bvi": 0
            },
            15: {
                "name": "Информационная безопасность (ИКБ)",
                "places": 52,
                "places_target": 22,
                "places_spec": 6,
                "places_sep": 6,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205535757344054",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205535756295478",
                "bvi": 0
            },
            16: {
                "name": "Компьютерная безопасность (ИИИ)",
                "places": 61,
                "places_target": 12,
                "places_spec": 9,
                "places_sep": 9,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205531612323126",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205531611274550",
                "bvi": 0
            },
            17: {
                "name": "Информационная безопасность телекоммуникационных систем (ИИИ)",
                "places": 32,
                "places_target": 20,
                "places_spec": 5,
                "places_sep": 5,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205527259684150",
                "bvi_url": None,
                "bvi": 0
            },
            18: {
                "name": "Информационная безопасность автоматизированных систем (ИКБ)",
                "places": 52,
                "places_target": 17,
                "places_spec": 7,
                "places_sep": 7,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205522704670006",
                "bvi_url": None,
                "bvi": 0
            },
            19: {
                "name": "Информационно-аналитические системы безопасности (ИКБ)",
                "places": 39,
                "places_target": 9,
                "places_spec": 5,
                "places_sep": 5,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205519868271926",
                "bvi_url": None,
                "bvi": 0
            },
            20: {
                "name": "Безопасность информационных технологий в правоохранительной сфере (ИКБ)",
                "places": 45,
                "places_target": 5,
                "places_spec": 5,
                "places_sep": 5,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205515758902582",
                "bvi_url": None,
                "bvi": 0
            },
            21: {
                "name": "Радиотехника (ИРИ)",
                "places": 58,
                "places_target": 20,
                "places_spec": 6,
                "places_sep": 6,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205512494685494",
                "bvi_url": None,
                "bvi": 0
            },
            22: {
                "name": "Инфокоммуникационные технологии и системы связи (ИРИ)",
                "places": 88,
                "places_target": 8,
                "places_spec": 9,
                "places_sep": 9,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205505111661878",
                "bvi_url": None,
                "bvi": 0
            },
            23: {
                "name": "Конструирование и технология электронных средств (ИРИ)",
                "places": 63,
                "places_target": 18,
                "places_spec": 7,
                "places_sep": 7,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205498687036726",
                "bvi_url": None,
                "bvi": 0
            },
            24: {
                "name": "Электроника и наноэлектроника (ИПТИП)",
                "places": 25,
                "places_target": 6,
                "places_spec": 3,
                "places_sep": 3,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205492169088310",
                "bvi_url": None,
                "bvi": 0
            },
            25: {
                "name": "Радиоэлектронные системы и комплексы (ИРИ)",
                "places": 40,
                "places_target": 26,
                "places_spec": 6,
                "places_sep": 6,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205486659870006",
                "bvi_url": None,
                "bvi": 0
            },
            26: {
                "name": "Приборостроение (ИКБ)",
                "places": 43,
                "places_target": 14,
                "places_spec": 5,
                "places_sep": 5,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205604742110518",
                "bvi_url": None,
                "bvi": 0
            },
            27: {
                "name": "Биотехнические системы и технологии (ИИИ)",
                "places": 60,
                "places_target": 3,
                "places_spec": 6,
                "places_sep": 6,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205598518811958",
                "bvi_url": None,
                "bvi": 0
            },
            28: {
                "name": "Лазерная техника и лазерные технологии (ИПТИП)",
                "places": 38,
                "places_target": 4,
                "places_spec": 4,
                "places_sep": 4,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205591555218742",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205591554170166",
                "bvi": 0
            },
            29: {
                "name": "Электронные и оптико-электронные приборы и системы специального назначения (ИПТИП)",
                "places": 30,
                "places_target": 16,
                "places_spec": 3,
                "places_sep": 3,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205585424194870",
                "bvi_url": None,
                "bvi": 0
            },
            30: {
                "name": "Машиностроение (ИПТИП)",
                "places": 40,
                "places_target": 8,
                "places_spec": 4,
                "places_sep": 4,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205581416537398",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205581415488822",
                "bvi": 0
            },
            31: {
                "name": "Автоматизация технологических процессов и производств (ИИИ)",
                "places": 40,
                "places_target": 6,
                "places_spec": 4,
                "places_sep": 4,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205574846160182",
                "bvi_url": None,
                "bvi": 0
            },
            32: {
                "name": "Мехатроника и робототехника (ИИИ)",
                "places": 48,
                "places_target": 3,
                "places_spec": 5,
                "places_sep": 5,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205567742057782",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205567741009206",
                "bvi": 0
            },
            33: {
                "name": "Химическая технология (ИТХТ)",
                "places": 331,
                "places_target": 30,
                "places_spec": 34,
                "places_sep": 34,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205560341208374",
                "bvi_url": None,
                "bvi": 0
            },
            34: {
                "name": "Биотехнология (ИТХТ)",
                "places": 128,
                "places_target": 13,
                "places_spec": 13,
                "places_sep": 13,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205685050449206",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205685049400630",
                "bvi": 0
            },
            35: {
                "name": "Техносферная безопасность (ИТХТ)",
                "places": 30,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 3,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205677892869430",
                "bvi_url": None,
                "bvi": 0
            },
            36: {
                "name": "Материаловедение и технологии материалов (ИПТИП)",
                "places": 60,
                "places_target": 6,
                "places_spec": 6,
                "places_sep": 6,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205671651745078",
                "bvi_url": None,
                "bvi": 0
            },
            37: {
                "name": "Стандартизация и метрология (ИПТИП)",
                "places": 30,
                "places_target": 5,
                "places_spec": 3,
                "places_sep": 3,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205665905548598",
                "bvi_url": None,
                "bvi": 0
            },
            38: {
                "name": "Системный анализ и управление (ИИИ)",
                "places": 75,
                "places_target": 8,
                "places_spec": 8,
                "places_sep": 8,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205659639258422",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205659638209846",
                "bvi": 0
            },
            39: {
                "name": "Инноватика (ИТУ)",
                "places": 75,
                "places_target": 5,
                "places_spec": 8,
                "places_sep": 8,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205653593169206",
                "bvi_url": None,
                "bvi": 0
            },
            40: {
                "name": "Нанотехнологии и микросистемная техника (ИПТИП)",
                "places": 20,
                "places_target": 1,
                "places_spec": 2,
                "places_sep": 2,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205647265013046",
                "bvi_url": None,
                "bvi": 0
            },
            41: {
                "name": "Технология художественной обработки материалов (ИПТИП)",
                "places": 30,
                "places_target": 3,
                "places_spec": 3,
                "places_sep": 2,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205626934172982",
                "bvi_url": None,
                "bvi": 0
            },
            42: {
                "name": "Управление персоналом (ИТУ)",
                "places": 1,
                "places_target": 0,
                "places_spec": 1,
                "places_sep": 0,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205737335594294",
                "bvi_url": None,
                "bvi": 0
            },
            43: {
                "name": "Бизнес-информатика (ИТУ)",
                "places": 4,
                "places_target": 1,
                "places_spec": 1,
                "places_sep": 1,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205728456252726",
                "bvi_url": None,
                "bvi": 0
            },
            44: {
                "name": "Экономическая безопасность (ИКБ)",
                "places": 1,
                "places_target": 0,
                "places_spec": 0,
                "places_sep": 0,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205722184719670",
                "bvi_url": None,
                "bvi": 0
            },
            45: {
                "name": "Юриспруденция (ИТУ)",
                "places": 6,
                "places_target": 1,
                "places_spec": 1,
                "places_sep": 1,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205718460177718",
                "bvi_url": None,
                "bvi": 0
            },
            46: {
                "name": "Правовое обеспечение национальной безопасности (ИКБ)",
                "places": 2,
                "places_target": 0,
                "places_spec": 1,
                "places_sep": 1,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205711439961398",
                "bvi_url": None,
                "bvi": 0
            },
            47: {
                "name": "Документоведение и архивоведение (ИТУ)",
                "places": 24,
                "places_target": 0,
                "places_spec": 3,
                "places_sep": 3,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205707438595382",
                "bvi_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205707437546806",
                "bvi": 0
            },
            48: {
                "name": "Дизайн (ИПТИП)",
                "places": 15,
                "places_target": 2,
                "places_spec": 2,
                "places_sep": 2,
                "base_url": "https://priem.mirea.ru/accepted-entrants-list/personal_code_rating.php?competition=1748205764814576950",
                "bvi_url": None,
                "bvi": 0
            }
        }

    async def _parse_list(self, num: int):
        async with aiohttp.ClientSession() as session:
            if self._specs[num]["bvi_url"]:
                async with session.get(self._specs[num]["bvi_url"]) as resp:
                    html = await resp.text()
                    bs = BeautifulSoup(html, "html.parser")
                    table = bs.find("table")
                    for n, row in enumerate(table.find_all("tr", recursive=False), start=1):
                        cols = row.find_all("td")
                        app_id = cols[1].text.replace("-", "").replace(" ", "").strip()
                        priority = int(cols[2].text)
                        if priority == 1:
                            self._specs[num]["bvi"] += 1
                            self._bvi.append(app_id)
                            if app_id in self._applicants.keys():
                                del self._applicants[app_id]
            async with session.get(self._specs[num]["base_url"]) as resp:
                html = await resp.text()
                bs = BeautifulSoup(html, "html.parser")
                table = bs.find("table")
                for n, row in enumerate(table.find_all("tr", recursive=False), start=1):
                    cols = row.find_all("td")
                    app_id = cols[1].text.replace("-", "").replace(" ", "").strip()
                    priority = int(cols[2].text)
                    if app_id in self._bvi:
                        continue
                    score = int(cols[10].text)
                    if app_id not in self._applicants.keys():
                        self._applicants[app_id] = {}
                    self._applicants[app_id][priority] = [num, score, n]
                    self._concurs_lists[num].append(app_id)
