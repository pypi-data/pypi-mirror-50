class Colors:
    end = '\033[0m'
    pink = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    bold = '\033[1m'
    underline = '\033[4m'

    map = {
        'red': '91',
        'blue': '94',
        'yellow': '93',
        'green': '92',
        'pink': '95'
    }


def green(text):
    return f'{Colors.green}{text}{Colors.end}'


def red(text):
    return f'{Colors.red}{text}{Colors.end}'


def yellow(text):
    return f'{Colors.yellow}{text}{Colors.end}'


def blue(text):
    return f'{Colors.blue}{text}{Colors.end}'


def highlight(color, bg_color, text):
    return f'\033[{Colors.map[color]};{Colors.map[bg_color]}m{text}{Colors.end}'
