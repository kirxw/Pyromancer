# spammed int() and str() cuz i kept switching between how i wanted to present ids to lua :sob:

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
    outbound_buffers: dict[int, list[OutboundMessage]]
    highest_recieved_id: int
    current_batch_id: int
    message_buffer: list[OutboundMessage]

    def __init__(self, wguild: WrappedGuild):
        self.wguild = wguild
        self.current_batch_id = 0
        self.highest_recieved_id = 0
        self.outbound_buffers = {}
        self.message_buffer = []

    def process_input(self, input: InboundPollBuffer):
        # get rid of outbound buffers that the server says it's already seen
        for id, buffer in list(self.outbound_buffers.items()):
            if input.HighestRecievedId >= int(id):
                del self.outbound_buffers[id]

        extracted_messages: list[InboundMessage] = []
        previous_highest_recieved = self.highest_recieved_id
        for id, buffer in input.Buffers.items():
            id = int(id)
            self.highest_recieved_id = max(self.highest_recieved_id, id)
            if previous_highest_recieved >= id:
                continue
            extracted_messages.extend(buffer)

        return extracted_messages

    def capture_output(self):
        buffer = self.message_buffer
        self.message_buffer = []

        id = self.current_batch_id
        self.current_batch_id += 1
        self.outbound_buffers[id] = buffer

        return OutboundPollBuffer(
            Buffers=self.outbound_buffers,
            HighestRecievedId=self.highest_recieved_id,
        )
