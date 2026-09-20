from context import RequestContext


def test_request_context_creates_request_id() -> None:
    context = RequestContext.create()

    assert context.request_id
    assert len(context.request_id) == 36


def test_request_context_is_immutable() -> None:
    context = RequestContext.create()

    try:
        context.request_id = "new-id"
        assert False
    except AttributeError:
        pass