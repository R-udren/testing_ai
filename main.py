import g4f
from rich.prompt import Prompt
from rich import print
from rich.console import Console


def get_user_input():
    return Prompt.ask("\n[yellow]You[/yellow]")


def get_bot_response(messages):
    print("[magenta]G4F: ", end='')
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
    )

    for message in response:
        print(message, end='')


def main():
    console = Console()
    try:
        print("[green]Type your message below. Press Ctrl+C to exit.[/green]", end='')
        messages = []
        while True:
            messages.append({"role": "user", "content": get_user_input()})
            messages.append({"role": "bot", "content": get_bot_response(messages)})
    except KeyboardInterrupt:
        print("\n[red]Exiting...[/red]")
    except:
        console.print_exception()


if __name__ == "__main__":
    main()
