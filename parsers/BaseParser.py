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
import os
from copy import deepcopy
from datetime import datetime
from typing import Optional, Any


class BaseParser:
    name: str
    update_type: str

    def __init__(self):
        self._applicants: dict[str, dict[int, list[Any]]] = dict()
        self._concurs_lists: dict[Any, list[str]] = dict()
        self._specs = dict()
        self._bvi = list()
        self._updating_lists: bool = True
        self._processing_lists: bool = True
        self._last_update: Optional[datetime] = None
        self.last_update_failed = False
        self._last_update_started = None

    @property
    def updating(self):
        return self._updating_lists

    @property
    def processing(self):
        return self._updating_lists or self._processing_lists

    @property
    def last_update(self):
        return self._last_update

    @property
    def last_update_started(self):
        return self._last_update_started

    @property
    def applicants(self):
        return self._applicants

    def get_applicant(self, app_id: str):
        if self._updating_lists:
            return None, None
        if app_id not in self._applicants:
            return None, None
        positions = self._applicants[app_id]
        if self._processing_lists:
            return positions, None
        predictions = [self._concurs_lists[i[0]].index(app_id) if app_id in self._concurs_lists[i[0]]
                       else None for i in self._applicants[app_id].values()]
        return positions, predictions

    def get_spec(self, spec_id: int):
        if spec_id in self._specs:
            return self._specs[spec_id]

    async def update_lists(self):
        self._updating_lists = True
        self._processing_lists = True
        self._applicants.clear()
        self._concurs_lists = {i: [] for i in self._specs.keys()}
        self._bvi.clear()
        for i in self._specs.keys():
            self._specs[i]["bvi"] = 0
        match self.update_type:
            case "parallel":
                coro = []
                for i in self._specs.keys():
                    coro.append(self._parse_list(i))
                await asyncio.gather(*coro)
            case "series":
                for i in self._specs.keys():
                    await self._parse_list(i)
            case _:
                raise NotImplemented("Implement update_lists or set update_type")

        self._last_update = datetime.now()

        for i in self._applicants.keys():
            self._applicants[i] = dict(sorted(self._applicants[i].items(), key=lambda x: x[0]))
        self._updating_lists = False

    async def process_concurs_lists(self):
        self._processing_lists = True
        working_dict = deepcopy(self._applicants)
        changed = True
        while changed and not self._updating_lists:
            changed = False
            for i in self._specs.keys():

                places = self._specs[i]["places"]
                places_target = self._specs[i]["places_target"]
                places_spec = self._specs[i]["places_spec"]
                places_sep = self._specs[i]["places_sep"]
                if "count" in self._specs[i]:
                    count_target = self._specs[i]["count_target"]
                    count_spec = self._specs[i]["count_spec"]
                    count_sep = self._specs[i]["count_sep"]
                    places_base = places \
                                  - min(places_target, count_target) \
                                  - min(places_spec, count_spec) \
                                  - min(places_sep, count_sep) \
                                  - self._specs[i]["bvi"]
                else:
                    places_base = places - places_target - places_spec - places_sep - self._specs[i]["bvi"]

                for j in range(min(places_base, len(self._concurs_lists[i]))):
                    app_id = self._concurs_lists[i][j]
                    while self._concurs_lists[i].count(app_id) != 1:
                        self._concurs_lists[i].remove(app_id)
                        changed = True
                    if app_id in self._bvi:
                        changed = True
                        self._concurs_lists[i].remove(app_id)
                        continue
                    priority = max(working_dict[app_id].keys())
                    for k, v in working_dict[app_id].items():
                        if v[0] == i:
                            priority = k
                            break
                    for k in range(priority + 1, max(working_dict[app_id].keys()) + 1):
                        if k in working_dict[app_id]:
                            changed = True
                            while self._concurs_lists[working_dict[app_id][k][0]].count(app_id) != 0:
                                self._concurs_lists[working_dict[app_id][k][0]].remove(app_id)
                            del working_dict[app_id][k]

                await asyncio.sleep(0.02)
        self._processing_lists = False

    async def process_update(self):
        self._last_update_started = datetime.now()
        await self.update_lists()
        await self.process_concurs_lists()

    async def _parse_list(self, num: Any):
        raise NotImplemented
