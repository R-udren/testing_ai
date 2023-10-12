import speedtest
from ping3 import ping
from rich.console import Console
from rich import print


def format_bytes(raw_bytes):
    units = ['bytes', 'Kb', 'Mb', 'Gb', 'Tb']
    i = 0
    while raw_bytes >= 1024:
        raw_bytes /= 1024
        i += 1
    return f'{raw_bytes:.2f} {units[i]}'


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

    download_speed = format_bytes(st.download())
    upload_speed = format_bytes(st.upload())

    return (f'[blue]Download speed: {download_speed}ps[/blue]',
            f'[magenta]Upload speed: {upload_speed}ps[/magenta]')


def main():
    host_to_ping = "google.com"
    console = Console()

    with console.status("[bold green]Checking internet speed...\n") as status:
        try:
            download_speed, upload_speed = check_speed()
            ping_result = check_ping(host_to_ping)
        except:
            console.print_exception()
            return
        finally:
            status.stop()
        print(ping_result)
        print(download_speed)
        print(upload_speed)


if __name__ == "__main__":
    main()
