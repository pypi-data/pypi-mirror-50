from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, receiver):
        self._receiver = receiver
    
    @abstractmethod
    def execute(self):
        pass

class ThresholdCommand(Command):
    def execute(self, result):
        return self._receiver.threshold(result)

class DenoiseCommand(Command):
    def execute(self, result):
        return self._receiver.denoise(result)

class ContourCommand(Command):
    def execute(self, result):
        return self._receiver.contour(result)

class CropCommand(Command):
    def execute(self, result):
        return self._receiver.crop(result)

class LabelCommand(Command):
    def execute(self, result):
        return self._receiver.label(result)

class IsolateCommand(Command):
    def execute(self, result):
        return self._receiver.isolate(result)

class WriteCommand(Command):
    def execute(self, result):
        return self._receiver.write(result)