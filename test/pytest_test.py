import pytest
import hello_world
@pytest.mark.integ
@pytest.mark.parametrize("test_input, expected", [("3+5", 8), ("2+4",6), ("6*9", 54)])
def test_eval(test_input, expected):
	assert eval(test_input) == expected

def test_print_hw():
	assert hello_world.hello() == "Hello world!"