"""Settings shared by the Group 7 UI tests. Uses the same environment variables as
member4/AutomatedUI (ST02) so one shell setup runs the whole UI suite."""
import os

from selenium import webdriver

BASE = os.environ.get("SHOP_BASE_URL", "http://157.85.102.236/shop").rstrip("/")
STAFF_USER = os.environ.get("SHOP_USERNAME") or os.environ.get("STAFF_USER", "itcs386-g07")
# Browser login password (row 07, "Password (shop + hotel)"), NOT the Shop API password.
STAFF_PASSWORD = os.environ.get("SHOP_PASSWORD") or os.environ.get("STAFF_PASSWORD", "")
BROWSER = os.environ.get("BROWSER", "edge").lower()  # edge (team default) or chrome


def make_driver():
    """New browser with its own empty profile, so staff and guest sessions never mix."""
    headless = os.environ.get("HEADLESS") == "1"
    if BROWSER == "chrome":
        opts = webdriver.ChromeOptions()
        factory = webdriver.Chrome
    else:
        opts = webdriver.EdgeOptions()
        factory = webdriver.Edge
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")
    # The shop is plain http. Stop Edge/Chrome from upgrading it to https or showing the
    # "not secure" warning page, which detaches the page from WebDriver.
    opts.add_argument("--disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable,"
                      "HttpsFirstModeV2ForTypicallySecureUsers,AutomaticHttpsDefault,"
                      "msAutomaticHttpsDefault,msEdgeAutomaticHttps")
    opts.add_experimental_option("prefs", {"https_only_mode_enabled": False,
                                           "https_upgrades_enabled": False})
    return factory(options=opts)


def open_page(drv, url, ready, timeout=120):
    """Open url and wait until ready(drv) is truthy. Retries when the browser drops the page
    (Edge 'target frame detached'); if an http warning page appears, click through it in the
    window and the wait continues."""
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.support.ui import WebDriverWait
    last = None
    for _ in range(3):
        try:
            drv.get(url)
            return WebDriverWait(drv, timeout, ignored_exceptions=(WebDriverException,)).until(ready)
        except WebDriverException as exc:
            last = exc
    raise last
