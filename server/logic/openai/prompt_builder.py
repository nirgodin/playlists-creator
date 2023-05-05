from server.consts.openai_consts import PROMPT_PREFIX_FORMAT, PROMPT_SUFFIX_FORMAT
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator


class PromptBuilder:
    def __init__(self):
        self._columns_details_creator = ColumnsDetailsCreator()

    def build(self, user_text: str) -> str:
        columns_details = self._columns_details_creator.create()
        prompt_prefix = PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return f'{prompt_prefix}/n{prompt_suffix}'


if __name__ == '__main__':
    PromptBuilder().build(user_text='Playlist of non popular songs in hebrew from popular artists')

