import autogen


def bot_manager():
    def __init__(self) -> None:
        config_list = autogen.config_list_from_dotenv()

        self.assistant = autogen.AssistantAgent(
            name="assistant", llm_config={"config_list": config_list}
        )

        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="TERMINATE",
            code_execution_config={"work_dir": "agent_code_executions"},
        )

    def ask_agent(self, message: str) -> str:
        self.user_proxy.ini
