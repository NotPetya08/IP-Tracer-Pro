import requests
import json
import webbrowser
import sys
import os
from colorama import Fore, Style, init

# Colors initialize for Linux/Windows
init(autoreset=True)

def clear_screen():
    # Kali/Linux ke liye 'clear', Windows ke liye 'cls'
    os.system('clear' if os.name == 'posix' else 'cls')

def save_log(data):
    """User se permission le kar save karne ka function"""
    choice = input(f"\n{Fore.YELLOW}[?] Save this result to 'logs.txt'? (y/n): ").lower()
    if choice in ['y', 'yes']:
        with open("logs.txt", "a") as f:
            f.write(f"IP: {data['query']} | Location: {data['city']}, {data['country']}\n")
            f.write(json.dumps(data, indent=4) + "\n" + "="*50 + "\n")
        print(f"{Fore.CYAN}[!] Data saved successfully.")
    else:
        print(f"{Fore.WHITE}[*] Log ignored.")

def exit_menu():
    """Tool se exit karne ka professional tareeqa"""
    print(f"\n{Fore.RED}[!] Press Ctrl+X then Enter to Exit or any other key to scan again...")
    choice = input(f"{Fore.WHITE}>>> ").lower()
    # Kali tools mein Ctrl+X aksar exit signal hota hai, yahan hum input se handle kar rahe hain
    if choice == '\x18' or choice == 'x': 
        print(f"{Fore.YELLOW}[*] Shutting down IP-Tracer... Goodbye!")
        sys.exit()

def start_tracer():
    while True:
        clear_screen()
        banner = f"""
    {Fore.RED}██╗██████╗     ████████╗██████╗  █████╗  ██████╗███████╗██████╗ 
    {Fore.RED}██║██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
    {Fore.WHITE}██║██████╔╝       ██║   ██████╔╝███████║██║     █████╗  ██████╔╝
    {Fore.WHITE}██║██╔═══╝        ██║   ██╔══██╗██╔══██║██║     ██╔══╝  ██╔══██╗
    {Fore.WHITE}██║██║            ██║   ██║  ██║██║  ██║╚██████╗███████╗██║  ██║
    {Fore.CYAN}╚═╝╚═╝            ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝
    {Fore.YELLOW}             >>> Kali Linux Edition v4.0 <<<
        """
        print(banner)
        
        target = input(f"{Fore.CYAN}[?] Enter Target IP: {Style.RESET_ALL}").strip()
        print(f"{Fore.GREEN}[*] Accessing Satellite Data...")

        try:
            url = f"http://ip-api.com/json/{target}?fields=66846719"
            response = requests.get(url, timeout=10)
            data = response.json()

            if data['status'] == 'success':
                print(f"\n{Fore.YELLOW}[+] TARGET INFORMATION")
                print(f"{Fore.WHITE}--------------------------------------")
                print(f"{Fore.GREEN}📍 Country:    {Fore.WHITE}{data['country']} ({data['countryCode']})")
                print(f"{Fore.GREEN}🏙️ City:       {Fore.WHITE}{data['city']}")
                print(f"{Fore.GREEN}🏢 ISP:        {Fore.WHITE}{data['isp']}")
                print(f"{Fore.GREEN}📡 Proxy/VPN:  {Fore.RED if data['proxy'] else Fore.BLUE}{data['proxy']}")
                print(f"{Fore.WHITE}--------------------------------------")
                
                save_log(data)
                
                view_map = input(f"\n{Fore.MAGENTA}[?] Open Google Maps? (y/n): ").lower()
                if view_map in ['y', 'yes']:
                    webbrowser.open(f"https://www.google.com/maps?q={data['lat']},{data['lon']}")

            else:
                print(f"{Fore.RED}[-] Error: {data.get('message', 'Invalid IP')}")

        except Exception as e:
            print(f"\n{Fore.RED}[!] CONNECTION ERROR: Please check your internet.")
        
        # Har haal mein exit menu dikhayega (Error ho ya Success)
        exit_menu()

if __name__ == "__main__":
    try:
        start_tracer()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Tool interrupted by user. Exiting...")
        sys.exit()