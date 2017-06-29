'''
Some constant variables consisting of ANSI escape codes used to
print "stylized" fonts in command line.
Works on Unices, Such as Linux, macOS, etc.
http://ascii-table.com/ansi-escape-sequences.php
'''


class fonts:

    FG_WHITE = "\033[37m"
    FG_CYAN = "\033[36m"
    FG_MAGENTA = "\033[35m"
    BG_RED ="\033[41m"
    BG_YELLOW = "\033[43m"
    BG_CYAN = "\033[46m"
    BG_GREEN = "\033[42m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ANSI_RESET  = "\033[0m"

    def disable(self):
            self.FG_WHITE = ""
            self.FG_CYAN = ""
            self.FG_MAGENTA = ""
            self.BG_RED =""
            self.BG_YELLOW = ""
            self.BG_CYAN = ""
            self.BG_GREEN = ""
            self.BOLD = ""
            self.UNDERLINE = ""
            self.ANSI_RESET  = ""
