from django.apps import AppConfig
import arduino_controller.serialreader.serialreader as acsr


class DjangoArduinoControllerConfig(AppConfig):
    module_path = ".".join(__name__.split(".")[:-1])
    name = "django_arduino_controller"
    baseurl = "arduino_controller"

    serial_reader = None
    config = None

    def ready(self):
        self.serial_reader = acsr.SerialReader(
            start_in_background=True, config=self.config.getsubdict(["portdata"])
        )
