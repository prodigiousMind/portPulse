#!/usr/bin/env python3

# Author: prodigiousMind
# youtube: https://www.youtube.com/channel/UCyoQWc93GZRlYl1LL7J5MrQ
# github: https://github.com/prodigiousMind/

# portPulse, or ppulse written in python3,
# a small tool that can be used for port scanning through HTTP requests.
# It sends GET requests to the target IP or hostname
# on the specified range of ports (default = all). 

import aiohttp
import asyncio
import argparse
import sys
import termcolor
from colorama import Fore, init

# Initialize (to reset the color back to what was set)
init(autoreset=True)

# Function to print help message
def print_help():
    print("\nUsage: python {} -t [IP/Hostname] -s PortStart -e PortEnd".format(sys.argv[0]))
    print(termcolor.colored(text="[+] Default PortStart=1 & PortEnd=65535",color="red"))
    print(termcolor.colored(text="[+] IP: Targer IP or Hostname\n",color="blue"))

# Asynchronous function to send a GET request to the given URL
async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return response.url
    except aiohttp.ClientResponseError as e:
        print(termcolor.colored(text="[+] "+url.split(":")[2], color="green"),end="")
        print(" ->",termcolor.colored(text=(str(e.message).replace("\n","").replace("Expected HTTP/:","").replace("^","").strip()), color="red"))
        return None
    except aiohttp.ClientConnectorError as e:
        return None
    except asyncio.TimeoutError:
        print(termcolor.colored(text="[+] "+url.split(":")[2], color="green"))
        return None
    except ConnectionResetError:
        print(termcolor.colored(text="[+] "+url.split(":")[2], color="green"))
        return None
    except Exception as e:
        print(termcolor.colored(text="[+] "+url.split(":")[2], color="green"))
        return None

# Main function to create tasks and gather responses
async def main(n, url):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(n-2000, n):
            if i < args.port_end:
                tasks.append(fetch(session, str(url)+":"+str(i)))
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for i in responses:
            if i:
                print(termcolor.colored(text="[+] "+str(i), color="blue"))

# Entry point
if __name__ == '__main__':

    try:
        parser = argparse.ArgumentParser(description='Port scanning through HTTP requests.')
        parser.add_argument('-t', '--target-ip', type=str, required=False, help='Target IP or hostname')
        parser.add_argument('-s', '--port-start', type=int, default=1, help='Start port (default: 1)')
        parser.add_argument('-e', '--port-end', type=int, default=65536, help='End port (default: 65535)')
        parser.add_argument('help', nargs='*', help="print usage")
        args = parser.parse_args()
      
        # generate help if -t/--target-ip flag not passed
        if not args.target_ip:
            print_help()
        else:
          
            # 2000 can be changed to another value
            for n in range(args.port_start, args.port_end, 2000):
                n = n+2000
                url = 'http://'+args.target_ip
                asyncio.run(main(n, url))
    except: print_help()
