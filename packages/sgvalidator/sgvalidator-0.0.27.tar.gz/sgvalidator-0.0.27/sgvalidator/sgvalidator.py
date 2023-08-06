from .validator_runner import ValidatorRunner
from .validator_io import ValidatorIO
from .color_printer import ColorPrinter

VERSION = "0.0.27"  # make sure this is consistent with setup.py


def validate(dataLocation, debug=False):
    ColorPrinter.printGreen("Validating data with DEBUG = {}".format(debug))
    validatorIo = ValidatorIO(VERSION)
    data = validatorIo.readDataFromLocation(dataLocation)
    classesToIgnore = validatorIo.getClassesToIgnore()
    ValidatorRunner(data, debug, classesToIgnore=classesToIgnore).run()
    validatorIo.optionallyWriteSuccessFile(debug)
