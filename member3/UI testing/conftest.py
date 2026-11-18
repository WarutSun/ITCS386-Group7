"""Fixtures for the ST03 UI test (and any later scenario placed in this folder)."""
import os
from datetime import datetime

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from ui_common import STAFF_PASSWORD, make_driver

EVIDENCE_DIR = os.path.join(os.path.dirname(__file__), "evidence")


@pytest.fixture(autouse=True)
def _need_password():
    if not STAFF_PASSWORD:
        pytest.fail("Set SHOP_PASSWORD (browser login password, see env.example). Never hard-code it.")


@pytest.fixture
def run_id():
    """Unique per run so repeated runs never collide (G07 prefix + date-time)."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


@pytest.fixture
def staff_driver():
    drv = make_driver()
    yield drv
    drv.quit()


@pytest.fixture
def customer_driver():
    """Separate browser = clean guest session, independent of the staff login."""
    drv = make_driver()
    yield drv
    drv.quit()


@pytest.fixture
def wait():
    return lambda drv, timeout=20: WebDriverWait(drv, timeout)


@pytest.fixture
def shot(request, run_id):
    """Save numbered screenshots to evidence/<run_id>/."""
    folder = os.path.join(EVIDENCE_DIR, run_id)
    os.makedirs(folder, exist_ok=True)
    counter = {"n": 0}

    def _shot(drv, label):
        counter["n"] += 1
        drv.save_screenshot(os.path.join(folder, f"{request.node.name}_{counter['n']:02d}_{label}.png"))
    return _shot
