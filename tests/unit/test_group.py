from styledconsole.core.group import CapturedFrame, FrameGroupContext


class DummyRenderer:
    def render_frame_to_string(self, content, context=None):
        return f"RENDERED:{content}"


class DummyConsole:
    def __init__(self):
        self._renderer = DummyRenderer()
        self._printed = []

    def _print_ansi_output(self, output: str, align: str = "left"):
        self._printed.append((output, align))


def test_group_handles_extra_kwargs():
    dummy = DummyConsole()
    group = FrameGroupContext(console=dummy)

    # Add captured frame with an extra, unexpected kwarg 'foo'
    group._captured_frames.append(
        CapturedFrame(content="X", kwargs={"border": "rounded", "foo": "bar"})
    )

    # Should not raise and should print rendered output
    group._render_group()
    assert dummy._printed, "Expected output to be printed by DummyConsole"
    out, _ = dummy._printed[0]
    assert "RENDERED" in out
