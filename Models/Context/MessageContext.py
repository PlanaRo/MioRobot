from Models.Event.BaseEvent import BaseEvent
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from Utils.Trigger import MessageTrigger

T = TypeVar("T", bound=BaseEvent, covariant=True)


class Commands(ABC, Generic[T]):
    messageData: T
    Trigger: MessageTrigger

    def __init__(self, event: T) -> None:
        self.messageData = event

    @abstractmethod
    async def Reply(self, message):
        pass


class MessageContext(ABC, Generic[T]):
    Event: T
    Command: Commands[T]
