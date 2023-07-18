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
from os import environ
from typing import Awaitable, Callable, Optional

from aiogram import Bot, Dispatcher, types
from aiorun import run

from parsers import BaseParser, MPEIParser, MIREAParser, STANKINParser, MAIParser

API_TOKEN = environ.get("TELEGRAM_TOKEN", "")

bot: Optional[Bot] = None
dp: Optional[Dispatcher] = None
parsers: list[BaseParser] = []


async def schedule_task(coro: Callable[[], Awaitable], interval: int):
    while True:
        await coro()
        await asyncio.sleep(interval)


async def handle_telegram(message: types.Message):
    app_id = message.text.replace("-", "").replace(" ", "")
    for parser in parsers:
        answer = f"*{parser.name}:*\n"
        if parser.updating:
            answer += "Обновляем списки, попробуйте через несколько секунд"
            await bot.send_message(message.chat.id, answer, types.ParseMode.MARKDOWN_V2)
            continue
        applicant = parser.get_applicant(app_id)
        if applicant == (None, None):
            answer += "Абитуриент не найден"
            await bot.send_message(message.chat.id, answer, types.ParseMode.MARKDOWN_V2)
            continue
        a = []
        for i, j in enumerate(applicant[0].values()):
            a.append((j, applicant[1][i] if applicant[1] else None))
        for i, j in a:
            spec = parser.get_spec(i[0])
            places = spec["places"]
            places_target = spec["places_target"]
            places_spec = spec["places_spec"]
            places_sep = spec["places_sep"]
            places_base = places - places_target - places_spec - places_sep
            if parser.processing:
                predict = "Идёт обработка списков, попробуйте через минуту"
            else:
                predict = f"*{j}* место в конкурсном списке после распределения" if j \
                    else "__*Поступил на более высокий приоритет*__"
                if j:
                    if j <= places_base:
                        predict += "\n__*Поступил на это направление*__"
            answer += f"__{spec['name']}:__\n" \
                      f"Количество баллов с учётом ИД: _{i[1]}_\n" \
                      f"*{i[2]}* место в текущем конкурсном списке\n" \
                      f"Прогноз: {predict}\n" \
                      f"Бюджетных мест: _{places}_\n" \
                      f"Особая квота: _{places_spec}_\n" \
                      f"Отдельная квота: _{places_sep}_\n" \
                      f"Целевая квота: _{places_target}_\n" \
                      f"Бюджетных мест в общем конкурсе: _{places_base}_\n"
            if "count" in spec:
                count = spec["count"]
                count_target = spec["count_target"]
                count_spec = spec["count_spec"]
                count_sep = spec["count_sep"]
                answer += f"Кол-во заявлений всего: _{count}_\n" \
                          f"Кол-во заявлений по особой квоте: _{count_spec}_\n" \
                          f"Кол-во заявлений по отдельной квоте: _{count_sep}_\n" \
                          f"Кол-во заявлений по целевой квоте: _{count_target}_\n" \
                          f"Кол-во БВИшников: _{spec['bvi']}_\n\n"
            else:
                answer += f"Кол-во БВИшников: _{spec['bvi']}_\n\n"
        answer += f"Обновлено: _{parser.last_update.isoformat(' ', 'seconds')}_"
        answer = answer.replace("-", r"\-").replace("(", r"\(").replace(")", r"\)")
        await bot.send_message(message.chat.id, answer, types.ParseMode.MARKDOWN_V2)


async def main():
    global bot, dp, parsers

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    dp.register_message_handler(handle_telegram)

    mpei_parser = MPEIParser()
    mirea_parser = MIREAParser()
    stankin_parser = STANKINParser()
    mai_parser = MAIParser()

    await mai_parser.init()

    parsers = [mpei_parser, mirea_parser, stankin_parser, mai_parser]

    asyncio.create_task(dp.start_polling())

    asyncio.create_task(schedule_task(mpei_parser.process_update, 3600))
    asyncio.create_task(schedule_task(mirea_parser.process_update, 3600))
    asyncio.create_task(schedule_task(stankin_parser.process_update, 3600))
    asyncio.create_task(schedule_task(mai_parser.process_update, 3600))


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
