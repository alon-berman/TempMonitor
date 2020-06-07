import json
import os

from ErrorManagement.LoopExceptions import LanguageNotFound

LANG_FILE_DIR = os.path.join('.', 'language_files')


def load_language(lang: str):
    """
    :param lang: string contains which language to load from the Languages/language_files folder
    :return: dictionary containing desired language sentences.
    """
    try:
        json.load(os.path.join(LANG_FILE_DIR, '{}.json'.format(lang)))
    except FileNotFoundError:
        raise LanguageNotFound