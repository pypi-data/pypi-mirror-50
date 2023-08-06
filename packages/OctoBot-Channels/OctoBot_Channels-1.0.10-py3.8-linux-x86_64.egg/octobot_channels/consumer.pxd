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

cdef class Consumer:
    cdef object logger          # object type = Logger
    cdef object queue           # object type = asyncio.Queue
    cdef object callback        # object type = CONSUMER_CALLBACK_TYPE
    cdef object consume_task    # object type = asyncio.Task

    cdef bint should_stop
    cdef bint filter_size

    cpdef void start(self)
    cpdef void stop(self)
    cpdef void create_task(self)
    cpdef void run(self)
