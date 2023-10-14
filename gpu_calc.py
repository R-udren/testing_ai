from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


def get_resolution():
    console.print("[bold cyan]Выбери разрешение:")
    selected_resolution = Prompt.ask(
        "[green_yellow]1. 1080p\n"
        "2. 1440p\n"
        "3. 2160p\n[/green_yellow]",
        choices=['1', '2', '3']
    )

    match selected_resolution:
        case '2':
            from gpus import card_1440p
            data_str = card_1440p
            selected_resolution = 'QuadHD - 1440p (2K QHD)'
        case '3':
            from gpus import card_2160p
            data_str = card_2160p
            selected_resolution = 'UltraHD - 2160p (4K UHD)'
        case _:
            from gpus import card_1080p
            data_str = card_1080p
            selected_resolution = 'FullHD - 1080p (FHD)'
    return data_str, selected_resolution


def convert_data(data_str):
    converted_data = {}
    for line in data_str.strip().split('\n'):
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

    while True:
        console.print(table)
        index = Prompt.ask(
            "[cyan1]Выбери порядковый номер видеокарты [/cyan1][red](0 для выхода)[/red]",
            default='0',
            show_default=False
        )
        try:
            if index.isdigit():
                index = int(index)
            elif index in gpu_names:
                index = gpu_names.index(index) + 1
            else:
                raise ValueError
        except ValueError:
            console.print("[red]Введено неверное значение![/red]")
            continue

        if len(gpu_names) >= index >= 1 and gpu_names[index - 1] not in selected_gpus:
            gpu = gpu_names[index - 1]
            try:
                price = float(Prompt.ask(
                    f"[magenta]Введи цену для [bold]{gpu}[/bold]",
                    default='0',
                    show_default=False
                ))

                if price <= 0:
                    raise ValueError("Цена должна быть положительной.")

                price_per_fps = round(price / cards_data[gpu], 2)

            except ValueError as e:
                console.print(f"[red]{e}[/red]")
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
            console.print("[red]Введено неправильное значение - ты лещ.[/red]")
            continue

    return selected_gpus


def most_profitable(selected_cards, selected_resolution):
    if not selected_cards:
        console.print("[red]Ты не выбрал ни одной видеокарты![/red]")
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
    try:
        data_string, resolution = get_resolution()
        data = convert_data(data_string)
        created_table = create_table(data)
        selected = get_price_per_fps(data, created_table)
        most_profitable(selected, resolution)
    except KeyboardInterrupt:
        console.print("\n[red]Программа прервана пользователем![/red]")
    except:
        console.print_exception(extra_lines=2)


if __name__ == "__main__":
    main()
    console.input("\n\n[bold yellow]Нажми Enter чтобы закрыть программу...")
