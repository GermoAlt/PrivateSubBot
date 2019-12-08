import json
import os

import config
import helpers


def main():
    titles_path = os.path.join(
        helpers.folder_path(), config.titles_path[0], config.titles_path[1]
    )
    with open(titles_path, "r") as f:
        titles = json.load(f)

    wanna_clear = input("Would you like to clear all existing titles? [y/n] ")
    try:
        if wanna_clear.lower()[0] == "y":
            if (
                input(
                    "Are you sure? This will destroy all previous titles. [y/n] "
                ).lower()[0]
                == "y"
            ):
                titles = []
                print("All titles have been cleared.")
    except IndexError:
        # no input
        pass

    new_title = "überSecretString"

    while new_title != "":
        if new_title != "überSecretString":
            titles.append(new_title)
        new_title = input("Enter a title (leave blank to finish): ")

    with open(titles_path, "w") as f:
        json.dump(titles, f)

    print("Titles successfully saved.\n")


if __name__ == "__main__":
    main()
