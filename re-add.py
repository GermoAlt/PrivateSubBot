import sys

import config
import helpers
import main as daddy
import updates


def main(new_users):
    reddit = helpers.initialize_reddit()

    user_list = helpers.load_data("user_list")

    for u in new_users:
        if u in user_list:
            helpers.write_log_trash(
                "Try to re-add existing user {}".format(helpers.date_string()), u
            )
            new_users.remove(u)

    if not new_users:
        helpers.write_log_trash(
            "All re-adds already on the memberlist {}".format(helpers.date_string()),
            new_users,
        )
        sys.exit(1)

    daddy.add_users(new_users, reddit)
    daddy.flair_users(
        new_users, reddit, config.flair_normal, number_adjustment=len(user_list)
    )

    insert_users_to_userlist(new_users)
    user_list = helpers.load_data("user_list")

    title, body = build_post(new_users, len(user_list) - len(new_users) + 1)
    daddy.make_post(title, body, reddit, distinguish=True, sticky=False)

    if config.update_sidebar:
        updates.update_sidebar(user_list)


def build_post(new_users, number):
    title = "User re-add"
    if config.title_date:
        title = helpers.date_string() + " - " + title
    if config.title_number:
        stats = helpers.load_data("stats")
        stats["re-add count"] += 1
        readd_count = stats["re-add count"]
        helpers.write_data("stats", stats)
        title += " #{}".format(readd_count)

    lines = []
    for user in new_users:
        lines.append(r"- \#{} /u/{}".format(number, user))
        number += 1

    if config.stats_section:
        cap = number - 1
        diff = len(new_users)
        lines.append(
            "\n# Info:\n\n- 0 users kicked\n- {} users added\n- Membercap: {} (+{})".format(
                diff, cap, diff
            )
        )

    body = "  \n".join(lines)

    return title, body


def insert_users_to_userlist(new_users):
    user_list = helpers.load_data("user_list")
    user_list.extend(new_users)
    helpers.write_data("user_list", user_list)


def process_input():
    if len(sys.argv) >= 2:
        users = sys.argv[1:]
    else:
        users = input("Enter users to re-add, separated by spaces: ").split()

    main(users)


if __name__ == "__main__":
    process_input()
