import re

import inquirer

questions = [
    inquirer.Text("name", message="What's your name"),
    inquirer.Text("surname", message="What's your surname"),
    inquirer.Text(
        "phone",
        message="What's your phone number",
        validate=lambda _, x: re.match("\+?\d[\d ]+\d", x),
    ),
    # inquirer.Editor("long_text", message="Provide long text"),
    inquirer.List(
        "size",
        message="What size do you need?",
        choices=["Jumbo", "Large", "Standard", "Medium", "Small", "Micro"],
    ),
    inquirer.Checkbox(
        "interests",
        message="What are you interested in?",
        choices=["Computers", "Books", "Science", "Nature", "Fantasy", "History"],
    ),
    inquirer.Path(
        "log_file",
        message="Where logs should be located?",
        path_type=inquirer.Path.DIRECTORY,
    ),
]

answers = inquirer.prompt(questions)
print(f'您的输入是：{answers}')

questions_check = [
    inquirer.Confirm(
        "check",
        message="请确认您的输入是否正确?"
    ),
    ]

check_result = inquirer.prompt(questions_check)
print(check_result)
