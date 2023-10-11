import g4f


def get_user_input():
    return input("\n> ")


def get_bot_response(user_input):
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}],
        stream=True,
    )

    for message in response:
        print(message, flush=True, end='')


def main():
    print("Welcome to GPT-3.5 Turbo, the best chatbot ever!")
    print("Type something to begin...", end='')

    while True:
        user_input = get_user_input()
        get_bot_response(user_input)


if __name__ == "__main__":
    main()