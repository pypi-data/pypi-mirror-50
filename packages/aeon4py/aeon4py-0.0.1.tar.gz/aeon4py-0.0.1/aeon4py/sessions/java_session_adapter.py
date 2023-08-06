from aeoncloud.sessions.session_adapter import ISessionAdapter


class JavaSessionAdapter(ISessionAdapter):

    def __init__(self, session):
        self.session = session

    def execute_command(self, command, arguments):
        self.session.executeCommand(command, arguments)

    def quit_session(self) -> None:
        self.session.quitSession()
