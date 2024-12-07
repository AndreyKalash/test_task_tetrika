from aiohttp import ClientSession, ClientError


async def get_page_data(url: str) -> str:
    """
    Получает содержимое веб-страницы по указанному URL в виде текста.

    Args:
        url (str): URL-адрес веб-страницы, которую необходимо получить.

    Returns:
        str: Текстовое содержимое веб-страницы.
    """
    try:
        async with ClientSession() as session:
            # асинхронный GET-запрос к указанному URL
            response = await session.get(url)

            # чтение и возврат текст ответа
            data = await response.text()
            return data
    except ClientError as e:
        raise ClientError(f"Не удалось получить данные с {url}: {e}")
