from pathlib import Path
from inject_config import inject_config
from json import loads


def test_direct():
    @inject_config({"hy": "bye", "good": 2})
    def foo(bar):
        return bar

    assert foo() == {"hy": "bye", "good": 2}


def test_direct_second_arg():
    @inject_config({"hy": "bye", "good": 2}, first=False)
    def foo(bar, bars):
        return bar

    assert foo("bar") == "bar"


def test_direct_kwarg():
    @inject_config({"hy": "bye", "good": 2}, use_kwarg="test")
    def foo(bar, test):
        return bar

    assert foo("bar") == "bar"


def test_direct_kwarg_wrong_key():
    @inject_config({"hy": "bye", "good": 2}, use_kwarg="test")
    def foo(bar, bars):
        return bar

    try:
        foo("bar")
        assert False
    except Exception:
        assert True


def test_yaml():
    p = Path(__file__).parent / "example_config.yml"

    @inject_config.from_yaml(p)
    def foo(bar):
        return bar

    assert foo() == {"test": 2, "some_key": 3}


def test_json():
    p = Path(__file__).parent / "example_config.json"

    @inject_config.from_json(p)
    def foo(bar):
        return bar

    assert foo() == {"test": 2, "some_key": 3}


def test_custom_loader():
    class JsonLoader:
        def __init__(self):
            self.file = Path(__file__).parent / "example_config.json"

        def __call__(self, **kwargs):
            with open(self.file, "r") as f:
                config = loads(f.read())
            for k, v in kwargs.items():
                config[k] = v
            return config

    loader = JsonLoader()

    @inject_config.from_loader(loader, loader_kwargs=dict(foo="bar"))
    def foo(bar):
        return bar

    assert foo() == {"test": 2, "some_key": 3, "foo": "bar"}
