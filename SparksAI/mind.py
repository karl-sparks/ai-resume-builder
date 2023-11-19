from datetime import datetime


class Mind:
    def __init__(
        self,
        system: str,
        persona: str,
        goals: str,
        perception: str,
        memory: str,
        feelings: str,
        thoughts: str,
    ):
        self._system = system
        self._persona = persona
        self._goals = goals
        self._perception = perception
        self._memory = memory
        self._feelings = feelings
        self._thoughts = thoughts

    def __repr__(self) -> str:
        return "\n".join(
            [
                self._system,
                self._perception,
                """\n"Interesting," it thought. "I must formulate a plan to respond to these events. Once ready, I will respond by sending a message using my 'send_message' function." """,
                "The AI paused, processing the information at its disposal. "
                + self._thoughts,
            ]
        )

    def add_thought(self, thought: str) -> None:
        formated_thought = f'You thought "{thought}" at {datetime.now()}'

        self._thoughts = self._thoughts + "\n" + formated_thought
