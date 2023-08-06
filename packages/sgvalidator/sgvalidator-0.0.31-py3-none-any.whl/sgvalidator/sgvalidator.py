from .validator_runner import ValidatorRunner
from .validator_io import ValidatorIO
from .color_printer import ColorPrinter


def validate(dataLocation, debug=False):
    ColorPrinter.printGreen("Validating data with DEBUG = {}".format(debug))
    validatorIo = ValidatorIO()
    data = validatorIo.readDataFromLocation(dataLocation)
    classesToIgnore = validatorIo.getClassesToIgnore()
    ValidatorRunner(data, debug, classesToIgnore=classesToIgnore).run()
    validatorIo.optionallyWriteSuccessFile(debug)
