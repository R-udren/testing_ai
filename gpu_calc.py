from gpus import card_1080p, card_1440p, card_2160p
from rich import print
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt


def get_resolution():
    print(f"[bold cyan]"
          f"1. 1080p\n"
          f"2. 1440p\n"
          f"3. 2160p"
          f"[/bold cyan]")
    selected_resolution = int(Prompt.ask("[green_yellow]Выбери разрешение", choices=['1', '2', '3']))

    match selected_resolution:
        case 2:
            data_str = card_1440p
            selected_resolution = 'QuadHD - 1440p (2K QHD)'
        case 3:
            data_str = card_2160p
            selected_resolution = 'UltraHD - 2160p (4K UHD))'
        case _:
            data_str = card_1080p
            selected_resolution = 'FullHD - 1080p (FHD)'
    return data_str, selected_resolution


def convert_data(data_str):
    data_lines = data_str.strip().split('\n')
    converted_data = {}
    for line in data_lines:
        gpu, value = line.split(' - ')
        value = int(value.replace(' FPS', ''))
        converted_data[gpu] = value
    return converted_data


def create_table(cards_data):
    card_table = Table(title="Выбери видеокарту", show_header=True, header_style="bold cyan")

    # Добавление заголовков
    card_table.add_column("No.", style="cyan")
    card_table.add_column("Graphics Card", style="magenta")
    card_table.add_column("FPS", style="green")

    # Добавление данных в таблицу
    for i, gpu in enumerate(cards_data.keys(), start=1):
        card_table.add_row(f'{i}.', gpu, str(cards_data[gpu]) + ' FPS')
    return card_table


def get_price_per_fps(cards_data, table):
    gpu_names = list(cards_data.keys())
    selected_gpus = {}
    console.print(table)
    while True:
        index = Prompt.ask("\n[cyan1]Выбери порядковый номер видеокарты [#FF4444](0 для выхода)", default='0',
                           show_default=False)
        try:
            if index.isdigit():
                index = int(index)
            elif index in gpu_names:
                index = gpu_names.index(index) + 1
            else:
                raise ValueError
        except ValueError:
            console.print("Введено неверное значение!", style="red")
            continue

        if len(gpu_names) >= index >= 1 and gpu_names[index - 1] not in selected_gpus:
            gpu = gpu_names[index - 1]
            try:
                price = float(Prompt.ask(f"[magenta]Введи цену для [bold]{gpu}", default='0', show_default=False))

                if price <= 0:
                    raise ValueError

                price_per_fps = round(price / cards_data[gpu], 2)

            except ValueError:
                console.print("Введено неверное значение!", style="red")
                continue

            console.print(table)
            console.print(f"\n[bold]Информация о {gpu}:[/bold]\n"
                          f"- Цена: [bold cyan]{price:.2f}[/bold cyan]\n"
                          f"- FPS: [bold green]{cards_data[gpu]}[/bold green]\n"
                          f"- Цена за FPS: [bold magenta]{price_per_fps:.2f}[/bold magenta]")

            selected_gpus[gpu] = {
                'FPS': cards_data[gpu],
                'Price': price,
                'Price per FPS': price_per_fps
            }

        elif index == 0:
            break
        else:
            console.print("Введено неправильное значение - ты лещ.", style="red")
            continue

    return selected_gpus


def most_profitable(selected_cards, selected_resolution):
    if not selected_cards:
        console.print("Ты не выбрал ни одной видеокарты!", style="red")
        return

    console.print("\n" * 2 + f"[green1]Разрешение [bold green]{selected_resolution}[/bold green].")
    console.print("[bold yellow]Самая выгодная видеокарта - первая в списке")

    table = Table(header_style="bold magenta1", show_header=True)

    # Добавление заголовков
    table.add_column("№", style="cyan")
    table.add_column("GPU", style="magenta")
    table.add_column("FPS", style="green")
    table.add_column("Цена", style="cyan")
    table.add_column("Цена за FPS", style="magenta")

    # Добавление данных в таблицу
    selected_cards = dict(sorted(selected_cards.items(), key=lambda item: item[1]['Price per FPS']))
    for i, (card_name, card_info) in enumerate(selected_cards.items(), start=1):
        table.add_row(
            str(i),
            card_name,
            str(card_info['FPS']),
            f"{card_info['Price']:.2f}",
            f"{card_info['Price per FPS']:.2f}"
        )

    # Вывод таблицы
    console.print(table)

    return selected_cards


def main():
    data_string, resolution = get_resolution()

    data = convert_data(data_string)

    created_table = create_table(data)

    selected = get_price_per_fps(data, created_table)
    most_profitable(selected, resolution)


if __name__ == "__main__":
    console = Console()
    main()
    console.input("\n\n[bold yellow]Нажми Enter чтобы закрыть программу...")
