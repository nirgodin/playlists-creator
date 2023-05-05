from server.logic.openai.columns_details_creator import ColumnsDetailsCreator


class PromptBuilder:
    def __init__(self):
        self._columns_details_creator = ColumnsDetailsCreator()

    def build(self) -> str:
        columns_details = self._columns_details_creator.create()
        print('b')


if __name__ == '__main__':
    PromptBuilder().build()
