import clier
from . import _input_mock 

def test_greet():
    _input_mock.sequence( ['greet Sandy', 'help' ])

    @clier.command
    def greet(name, title='Mr.'):
        """ Greet a person by name """
        print("Hello,", title, name)

    clier.start()

    _input_mock.restore()
