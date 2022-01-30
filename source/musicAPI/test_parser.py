import argparse
import pytest

class ErrorRaisingArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> ValueError:
        print(message)
        raise ValueError(message) 
    
def test_required_unknown(capsys):
    """ Try to perform sweep on something that isn't an option. """
    parser=argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--color",
        type=str,
        choices=["yellow", "blue"],
        required=True)
    args = ["--color", "NADA"]

    with pytest.raises(SystemExit):
        parser.parse_args(args)

    stderr = capsys.readouterr().err
    assert 'invalid choice' in stderr
