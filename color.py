class Color:
    end = "\x1b[0m"
    class f:
        # standard colors
        default =  "\x1b[38;5;0m"
        black = "\x1b[38;5;0m"
        red = "\x1b[38;5;1m"
        green = "\x1b[38;5;2m"
        yellow = "\x1b[38;5;3m"
        blue = "\x1b[38;5;4m"
        magenta = "\x1b[38;5;5m"
        cyan = "\x1b[38;5;6m"
        light_gray = "\x1b[38;5;7m"
        # high intensity colors
        dark_gray = "\x1b[38;5;8m"
        light_red = "\x1b[38;5;9m"
        light_green = "\x1b[38;5;10m"
        light_yellow = "\x1b[38;5;11m"
        light_blue = "\x1b[38;5;12m"
        light_magenta = "\x1b[38;5;13m"
        light_cyan = "\x1b[38;5;14m"
        white = "\x1b[38;5;15m"
    class b:
        # standard colors
        default =  "\x1b[48;5;0m"
        black = "\x1b[48;5;0m"
        red = "\x1b[48;5;1m"
        green = "\x1b[48;5;2m"
        yellow = "\x1b[48;5;3m"
        blue = "\x1b[48;5;4m"
        magenta = "\x1b[48;5;5m"
        cyan = "\x1b[48;5;6m"
        light_gray = "\x1b[48;5;7m"
        # high intensity colors
        dark_gray = "\x1b[48;5;8m"
        light_red = "\x1b[48;5;9m"
        light_green = "\x1b[48;5;10m"
        light_yellow = "\x1b[48;5;11m"
        light_blue = "\x1b[48;5;12m"
        light_magenta = "\x1b[48;5;13m"
        light_cyan = "\x1b[48;5;14m"
        white = "\x1b[48;5;15m"

bold, dim, italic  = 1, 2, 3

def color(foreground=None, background=None, style=None): # 0-255, 0-255, style: bold, dim, or italic
    if foreground is None and background is None and style is None:
        return default()
    elif foreground is not None and background is None and style is None:
        return fg_color(foreground)
    elif foreground is not None and background is not None and style is None:
        return fg_color(foreground) + bg_color(background)
    elif foreground is not None and background is None and style is not None:
        return fg_color(foreground) + format_text(style)
    else:
        return fg_color(foreground) + bg_color(background) + format_text(style)

def default():
    return "\x1b[0m"

def fg_color(color):
    return '\x1b[38;5;' + str(color) + 'm'

def bg_color(color):
    return '\x1b[48;5;' + str(color) + 'm'

def format_text(style):
    return '\x1b[' + str(style) + 'm'