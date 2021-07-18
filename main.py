import os
from colorama import Fore, init
from selectmenu import SelectMenu

from modules.phash import load_phashes, find_similar_imgs
from modules.utils import load_classes, get_cropped_card
from modules.border_detection import detect_contours
from modules.border_calculations import get_border_dimensions


def print_logo():
    logo = """
   _____                  _  _                      _____               _              
  |  __ \                | |(_)                    /  __ \             | |             
  | |  \/ _ __  __ _   __| | _  _ __    __ _       | /  \/  ___  _ __  | |_  ___  _ __ 
  | | __ | '__|/ _` | / _` || || '_ \  / _` |      | |     / _ \| '_ \ | __|/ _ \| '__|
  | |_\ \| |  | (_| || (_| || || | | || (_| |      | \__/\|  __/| | | || |_|  __/| |   
   \____/|_|   \__,_| \__,_||_||_| |_| \__, |       \____/ \___||_| |_| \__|\___||_|   
                                        __/ |                                     
                                       |___/                    
                                                                Made with <3 by Antonji
    """

    os.system("cls")
    init(autoreset=True)
    print(Fore.LIGHTRED_EX + logo)
    print()


def get_mode_choice(choices):
    menu = SelectMenu()
    menu.add_choices(choices)
    mode = menu.select("  Which mode would you like to use?")

    print(Fore.LIGHTMAGENTA_EX + f"  Selected mode: {mode.split('. ')[1]}")
    print()

    return mode


def get_selected_img():
    menu = SelectMenu()
    choices = os.listdir("workspace")
    menu.add_choices(choices)
    img_name = menu.select("  Which card would you like to recognise?")

    print(Fore.LIGHTMAGENTA_EX + f"  Selected image: {img_name}")
    print()

    return img_name


def get_manual_border_dimension():
    top_outside_border_y = int(input("  Type y coordinate (height) of top outside border: "))
    top_inside_border_y = int(input("  Type y coordinate (height) of top inside border: "))
    right_outside_border_x = int(input("  Type x coordinate (width) of right outside border: "))
    right_inside_border_x = int(input("  Type x coordinate (width) of right inside border: "))
    bottom_outside_border_y = int(input("  Type y coordinate (height) of bottom outside border: "))
    bottom_inside_border_y = int(input("  Type y coordinate (height) of bottom inside border: "))
    left_outside_border_x = int(input("  Type x coordinate (width) of left outside border: "))
    left_inside_border_x = int(input("  Type x coordinate (width) of left inside border: "))

    top_border = abs(top_outside_border_y - top_inside_border_y)
    bottom_border = abs(right_outside_border_x - right_inside_border_x)
    right_border = abs(bottom_outside_border_y - bottom_inside_border_y)
    left_border = abs(left_outside_border_x - left_inside_border_x)

    return top_border, right_border, bottom_border, left_border


def print_similar_images(img_path):
    similar_imgs = find_similar_imgs(get_cropped_card(img_path), phashes)

    print(Fore.GREEN + f"  1. {classes[list(similar_imgs[0].keys())[0]]}")
    print(Fore.YELLOW + f"  2. {classes[list(similar_imgs[1].keys())[0]]}")
    print(Fore.LIGHTRED_EX + f"  3. {classes[list(similar_imgs[2].keys())[0]]}")
    print()


def print_border_dimensions(top_border, right_border, bottom_border, left_border):
    print(f"  Top border: {top_border}px")
    print(f"  Bottom border: {bottom_border}px")
    print(f"  Top + Bot border: {top_border + bottom_border}px")
    print(Fore.GREEN + f"  Vertical deviation: {round(abs(top_border - bottom_border) / (top_border + bottom_border) * 100, 4)}%")
    print()
    print(f"  Right border: {right_border}px")
    print(f"  Left border: {left_border}px")
    print(f"  Right + Left border: {right_border + left_border}px")
    print(Fore.GREEN + f"  Horizontal deviation: {round(abs(right_border - left_border) / (right_border + left_border) * 100, 4)}%")


print_logo()

print(Fore.LIGHTBLUE_EX + "  Loading pHashes and classes...", end="")
phashes = load_phashes("database/phashes.txt")
classes = load_classes("database/classes.txt")

while True:
    print_logo()

    choices = ["1. Card scanner", "2. Auto card centering rating", "3. Manual card centering rating"]
    mode = get_mode_choice(choices)
    if mode == choices[0]:
        selected_img_path = "workspace/" + get_selected_img()
        print_similar_images(selected_img_path)
    elif mode == choices[1]:
        selected_img_path = "workspace/" + get_selected_img()

        print(Fore.LIGHTBLUE_EX + "  Detecting contours...", end="\r")
        detect_contours(selected_img_path)

        print(Fore.LIGHTBLUE_EX + "  Calculating border dimensions...", end="\x1b[1K\r")
        top_border, right_border, bottom_border, left_border = get_border_dimensions(selected_img_path)

        print_border_dimensions(top_border, right_border, bottom_border, left_border)
    elif mode == choices[2]:
        top_border, right_border, bottom_border, left_border = get_manual_border_dimension()

        print_border_dimensions(top_border, right_border, bottom_border, left_border)

    print()
    input("  Press any key to restart")

    os.system("cls")
