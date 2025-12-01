from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_echo_displays_message_as_text():
    msg = "<script>alert(1)</script>"
    resp = client.get("/echo", params={"msg": msg})
    assert resp.status_code == 200
    # Проверяем, что содержимое видно, но уже экранированное (как текст, а не как тег)
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in resp.text
