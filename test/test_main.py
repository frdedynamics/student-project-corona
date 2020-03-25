from unittest import TestCase
from .context import src
import app


class TestMain(TestCase):
    def test_main(self):
        try:
            self.model_sir = src.models.SIR()
            app.main()
        except ValueError as e:
            self.fail(msg=e)
