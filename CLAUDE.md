# CLAUDE.md — music.163.com automation test

## Commands

```bash
# Headless (default)
pytest test_music163.py -v -s

# Headed — watch browser steps
pytest test_music163.py -v -s --headed
```

## Target site architecture

- **SPA with hash routing**: `https://music.163.com/#/discover/toplist?id=3779629`
- **iframe**: main content loads inside `<iframe id="g_iframe">`. Top nav and player bar are on the outer page. Always use `page.frame_locator("#g_iframe")` for content selectors.
- **Chart IDs**: 新歌榜 = `3779629`. Direct URL navigation is more reliable than clicking through UI.

## Anti-bot config (conftest.py)

- Custom User-Agent (Chrome 147 on Windows)
- `--disable-blink-features=AutomationControlled`
- `--disable-features=IsolateOrigins,site-per-process`
- Do NOT define a custom `pytest_addoption` for `--headed` — pytest-playwright already registers it.

## Key patterns

- **No hard waits**: use `locator.first.wait_for(state="visible", timeout=N)` instead of `page.wait_for_timeout()`
- **Popup dismissal**: the site shows modal overlays — iterate common close selectors before interacting
- **Web player limitation**: clicking play triggers UI response but full playback requires login/desktop client
