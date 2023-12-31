import speedtest
from ping3 import ping
from rich.console import Console
from rich import print


def format_bits(raw_bits):
    units = ['b', 'Kb', 'Mb', 'Gb', 'Tb']
    i = 0
    while raw_bits >= 1024:
        raw_bits /= 1024
        i += 1
    return f'{raw_bits:.2f} {units[i]}'


# Function to check ping
def check_ping(host):
    response_time = round(ping(host), 3)
    if response_time is not None:
        return f'[green]Ping to {host} is {response_time} ms[/green]'
    else:
        return f'[red]Could not reach {host}[/red]'


# Function to check download and upload speeds
def check_speed():
    st = speedtest.Speedtest()
    st.get_best_server()  # Find the best server

    download_speed = format_bits(st.download())
    upload_speed = format_bits(st.upload())

    return (f'[blue]Download speed: {download_speed}ps[/blue]',
            f'[magenta]Upload speed: {upload_speed}ps[/magenta]')


def main():
    host_to_ping = "google.com"
    console = Console(style="bold cyan")

    with console.status("[bold green]Checking internet speed...\n", spinner='bouncingBall') as status:
        try:
            download_speed, upload_speed = check_speed()
            ping_result = check_ping(host_to_ping)
        except:
            console.print_exception(extra_lines=2)
            return

        finally:
            status.stop()
        print(ping_result)
        print(download_speed)
        print(upload_speed)
    console.input("\n[bold yellow]Press Enter to exit...[/bold yellow]")


if __name__ == "__main__":
    main()
