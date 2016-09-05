from cloudshell.cli.session.session_holder import SessionHolder


class ThreadBasedSessionHolder(SessionHolder):
    def __enter__(self):
        pass


    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
