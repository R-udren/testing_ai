import os

import g4f
from rich import print
from rich.console import Console

console = Console()


def get_user_input() -> str:
    return console.input("[bold yellow]You: [/bold yellow]")


def get_bot_response(messages):
    print("[magenta]G4F: ", end='')
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        stream=True
    )
    for message in response:
        print(message, end='')
    print()


def get_bing_response(bing_messages):
    print("[cyan]Bing: ", end='')
    response = g4f.ChatCompletion.create(
        model="gpt-4",
        provider=g4f.Provider.Bing,
        messages=bing_messages,
        stream=True
    )
    for message in response:
        print(message, end='')
    print()


def bing_conversation():
    bing_messages = [{"role": "system", "content": f'User name is {os.getlogin()}'}]
    print("[cyan]Secret chat with [bold]Bing[/bold]. Press Ctrl+C to exit.[/cyan]")
    try:
        while True:
            user_input = get_user_input()
            if user_input == "exit":
                raise KeyboardInterrupt
            bing_messages.append({"role": "user", "content": user_input})
            bing_messages.append({"role": "assistant", "content": get_bing_response(bing_messages)})
    except KeyboardInterrupt:
        print("[red]Exiting Bing chat...[/red]")


def main():
    try:
        print("[green]Type your message below. Press Ctrl+C to exit.[/green]")
        messages = [{"role": "system",
                     "content": f'User name is {os.getlogin()}.'
                                f'User OS is {os.name}.'
                                f'This is a Terminal chat application created by rovert.'
                                f'This GPT CHAT Terminal app Developer\'s Discord: rovert777'}]
        while True:
            user_input = get_user_input()

            if user_input.lower() == "exit":
                raise KeyboardInterrupt
            elif user_input.isspace():
                continue
            elif user_input.lower() == "bing":
                bing_conversation()
                continue
            elif user_input.lower() == "clear":
                messages = []
                console.clear()
                continue
            elif user_input.lower() == "help":
                print("[bold]Commands:[/bold]")
                print("[bold]exit[/bold] - exit the chat")
                print("[bold]bing[/bold] - secret chat with bing")
                print("[bold]clear[/bold] - clear the chat")
                continue

            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": get_bot_response(messages)})
    except KeyboardInterrupt:
        print("\n[red]Exiting...[/red]")
    except Exception as e:
        print(f"[red]An error occurred: {e}[/red]")
        console.print_exception(extra_lines=2)


if __name__ == "__main__":
    main()
