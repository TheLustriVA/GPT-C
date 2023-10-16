from rich.console import Console
from rich.table import Table
import math

def sdxl_ratio_simple() -> None:
    """Display SDXL ratio catalogue as a table with headings height, width, 
    ratio, and name:
        1024 x 1024 (1:1 Square)
        1152 x 896 (9:7)
        896 x 1152 (7:9)
        1216 x 832 (19:13)
        832 x 1216 (13:19)
        1344 x 768 (7:4 Horizontal)
        768 x 1344 (4:7 Vertical)
        1536 x 640 (12:5 Horizontal)
        640 x 1536 (5:12 Vertical, the closest to the iPhone resolution)
    """
    console = Console()
    table = Table(title="SDXL Ratio Catalogue")
    table.add_column("Height", justify="right", style="cyan")
    table.add_column("Width", justify="right", style="cyan")
    table.add_column("Ratio", justify="right", style="magenta")
    table.add_column("Name", justify="left", style="green")
    table.add_row("1024", "1024", "1:1", "Square")
    table.add_row("1152", "896", "9:7", "")
    table.add_row("896", "1152", "7:9", "")
    table.add_row("1216", "832", "19:13", "")
    table.add_row("832", "1216", "13:19", "")
    table.add_row("1344", "768", "7:4", "Horizontal")
    table.add_row("768", "1344", "4:7", "Vertical")
    table.add_row("1536", "640", "12:5", "Horizontal")
    table.add_row("640", "1536", "5:12", "Vertical, the closest to the iPhone resolution")
    console.print(table)
    return None
    
    
from rich.console import Console
from rich.table import Table

def sdxl_ratio_complete() -> None:
    """resolutions = [
        # SDXL Base resolution
        {"width": 1024, "height": 1024},
        # SDXL Resolutions, widescreen
        {"width": 2048, "height": 512},
        {"width": 1984, "height": 512},
        {"width": 1920, "height": 512},
        {"width": 1856, "height": 512},
        {"width": 1792, "height": 576},
        {"width": 1728, "height": 576},
        {"width": 1664, "height": 576},
        {"width": 1600, "height": 640},
        {"width": 1536, "height": 640},
        {"width": 1472, "height": 704},
        {"width": 1408, "height": 704},
        {"width": 1344, "height": 704},
        {"width": 1344, "height": 768},
        {"width": 1280, "height": 768},
        {"width": 1216, "height": 832},
        {"width": 1152, "height": 832},
        {"width": 1152, "height": 896},
        {"width": 1088, "height": 896},
        {"width": 1088, "height": 960},
        {"width": 1024, "height": 960},
        # SDXL Resolutions, portrait
        {"width": 960, "height": 1024},
        {"width": 960, "height": 1088},
        {"width": 896, "height": 1088},
        {"width": 896, "height": 1152},
        {"width": 832, "height": 1152},
        {"width": 832, "height": 1216},
        {"width": 768, "height": 1280},
        {"width": 768, "height": 1344},
        {"width": 704, "height": 1408},
        {"width": 704, "height": 1472},
        {"width": 640, "height": 1536},
        {"width": 640, "height": 1600},
        {"width": 576, "height": 1664},
        {"width": 576, "height": 1728},
        {"width": 576, "height": 1792},
        {"width": 512, "height": 1856},
        {"width": 512, "height": 1920},
        {"width": 512, "height": 1984},
        {"width": 512, "height": 2048},
    ]    """

    resolutions = [
        {"width": 1024, "height": 1024}, # SDXL Base resolution
        {"width": 2048, "height": 512},  # SDXL Resolutions, widescreen
        {"width": 1984, "height": 512},
        {"width": 1920, "height": 512},
        {"width": 1856, "height": 512},
        {"width": 1792, "height": 576},
        {"width": 1728, "height": 576},
        {"width": 1664, "height": 576},
        {"width": 1600, "height": 640},
        {"width": 1536, "height": 640},
        {"width": 1472, "height": 704},
        {"width": 1408, "height": 704},
        {"width": 1344, "height": 704},
        {"width": 1344, "height": 768},
        {"width": 1280, "height": 768},
        {"width": 1216, "height": 832},
        {"width": 1152, "height": 832},
        {"width": 1152, "height": 896},
        {"width": 1088, "height": 896},
        {"width": 1088, "height": 960},
        {"width": 1024, "height": 960},
        {"width": 960, "height": 1024},  # SDXL Resolutions, portrait
        {"width": 960, "height": 1088},
        {"width": 896, "height": 1088},
        {"width": 896, "height": 1152},
        {"width": 832, "height": 1152},
        {"width": 832, "height": 1216},
        {"width": 768, "height": 1280},
        {"width": 768, "height": 1344},
        {"width": 704, "height": 1408},
        {"width": 704, "height": 1472},
        {"width": 640, "height": 1536},
        {"width": 640, "height": 1600},
        {"width": 576, "height": 1664},
        {"width": 576, "height": 1728},
        {"width": 576, "height": 1792},
        {"width": 512, "height": 1856},
        {"width": 512, "height": 1920},
        {"width": 512, "height": 1984},
        {"width": 512, "height": 2048}
    ]

    console = Console()
    table = Table(title="SDXL Ratio Catalogue")
    table.add_column("Width", justify="right", style="cyan")
    table.add_column("Height", justify="right", style="cyan")
    table.add_column("Ratio", justify="right", style="magenta")
    for resolution in resolutions:
        width = str(resolution["width"])
        height = str(resolution["height"])
        ratio = f"{resolution['width'] // math.gcd(resolution['width'], resolution['height'])}:" \
            f"{resolution['height'] // math.gcd(resolution['width'], resolution['height'])}"
        table.add_row(width, height, ratio)
    console.print(table)
    return None


def main_menu() -> None:
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option")
    table.add_column("Description")
    table.add_row("1", "View sdxl_ratio_simple output")
    table.add_row("2", "View sdxl_ratio_complete output")
    table.add_row("3", "Quit")
    console.print(table)

    while True:
        choice = input("Enter an option: ")
        if choice == "1":
            sdxl_ratio_simple()
            console.print(table)
        elif choice == "2":
            sdxl_ratio_complete()
            console.print(table)
        elif choice == "3":
            break
        else:
            console.print("Invalid option, please try again.", style="bold red")
            continue

if __name__ == "__main__":
    main_menu()
