import speedtest
from ping3 import ping
from rich.console import Console
from rich import print
import time


# Function to check ping
def check_ping(host):
    response_time = ping(host)
    if response_time is not None:
        return f'[green]Ping to {host} is {response_time:0.3f} ms[/green]'
    else:
        return f'[red]Could not reach {host}[/red]'


# Function to check download and upload speeds
def check_speed():
    st = speedtest.Speedtest()
    st.get_best_server()  # Find the best server

    download_speed = st.download() / 10 ** 6  # Convert to Mbps
    upload_speed = st.upload() / 10 ** 6  # Convert to Mbps

    return (f'[blue]Download speed: {download_speed:.2f} Mbps[/blue]\n'
            f'[magenta]Upload speed: {upload_speed:.2f} Mbps[/magenta]')


def animated_print(text):
    text += '\n'
    for char in text:
        print(char, end='')
        time.sleep(0.01)


if __name__ == "__main__":
    host_to_ping = "www.google.com"  # Change this to the host you want to ping
    ping_result = check_ping(host_to_ping)
    speed_result = check_speed()

    console = Console()
    print(ping_result)
    print(speed_result)