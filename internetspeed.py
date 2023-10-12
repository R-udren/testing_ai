import speedtest
from ping3 import ping
from rich.console import Console
from rich import print


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


def main():
    host_to_ping = "google.com"
    console = Console()

    with console.status("[bold green]Checking internet speed...\n") as status:
        speed_result = check_speed()
        ping_result = check_ping(host_to_ping)
        status.stop()
        print(ping_result)
        print(speed_result)


if __name__ == "__main__":
    main()