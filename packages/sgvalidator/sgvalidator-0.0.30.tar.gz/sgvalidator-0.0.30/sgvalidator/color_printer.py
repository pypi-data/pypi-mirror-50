import termcolor


class ColorPrinter:
    @staticmethod
    def printGreen(message):
        ColorPrinter._printColor(message, "green")

    @staticmethod
    def printYellow(message):
        ColorPrinter._printColor(message, "yellow")

    @staticmethod
    def printRed(message):
        ColorPrinter._printColor(message, "red")

    @staticmethod
    def printBlue(message):
        ColorPrinter._printColor(message, "blue")

    @staticmethod
    def printCyan(message):
        ColorPrinter._printColor(message, "cyan")

    @staticmethod
    def _printColor(message, color):
        print(termcolor.colored(message, color))
