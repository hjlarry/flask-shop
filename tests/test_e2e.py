import pytest


def is_success_res(client, path):
    rv = client.get(path)
    assert rv.status_code == 200


@pytest.mark.usefixtures("db")
class TestBasicPageCanView:
    def test_404(self, client):
        rv = client.get("/404notfound")
        assert rv.status_code == 404

    def test_homepage(self, client):
        is_success_res(client, "/")

    def test_category_page(self, client):
        is_success_res(client, "/products/category/1")

    def test_product_page(self, client):
        is_success_res(client, "/products/1")

    def test_account_page(self, client):
        is_success_res(client, "/account/")

    def test_login_page(self, client):
        is_success_res(client, "/account/login")

    def test_signup_page(self, client):
        is_success_res(client, "/account/signup")
