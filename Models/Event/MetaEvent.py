from Models.Event.BaseEvent import BaseEvent


class MetaEvent(BaseEvent):

    def __init__(self, data: dict):

        self.Post_Type = data.get("post_type", None)
