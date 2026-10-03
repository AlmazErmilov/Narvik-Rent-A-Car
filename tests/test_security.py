import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1] / 'rent_a_car_website'


@pytest.fixture(scope='module')
def application():
    spec = importlib.util.spec_from_file_location('legacy_site', ROOT / 'app.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.app.config['TESTING'] = True
    return module.app


@pytest.mark.parametrize('path', ['/', '/about', '/services', '/renting-agreement', '/contact', '/company-cars'])
def test_pages_are_served_without_debugger(application, path):
    response = application.test_client().get(path)
    assert response.status_code == 200
    assert application.debug is False
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert response.headers['X-Frame-Options'] == 'DENY'


def test_unknown_route_does_not_expose_debugger(application):
    response = application.test_client().get('/missing')
    assert response.status_code == 404
    assert b'Werkzeug Debugger' not in response.data


def test_run_module_has_a_working_application(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT))
    spec = importlib.util.spec_from_file_location('legacy_run', ROOT / 'run.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.app.debug is False
