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
    def printBlueBanner(message):
        ColorPrinter._printColor(message, "blue", attrs=['reverse'])

    @staticmethod
    def printRedBanner(message):
        ColorPrinter._printColor(message, "red", attrs=['reverse'])

    @staticmethod
    def printCyan(message):
        ColorPrinter._printColor(message, "cyan")

    @staticmethod
    def _printColor(message, color, attrs=None):
        print(termcolor.colored(message, color, attrs=attrs))
