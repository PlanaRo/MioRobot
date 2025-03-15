class MessageTrigger:
    # 是否触发了事件
    triggered: bool
    # 是否中断
    interrupt: bool
    # 触发的次数
    triggerNumber: int

    def __init__(self) -> None:
        self.triggered = False
        self.interrupt = False
        self.triggerNumber = 0

    def update(self):
        """
        更新触发状态
        """
        self.triggered = True
        self.triggerNumber += 1
        self.interrupt = True

    def setInterrupt(self, state: bool):
        """
        设置中断
        """
        self.interrupt = state

    def isInterrupt(self) -> bool:
        return self.interrupt

    def isTriggered(self) -> bool:
        return self.triggered
