import asyncio
import functools

import pytest

import httpx


def threadpool(func):
    """
    Our sync tests should run in separate thread to the uvicorn server.
    """

    @functools.wraps(func)
    async def wrapped(*args, **kwargs):
        nonlocal func

        loop = asyncio.get_event_loop()
        if kwargs:
            func = functools.partial(func, **kwargs)
        await loop.run_in_executor(None, func, *args)

    return pytest.mark.asyncio(wrapped)


@threadpool
def test_get(server):
    response = httpx.get("http://127.0.0.1:8000/")
    assert response.status_code == 200
    assert response.reason_phrase == "OK"
    assert response.text == "Hello, world!"


@threadpool
def test_post(server):
    response = httpx.post("http://127.0.0.1:8000/", data=b"Hello, world!")
    assert response.status_code == 200
    assert response.reason_phrase == "OK"


@threadpool
def test_post_byte_iterator(server):
    def data():
        yield b"Hello"
        yield b", "
        yield b"world!"

    response = httpx.post("http://127.0.0.1:8000/", data=data())
    assert response.status_code == 200
    assert response.reason_phrase == "OK"


@threadpool
def test_options(server):
    response = httpx.options("http://127.0.0.1:8000/")
    assert response.status_code == 200
    assert response.reason_phrase == "OK"


@threadpool
def test_head(server):
    response = httpx.head("http://127.0.0.1:8000/")
    assert response.status_code == 200
    assert response.reason_phrase == "OK"


@threadpool
def test_put(server):
    response = httpx.put("http://127.0.0.1:8000/", data=b"Hello, world!")
    assert response.status_code == 200
    assert response.reason_phrase == "OK"


@threadpool
def test_patch(server):
    response = httpx.patch("http://127.0.0.1:8000/", data=b"Hello, world!")
    assert response.status_code == 200
    assert response.reason_phrase == "OK"


@threadpool
def test_delete(server):
    response = httpx.delete("http://127.0.0.1:8000/")
    assert response.status_code == 200
    assert response.reason_phrase == "OK"


@threadpool
def test_get_invalid_url(server):
    with pytest.raises(httpx.InvalidURL):
        httpx.get("invalid://example.org")
