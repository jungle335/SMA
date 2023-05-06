class Message:
    agPosition = None
    agNextAction = None
    agHoldingTileColor = None

    def __init__(self, agPosition=None, agNextAction=None, agHoldingTileColor=None):
        self.agPosition = agPosition
        self.agNextAction = agNextAction
        self.agHoldingTileColor = agHoldingTileColor

    def __str__(self):
        return f"Message with content:\n Agent -> Position: {self.agPosition}, Next Action: {self.agNextAction}, If holding, color: {self.agHoldingTileColor}"

class AgentMessage:
    conversation_id = None
    sender_id = None
    receivers = None
    message = None

    def __init__(self, conversation_id, receivers=None, sender_id=None, message: Message=None):
        self.conversation_id = conversation_id
        self.sender_id = sender_id
        self.receivers = receivers
        self.message = message

    def __str__(self):
        return f"Id: {self.conversation_id}\nSender: {self.sender_id}\nReceivers: {self.receivers}\nMessage: {self.message}"
    
    def setSender(self, agendtId):
        self.sender_id = agendtId

    def addReceivers(self, agentsId: list):
        self.receivers = agentsId

    def addContent(self, message: Message):
        self.message = message

