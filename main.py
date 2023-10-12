import g4f
from rich.prompt import Prompt
from rich import print


def get_user_input():
    return Prompt.ask("\n[yellow]You[/yellow]")


def get_bot_response(user_input):
    print("[blue]G4F: ", end='')
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}],
        stream=True,
    )

    for message in response:
        print(message, end='')


def main():
    try:
        print("[green]Type your message below. Press Ctrl+C to exit.[/green]", end='')
        while True:
            user_input = get_user_input()
            get_bot_response(user_input)
    except KeyboardInterrupt:
        print("\n[red]Exiting...[/red]")


if __name__ == "__main__":
    main()
