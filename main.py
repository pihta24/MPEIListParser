import asyncio
from datetime import datetime
from enum import Enum
from copy import deepcopy
from os import environ
from typing import Awaitable, Callable, Optional

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiorun import run
from bs4 import BeautifulSoup

base_url = "https://pk-mpei.ru/inform/list{}bac{}.html"
API_TOKEN = environ.get("TELEGRAM_TOKEN", "")

sep = 0.1
spec = 0.1

specs = {
    581: {
        "name": "Прикладная математика и информатика МПОВМКС",
        "places": 60,
        "places_target": 6,
        "list": [],
        "bvi": 0
    },
    16: {
        "name": "Прикладная математика и информатика ММ",
        "places": 40,
        "places_target": 4,
        "list": [],
        "bvi": 0
    },
    533: {
        "name": "Строительство",
        "places": 25,
        "places_target": 3,
        "list": [],
        "bvi": 0
    },
    14: {
        "name": "Информатика и вычислительная техника",
        "places": 190,
        "places_target": 29,
        "list": [],
        "bvi": 0
    },
    35: {
        "name": "Прикладная информатика",
        "places": 30,
        "places_target": 3,
        "list": [],
        "bvi": 0
    },
    22: {
        "name": "Информационная безопасность",
        "places": 50,
        "places_target": 15,
        "list": [],
        "bvi": 0
    },
    19: {
        "name": "Беспроводные технологии",
        "places": 100,
        "places_target": 30,
        "list": [],
        "bvi": 0
    },
    10: {
        "name": "Электроника и наноэлектроника",
        "places": 200,
        "places_target": 20,
        "list": [],
        "bvi": 0
    },
    20: {
        "name": "Интеллектуальные системы",
        "places": 85,
        "places_target": 51,
        "list": [],
        "bvi": 0
    },
    15: {
        "name": "Биотехнические системы и технологии, приборостроение",
        "places": 105,
        "places_target": 9,
        "list": [],
        "bvi": 0
    },
    5: {
        "name": "Теплоэнергетика, теплотехника, автоматизация",
        "places": 190,
        "places_target": 28,
        "list": [],
        "bvi": 0
    },
    963: {
        "name": "Экономика и управление на предприятии теплоэнергетики",
        "places": 20,
        "places_target": 4,
        "list": [],
        "bvi": 0
    },
    971: {
        "name": "Промышленная и коммунальная теплоэнергетика",
        "places": 140,
        "places_target": 38,
        "list": [],
        "bvi": 0
    },
    518: {
        "name": "Возобновляемая энергетика",
        "places": 55,
        "places_target": 11,
        "list": [],
        "bvi": 0
    },
    975: {
        "name": "Цифровая электротехника и электроника",
        "places": 225,
        "places_target": 29,
        "list": [],
        "bvi": 0
    },
    13: {
        "name": "Электроэнергетика",
        "places": 320,
        "places_target": 80,
        "list": [],
        "bvi": 0
    },
    4: {
        "name": "Энергетическое машиностроение",
        "places": 96,
        "places_target": 14,
        "list": [],
        "bvi": 0
    },
    7: {
        "name": "Ядерная энергетика и теплофизика",
        "places": 190,
        "places_target": 38,
        "list": [],
        "bvi": 0
    },
    1: {
        "name": "Мехатроника, робототехника и машиностроение",
        "places": 85,
        "places_target": 11,
        "list": [],
        "bvi": 0
    },
    544: {
        "name": "Управление качеством в производственно-технологических системах",
        "places": 25,
        "places_target": 3,
        "list": [],
        "bvi": 0
    },
    17: {
        "name": "Управление в технических системах",
        "places": 75,
        "places_target": 8,
        "list": [],
        "bvi": 0
    },
    540: {
        "name": "Экономика",
        "places": 50,
        "places_target": 8,
        "list": [],
        "bvi": 0
    },
    542: {
        "name": "Менеджмент",
        "places": 30,
        "places_target": 2,
        "list": [],
        "bvi": 0
    },
    588: {
        "name": "Бизнес-информатика",
        "places": 10,
        "places_target": 1,
        "list": [],
        "bvi": 0
    }
}


class Types(Enum):
    bvi = "we"
    base = "c"
    spec = "q"
    sep = "qs"
    target = "t"


applicants: dict = {}
bvi: list = []
updating_list: bool = True
dp: Optional[Dispatcher] = None
last_update: Optional[datetime] = None


