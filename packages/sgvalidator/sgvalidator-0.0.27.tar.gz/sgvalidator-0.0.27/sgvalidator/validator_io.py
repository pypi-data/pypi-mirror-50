import os
import csv
import sys
import json
import termcolor
from .color_printer import ColorPrinter
from glob import glob


class ValidatorIO:
    SUCCESS_FILEPATH = './SUCCESS'

    def __init__(self, version):
        self.version = version

    def optionallyWriteSuccessFile(self, debug):
        if not debug:
            ColorPrinter.printGreen("Nice job! Creating SUCCESS file. Please commit this with your scraper.")
            ValidatorIO.touch(ValidatorIO.SUCCESS_FILEPATH)
            with open(ValidatorIO.SUCCESS_FILEPATH, 'a') as f:
                f.write("VERSION: {}".format(self.version))
                f.write("\n")
                f.write("COMMAND: {}".format(self.getCommandThatRanMe()))

    @staticmethod
    def readDataFromLocation(dataLocation):
        data = []
        if dataLocation.endswith(".csv"):
            with open(dataLocation) as csv_file:
                reader = csv.DictReader(csv_file, skipinitialspace=True)
                for row in reader:
                    data.append(row)
        else:
            for f_name in glob(os.path.join(dataLocation, 'datasets/default', '*.json')):
                with open(f_name) as json_file:
                    data.append(json.load(json_file))

        if len(data) == 0:
            ColorPrinter.printRed("Data location doesn't exist or dataset is empty: {}".format(dataLocation))
            exit(0)

        return data

    @staticmethod
    def touch(path):
        with open(path, 'a'):
            os.utime(path, None)

    @staticmethod
    def getCommandThatRanMe():
        return " ".join(sys.argv[:])

    @staticmethod
    def getClassesToIgnore():
        IGNORE_FLAG = "--ignore"
        cmd = ValidatorIO.getCommandThatRanMe()
        if IGNORE_FLAG in cmd:
            idx = cmd.index("--ignore")
            cmdsString = cmd[idx + len(IGNORE_FLAG):].strip()
            return list(map(lambda x: x.strip(), cmdsString.split(" ")))
        return []
