def get_color(color):
    colors = {
        "Green": "\x1b[32m",
        "Yellow": "\x1b[33m",
        "DarkGray": "\x1b[90m",
        "Default": "\x1b[39m"
    }
    return colors[color]
