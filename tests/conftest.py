import pytest
import os
import shutil
from first_api.api.run import app
from httpx import AsyncClient


@pytest.fixture
def client():
    yield AsyncClient(app=app, base_url="http://testserver")


@pytest.fixture(autouse=True)
def reset_db():
    test_db_folder = "data-test"
    os.environ["DB_FOLDER"] = test_db_folder
    if os.path.exists(test_db_folder):
        shutil.rmtree(test_db_folder)
    os.mkdir(test_db_folder)
    yield
    shutil.rmtree(test_db_folder)
