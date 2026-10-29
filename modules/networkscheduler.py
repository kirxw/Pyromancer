# spammed int() and str() cuz i kept switching between how i wanted to present ids to lua :sob:

import datetime
from typing import TYPE_CHECKING

from structuring import (
    InboundMessage,
    InboundPollBuffer,
    OutboundMessage,
    OutboundPollBuffer,
)

if TYPE_CHECKING:
    from classes.wrappedguild import WrappedGuild


class NetworkScheduler:
    wguild: WrappedGuild
    missing_buffers: dict[int, int]
    outbound_buffers: dict[int, list[OutboundMessage]]
    last_recieved_id: int
    current_batch_id: int

    def __init__(self, wguild: WrappedGuild):
        self.wguild = wguild
        self.last_recieved_id = 0
        self.current_batch_id = 0
        self.missing_buffers = {}
        self.outbound_buffers = {}

    def process_input(self, input: InboundPollBuffer):
        # get rid of outbound buffers that aren't requested anymore
        # TODO GIANT LOGIC ERROR HERE :SCREAM:
        for id, buffer in list(self.outbound_buffers.items()):
            if int(id) not in input.RequestedBuffers:
                del self.outbound_buffers[id]

        now = int(datetime.datetime.now(datetime.UTC).timestamp())

        last_batch = self.last_recieved_id
        self.last_recieved_id = input.CurrentId

        for i in range(last_batch, self.input.CurrentId + 1):
            self.missing_buffers[str(i)] = now

        extracted_messages: list[InboundMessage] = []
        for id, buffer in input.Buffers.items():
            id = str(id)
            if id in self.missing_buffers:
                del self.missing_buffers[str(id)]
                extracted_messages.extend(buffer)

        return extracted_messages

    def add_message_buffer(self, buffer: list[OutboundMessage]):
        id = self.current_batch_id
        self.current_batch_id += 1
        self.outbound_buffers[id] = buffer

    def get_output(self):
        now = int(datetime.datetime.now(datetime.UTC).timestamp())

        missing_buffer_list = []
        for id, send_time in list(self.missing_buffers.items()):
            if now - send_time > 60:
                del self.missing_buffers[id]
            else:
                missing_buffer_list.append(int(id))

        return OutboundPollBuffer(
            Buffers=self.outbound_buffers,
            RequestedBuffers=missing_buffer_list,
            CurrentId=id,
        )
