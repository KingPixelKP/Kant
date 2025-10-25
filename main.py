"""
Converts Json to linux ip routes
The first Connection in the arrays of host or routers is its local network
"""

from commands import *
from system import System




def main():
    system = System("config.json")
    invoker = Invoker()

    try:
        while True:
            cmd = input(">>>>").upper()
            if cmd == "WRITE KATHARA":
                system.write_kathara_config()
            elif cmd == "WRITE CONFIG":
                c = WriteConfig(system)
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD NET":
                c = AddNetwork(system, input("Network Name>>>>"), input("Network Address>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "RM NET":
                c = RemoveNetwork(system, input("Network Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD HOST":
                ...
            elif cmd == "ADD ROUTER":
                c = AddRouter(system, input("Router Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "RM ROUTER":
                c = RemoveRouter(system, input("Router Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD ROUTE":
                c = AddRoute(system, input("Router Name>>>>"),
                             input("Via Router>>>>"),
                             input("Connection Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "RM ROUTE":
                c = RemoveRoute(system, input("Router Name>>>>"),
                             input("Via Router>>>>"),
                             input("Connection Name>>>>"))
                invoker.add_command(c)
                invoker.execute_top()
            elif cmd == "ADD CON":
                ...
            elif cmd == "RM CON":
                ...
            elif cmd == "EXIT":
                break
            elif cmd == "SEXIT":
                c = WriteConfig(system)
                invoker.add_command(c)
                invoker.execute_top()
                break
            elif cmd == "HELP":
                ...
            elif cmd == "PRINT":
                ...
            elif cmd == "UNDO":
                invoker.undo_top()
            elif cmd == "REDO":
                invoker.redo_top()
            else:
                print("Unknown")
    except Exception as e:
        print(e)
        

if __name__ == "__main__":
    main()