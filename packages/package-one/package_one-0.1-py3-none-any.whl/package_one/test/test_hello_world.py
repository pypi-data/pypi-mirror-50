from unittest import TestCase

from package_one.hello_world import HELLO_WORLD_MESSAGE
from package_one.hello_world import get_message


class TestHelloWorld(TestCase):
    def test_get_message(self):
        assert HELLO_WORLD_MESSAGE == get_message()
