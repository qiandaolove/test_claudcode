import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/147.0.0.0 Safari/537.36"
        ),
        # Bypass bot detection
        "bypass_csp": True,
        "java_script_enabled": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, request):
    headed = request.config.getoption("--headed", default=False)
    return {
        **browser_type_launch_args,
        "headless": not headed,
        "slow_mo": 300 if headed else 0,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-features=IsolateOrigins,site-per-process",
        ],
    }
