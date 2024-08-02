# This is just a mock to run the code on any computer to test the logic

USE_MOCK = True

if USE_MOCK:
    from unittest.mock import MagicMock

    smbus = MagicMock()

else:
    import smbus2 as smbus