async def process_list_mpei(num: int, list_type: Types):
    global applicants
    async with aiohttp.ClientSession() as session:
        match list_type:
            case Types.bvi | Types.base:
                url = base_url.format(num, list_type.value)
        async with session.get(url) as resp:
            html = await resp.text()
            bs = BeautifulSoup(html, "html.parser")
            for table in bs.find_all("table"):
                for n, row in enumerate(table.find_all("tr", {"class": "accepted"}), start=1):
                    cols = row.find_all("td")
                    if len(cols) not in [14, 15]:
                        break
                    app_id = int(cols[0].text.split(":")[1].strip())
                    if list_type == Types.bvi:
                        specs[num]["bvi"] += 1
                        bvi.append(app_id)
                        if app_id in applicants.keys():
                            del applicants[app_id]
                    else:
                        if app_id in bvi:
                            continue
                        score = int(cols[1].text) if list_type != Types.target else int(cols[2])
                        if app_id not in applicants.keys():
                            applicants[app_id] = {}
                        priority = int(cols[10].text if list_type == Types.spec else cols[11].text)
                        applicants[app_id][priority] = [num, score, n]
                        specs[num]["list"].append(app_id)
                else:
                    break


async def update_applicants_mpei():
    global updating_list, last_update, applicants
    updating_list = True
    applicants.clear()
    for i in specs.keys():
        specs[i]["list"].clear()
        specs[i]["bvi"] = 0
    coro = []
    for i in specs.keys():
        coro.append(process_list_mpei(i, Types.base))
        coro.append(process_list_mpei(i, Types.bvi))
    await asyncio.gather(*coro)

    last_update = datetime.now()

    for i in applicants.keys():
        applicants[i] = dict(sorted(applicants[i].items(), key=lambda x: x[0]))

    working_dict = deepcopy(applicants)
    changed = True
    while changed:
        changed = False
        for i in specs.keys():

            places = specs[i]["places"]
            places_target = specs[i]["places_target"]
            places_spec = int(places * spec - 0.1) + 1
            places_sep = int(places * sep - 0.1) + 1
            places_base = places - places_target - places_spec - places_sep - specs[i]["bvi"]

            for j in range(places_base):
                app_id = specs[i]["list"][j]
                if app_id in bvi:
                    changed = True
                    specs[i]["list"].remove(app_id)
                    continue
                priority = 0
                for k, v in working_dict[app_id].items():
                    if v[0] == i:
                        priority = k
                for k in range(priority + 1, max(working_dict[app_id].keys()) + 1):
                    if k in working_dict[app_id]:
                        changed = True
                        specs[working_dict[app_id][k][0]]["list"].remove(app_id)
                        del working_dict[app_id][k]

        await asyncio.sleep(0.05)

    updating_list = False


async def schedule_task(coro: Callable[[], Awaitable], interval: int):
    while True:
        await coro()
        await asyncio.sleep(interval)


async def handle_telegram(message: types.Message):
    global updating_list, last_update
    if updating_list:
        await message.answer("Обновляем списки, попробуйте через минуту")
        return
    if not message.text.isnumeric():
        await message.answer("Принимаем только цифры")
        return
    app_id = int(message.text)
    if app_id not in applicants:
        await message.answer("Абитуриент не найден")
        return
    answer = ""
    for j in applicants[app_id].values():
        places = specs[j[0]]["places"]
        places_target = specs[j[0]]["places_target"]
        places_spec = int(places * spec - 0.1) + 1
        places_sep = int(places * sep - 0.1) + 1
        places_base = places - places_target - places_spec - places_sep
        answer += f"{specs[j[0]]['name']}: {j[2]} место в списке\n" \
                  f"Прогноз: {specs[j[0]]['list'].index(app_id) if app_id in specs[j[0]]['list'] else 'Поступил выше'}\n"\
                  f"Бюджетных мест: {places}\n" \
                  f"Особая квота: {places_spec}\n" \
                  f"Отдельная квота: {places_sep}\n" \
                  f"Целевая квота: {places_target}\n" \
                  f"Бюджетных мест в общем конкурсе: {places_base}\n" \
                  f"Кол-во БВИшников: {specs[j[0]]['bvi']}\n\n"
    answer += f"Обновлено: {last_update.isoformat()}"
    await message.answer(answer)


async def main():
    global dp

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    dp.register_message_handler(handle_telegram)

    asyncio.create_task(dp.start_polling())

    asyncio.create_task(schedule_task(update_applicants_mpei, 3600))


async def shutdown_callback(loop):
    if dp is not None:
        dp.stop_polling()
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await dp.bot.get_session()
        await session.close()
        await dp.wait_closed()


if __name__ == '__main__':
    run(main(), shutdown_callback=shutdown_callback)
