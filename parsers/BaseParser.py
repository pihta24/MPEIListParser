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
from copy import deepcopy
from datetime import datetime
from typing import Optional


class BaseParser:
    name: str

    def __init__(self):
        self._applicants: dict[int, dict[int, list[int]]] = dict()
        self._concurs_lists: dict[int, list[int]] = dict()
        self._specs = dict()
        self._bvi = list()
        self._updating_lists: bool = True
        self._processing_lists: bool = True
        self._last_update: Optional[datetime] = None

    @property
    def updating(self):
        return self._updating_lists

    @property
    def processing(self):
        return self._updating_lists or self._processing_lists

    @property
    def last_update(self):
        return self._last_update

    def get_applicant(self, app_id: int):
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
        raise NotImplemented

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
                places_base = places - places_target - places_spec - places_sep - self._specs[i]["bvi"]

                for j in range(places_base):
                    app_id = self._concurs_lists[i][j]
                    if app_id in self._bvi:
                        changed = True
                        self._concurs_lists[i].remove(app_id)
                        continue
                    priority = 0
                    for k, v in working_dict[app_id].items():
                        if v[0] == i:
                            priority = k
                    for k in range(priority + 1, max(working_dict[app_id].keys()) + 1):
                        if k in working_dict[app_id]:
                            changed = True
                            self._concurs_lists[working_dict[app_id][k][0]].remove(app_id)
                            del working_dict[app_id][k]

                await asyncio.sleep(0.01)
        self._processing_lists = False

    async def process_update(self):
        await self.update_lists()
        await self.process_concurs_lists()