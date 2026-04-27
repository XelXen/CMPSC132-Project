# LaptopScrappy: A command-line tool for scraping and viewing laptop listings from a website.
import backend


# Help mode: Displays available commands and their usage
def help_mode():
    print("\n--- COMMANDS ---")
    print("[-] view <query: optional> <sort: optional> - List laptops with search query and sorting")
    print("    | EXAMPLE USAGE:")
    print("    | >> view - View laptops with default settings")
    print("    | >> view asus rog - View laptops with 'asus rog' in the title")
    print("    | >> view asus rog SORT_PRICE_LOW_TO_HIGH - View laptops with 'asus rog' sorted by price")
    print("    | >> view SORT_BEST_SELLERS - View laptops sorted by best sellers")
    print("[-] sort - View the sorting types available")
    print("[-] help - Show this help message")
    print("[-] exit | quit - Exit the program")
    print("----------------\n")


# View mode: Displays laptops with optional sorting, searching, and pagination
def view_mode(command: str):
    cmds = command.split(" ")
    page = 1

    if len(cmds) == 0:
        # No query or sort provided, default to first page with no sorting
        sortmode = None
        query = None
    if len(cmds) == 1:
        if cmds[0].upper() in backend.sorttypes:
            # Only sort provided, no query
            sortmode = cmds[0].upper()
            query = None
        else:
            # Only query provided, no sort
            sortmode = None
            query = cmds[0]
    else:
        if cmds[-1].upper() not in backend.sorttypes:
            # Last argument is not a valid sort type, treat all as query
            sortmode = None
            query = "+".join(cmds)
        else:
            # Last argument is a valid sort type, treat it as sort and the rest as query
            sortmode = cmds[-1].upper()
            query = "+".join(cmds[:-1])

    running = True
    while running:
        # Fetch and display laptops based on the current page, query, and sort mode
        print(f"\n--- PAGE {page} ---")
        for laptop in backend.parse_index(
            backend.fetch(
                backend.base,
                page_keyword=str(page),
                search_keyword=query,
                sort_keyword=sortmode,
            )
        ):
            print(laptop)
        ui = (
            input("--- OPTIONS ---\n\n[|] (n)ext, (p)revious, (e)xit: ").strip().lower()
        )

        # Process user input for pagination and exiting the view mode
        if ui == "n":
            page += 1
        elif ui == "p":
            if page > 1:
                page -= 1
            else:
                print("Already on the first page.")
        elif ui == "e":
            print()
            running = False
        else:
            print("Unknown option. Please enter 'n', 'p', or 'e'.")


# Sort mode: Displays available sorting types
def sort_mode():
    print("\n--- SORTING TYPES ---")
    for sort in backend.sorttypes:
        print(f"[-] {sort}")
    print("---------------------\n")


# Shell mode: Main loop for user interaction, processes commands and calls respective modes
def shell():
    running = True
    while running:
        command = input("[>>] ").strip().lower()

        if command == "exit" or command == "quit":
            running = False
        elif command == "help":
            help_mode()
        elif command.startswith("view"):
            view_mode(command[4:].strip())
        elif command.startswith("sort"):
            sort_mode()
        else:
            print("Unknown command. Type 'help' for a list of commands.")


if __name__ == "__main__":
    print("Welcome to the LaptopScrappy!")
    help_mode()
    shell()
