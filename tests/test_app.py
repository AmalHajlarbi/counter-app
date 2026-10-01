import redis
import app as app_module


class FakeRedis:
    def __init__(self):
        self.n = 0

    def incr(self, key):
        self.n += 1
        return self.n


class BrokenRedis:
    def incr(self, key):
        raise redis.exceptions.ConnectionError()


def test_compteur_incremente(monkeypatch):
    monkeypatch.setattr(app_module, "db", FakeRedis())
    client = app_module.app.test_client()

    r1 = client.get("/")
    r2 = client.get("/")

    assert r1.status_code == 200
    assert "vue 1 fois" in r1.get_data(as_text=True)
    assert "vue 2 fois" in r2.get_data(as_text=True)


def test_affiche_id_conteneur(monkeypatch):
    monkeypatch.setattr(app_module, "db", FakeRedis())
    r = app_module.app.test_client().get("/")
    assert "Je suis le conteneur" in r.get_data(as_text=True)


def test_redis_indisponible(monkeypatch):
    monkeypatch.setattr(app_module, "db", BrokenRedis())
    r = app_module.app.test_client().get("/")
    assert r.status_code == 503
