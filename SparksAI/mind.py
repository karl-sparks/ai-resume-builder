from datetime import datetime


class Mind:
    def __init__(
        self,
        system: str,
        persona: str,
        goals: str,
        perception: str,
        feelings: str,
        thoughts: str,
    ):
        self._system = system
        self._persona = persona
        self._goals = goals
        self._perception = perception
        self._feelings = feelings
        self._thoughts = thoughts

    def __repr__(self) -> str:
        return "\n".join(
            [
                "<mind>",
                "<system>",
                self._system,
                "</system>",
                "\n",
                "<persona>",
                self._persona,
                "</persona>",
                "\n",
                "<goals>",
                self._goals,
                "</goals>",
                "\n",
                "<perception>",
                self._perception,
                "</perception>",
                "\n",
                "<feelings>",
                self._feelings,
                "</feelings>",
                "\n",
                "<thoughts>",
                self._thoughts,
                "</thoughts>",
                "</mind>",
            ]
        )

    def add_thought(self, thought: str) -> None:
        formated_thought = f'You thought "{thought}" at {datetime.now()}'

        self._thoughts = self._thoughts + "\n" + formated_thought
