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
    sender_ag = None
    receivers = None
    message = None

    def __init__(self, conversation_id, receivers=None, sender_ag=None, message: Message=None):
        self.conversation_id = conversation_id
        self.sender_ag = sender_ag
        self.receivers = receivers
        self.message = message

    def __str__(self):
        return f"Id: {self.conversation_id}\nSender: {self.sender_ag}\nReceivers: {self.receivers}\nMessage: {self.message}"
    
    def setSender(self, agent):
        self.sender_ag = agent

    def addReceivers(self, agentsId: list):
        self.receivers = agentsId

    def addContent(self, message: Message):
        self.message = message

