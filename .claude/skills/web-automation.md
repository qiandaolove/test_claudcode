---
name: web-automation
description: Playwright web automation testing — setup, iframe handling, anti-bot, waiting patterns
---

# Web Automation with Playwright (Python)

## Project scaffold

```
project/
├── requirements.txt    # playwright, pytest, pytest-playwright
├── conftest.py         # browser context + launch args
└── test_*.py           # test files
```

Run `playwright install chromium` after `pip install -r requirements.txt`.

## conftest.py template

```python
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, request):
    headed = request.config.getoption("--headed", default=False)
    return {
        **browser_type_launch_args,
        "headless": not headed,
        "slow_mo": 300 if headed else 0,
    }
```

Add anti-bot args only for sites that detect automation:
```python
"args": ["--disable-blink-features=AutomationControlled"],
"user_agent": "Mozilla/5.0 ... Chrome/147.0.0.0 Safari/537.36",
```

## iframe handling

If content is inside `<iframe id="x">`, scope all locators through the frame:
```python
content = page.frame_locator("#x")
content.locator(".foo").click()
```

Discover iframes by checking `page.content()` or looking for `<iframe>` in the page source.

## Wait patterns

**Good** — event-driven, returns as soon as element is ready:
```python
locator.first.wait_for(state="visible", timeout=15000)
locator.first.wait_for(state="attached", timeout=15000)
```

**Bad** — blind sleep, wastes time, flaky:
```python
page.wait_for_timeout(5000)
```

`locator.count()` returns immediately (no auto-wait). Use `wait_for` before counting dynamic elements.

## Debug workflow for live sites

1. Run test → read the assertion error
2. `page.screenshot(path="debug.png", full_page=True)` at the failure point
3. `print(page.content())` or `locator.first.inner_html()` to see real DOM
4. Fix selectors based on actual HTML structure
5. Repeat

## Popup / modal dismissal

Iterate common close selectors before interacting:
```python
for sel in [".close", ".dialog-close", '[class*="close"]']:
    for el in page.locator(sel).all():
        if el.is_visible():
            el.click()
            page.wait_for_timeout(400)  # brief pause for animation
```
