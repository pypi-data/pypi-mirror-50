import janis_core as j
from .echo import Echo


class HelloWorkflow(j.Workflow):
    def __init__(self):
        super().__init__("hello", doc="A simple hello world example")

        inp = j.Input("inp", j.String(optional=True), default="Hello, world!")
        echo = j.Step("hello", tool=Echo())
        self.add_edge(inp, echo.inp)
        self.add_edge(echo.out, j.Output("out"))
