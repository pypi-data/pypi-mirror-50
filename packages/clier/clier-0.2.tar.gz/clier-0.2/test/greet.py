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

def test_fact():
    @clier.command
    def factorial(x: int):
        f = 1
        while x>1:
            f*=x
            x-=1
        return f
    #clier.start()

if __name__=="__main__":
    test_greet()
