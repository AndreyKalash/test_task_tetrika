# URL веб-страницы со списком животных по алфавиту
URL = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту"


# CSS-селектор для получения букв на которые есть животные
ALPHABET_SELECTOR = "ul.ts-module-Индекс_категории-multi-items > li:first-child"

# CSS-селектор для получения букы, под которой находится список животных
LETTER_SELECTOR = "div.mw-category.mw-category-columns h3"

# CSS-селектор для получения списков животных
ANIMALS_LIST_SELECTOR = "div.mw-category.mw-category-columns ul"

# CSS-селектор для получения ссылки на следующую страницу со списками животных
NEXT_PAGE_SELECTOR = "div#mw-pages > a:last-child"
