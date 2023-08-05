# cython: language_level=3
#  Drakkar-Software OctoBot-Channels
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import asyncio
from queue import Queue

from octobot_commons.logging.logging_util import get_logger

from octobot_channels import CONSUMER_CALLBACK_TYPE


class Consumer:
    def __init__(self, callback: CONSUMER_CALLBACK_TYPE, size: int = 0, filter_size: bool = False):
        self.logger = get_logger(self.__class__.__name__)

        self.queue = Queue(maxsize=size)
        self.callback = callback
        self.consume_task = None
        self.should_stop = False
        self.filter_size = filter_size

    async def consume(self):
        """
        Should implement self.queue.get() in a while loop

        while not self.should_stop:
            self.callback(await self.queue.get())

        :return:
        """
        raise NotImplemented("consume is not implemented")

    def start(self):
        """
        Should be implemented for consumer's non-triggered tasks
        :return:
        """
        pass

    def stop(self):
        """
        Stops non-triggered tasks management
        :return:
        """
        self.should_stop = True

    def create_task(self):
        self.consume_task = asyncio.create_task(self.consume())

    def run(self):
        self.start()
        self.create_task()
