import PyInquirer


def update_api_key():
    info = get_information()

    f = open("key.txt", "w+")
    f.write(info["key"])
    f.close()

    return "Your key has been added"


def get_information():
    questions = [
        {
            'type': 'input',
            'name': 'key',
            'message': 'What\'s the value of your API key',
        },
    ]
    answers = PyInquirer.prompt(questions)

    return answers
