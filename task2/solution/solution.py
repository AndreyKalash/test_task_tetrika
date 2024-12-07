import asyncio
from logic import get_count_animals_by_letter, create_csv_report


def main():
    data = asyncio.run(get_count_animals_by_letter())
    create_csv_report(data, "animals_count_report.csv")
    print("Данные успешно сохранены")


if __name__ == "__main__":
    main()
