import config as c
from async_requests import get_page_data

import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


async def gel_alphabet() -> list[str] | None:
    """
    Асинхронно извлекает и возвращает список букв алфавита с первой страницы.

    Returns:
        list[str]: Список букв, представленных на странице.

    Raises:
        ValueError: Если список букв пуст.
    """
    # получение HTML главной страницы
    data = await get_page_data(c.URL)
    soup = BeautifulSoup(data, "html.parser")
    # получение букв с первой страницы
    elements = soup.select(c.ALPHABET_SELECTOR)
    if not elements:
        raise ValueError("Не удалось извлечь буквы из HTML.")

    letters = [element.text.upper() for element in elements]
    return letters


async def get_count_animals_by_letter() -> dict[str, int]:
    """
    Асинхронно проходит по страницам категории животных, сгруппированных по алфавиту,
    и подсчитывает количество животных на каждую букву.

    Returns:
        dict[str, int]: Словарь, где ключ - буква, значение - количество животных.
    """
    # получение списка букв алфавита для ограничения по буквам
    letters = await gel_alphabet()
    if not letters:
        return {}

    count_animals_by_letter = {}
    processed_letters = set()  # множество для отслеживания уже обработанных букв
    total_letters = len(letters)

    # словарь для хранения общей информации о количестве животных по буквам
    count_animals_by_letter = {}

    next_page = c.URL

    while next_page:
        # получение html страницы
        data = await get_page_data(next_page)
        soup = BeautifulSoup(data, "html.parser")

        animal_div_lists = soup.select(
            c.ANIMALS_LIST_SELECTOR
        )  # список с блоками списков с животными
        letters_on_page = soup.select(c.LETTER_SELECTOR)  # список с буквами на странице

        # получение ссылку на следующую страницу, если она есть
        try:
            next_page_part_url = soup.select_one(c.NEXT_PAGE_SELECTOR)
            next_page_part_url = (
                next_page_part_url.get("href") if next_page_part_url else None
            )
            next_page = (
                urljoin(c.URL, next_page_part_url) if next_page_part_url else None
            )
        except AttributeError:
            # Если не удалось получить ссылку, значит нет следующей страницы
            next_page = None

        # цикл по всем буквам на странице
        for i, letter_tag in enumerate(letters_on_page):
            current_letter = letter_tag.text.strip().upper()

            # если на странице появилась буква, которой нет в общем списке,
            # значит мы достигли конца нужных данных
            if current_letter not in letters and len(count_animals_by_letter) >= len(
                letters
            ):
                next_page = None
                break

            # список животных для текущей буквы
            animals_list = animal_div_lists[i].find_all("li")

            # обновление количества животных для текущей буквы
            letter_animals_count = count_animals_by_letter.setdefault(current_letter, 0)
            letter_animals_count += len(animals_list)
            count_animals_by_letter[current_letter] = letter_animals_count

            if current_letter not in processed_letters:
                processed_letters.add(current_letter)

                # Расчет прогресса
                progress_fraction = len(processed_letters) / total_letters
                bar_length = 30
                filled_length = int(bar_length * progress_fraction)
                bar = "#" * filled_length + "-" * (bar_length - filled_length)

                # Выводим прогресс в одну строку, используя \r для возврата в начало строки
                print(
                    f"\rПрогресс обработки: [{bar}] {len(processed_letters)}/{total_letters} букв | "
                    f"Текущая буква: {current_letter}",
                    end="",
                    flush=True,
                )

    print()  # переход на новую строку после завершения

    return count_animals_by_letter


def create_csv_report(data: dict[str, int], file_name: str) -> None:
    """
    Создает CSV-отчет из данных о количестве животных по буквам.

    Args:
        data (dict[str, int]): Словарь, где ключ - буква, значение - количество животных.
        file_name (str): Имя выходного CSV-файла.
    """

    # преобразование словаря в DataFrame
    df = pd.DataFrame(data=list(data.items()))
    try:
        # запись данных в CSV-файл без заголовка и индексов
        df.to_csv(file_name, sep=",", index=False, header=False)
    except Exception as e:
        raise Exception(f"Не удалось сохранить CSV-файл '{file_name}': {e}")
