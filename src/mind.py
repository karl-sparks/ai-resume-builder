import os
from collections import defaultdict


class Mind:
    def __init__(self, path_to_mind_files: str, path_to_starters: str) -> None:
        self.mind_file_root = path_to_mind_files
        self.starter_file_root = path_to_starters

        with open(
            self.starter_file_root + "unknown-user-starter.md", "r", encoding="utf-8"
        ) as file:
            default_mind = file.read()

        self.mind_files = defaultdict(lambda: default_mind)

        file_names = os.listdir(self.mind_file_root)

        for file_name in file_names:
            mind_name = os.path.basename(file_name).split("-", 1)[0]

            with open(self.mind_file_root + file_name, "r", encoding="utf-8") as file:
                file_text = file.read()

            self.mind_files[mind_name] = file_text

        if "core" not in self.mind_files:
            with open(
                self.starter_file_root + "core-file-starter.md", "r", encoding="utf-8"
            ) as file:
                file_text = file.read()

            self.mind_files["core"] = file_text

    def save_mind_files(self):
        for name, content in self.mind_files.items():
            file_path = self.mind_file_root + name + "-mind-file.md"

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

    def update_mind_file(self, file_name: str, content: str):
        self.mind_files[file_name] = content

    def get_mind_file(self, file_name: str) -> str:
        return self.mind_files[file_name]
