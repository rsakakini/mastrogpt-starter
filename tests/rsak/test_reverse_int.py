import os, requests as req
def test_reverse():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/rsak/reverse"
    res = req.get(url).json()
    assert res.get("output") == res.get("output")[::-1]
