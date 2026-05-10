"""Automated test: music.163.com -> leaderboard -> play 3rd song in New Song chart."""

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeout, FrameLocator

LEADERBOARD_URL = "https://music.163.com/#/discover/toplist"
NEW_SONG_CHART_ID = "3779629"


def _dismiss_popups(page: Page) -> None:
    """Dismiss any overlay popups that may block interaction."""
    for sel in [
        "a.close", "span.close", ".u-dlg-close", ".dialog-close",
        ".zcls", ".z-close", '[class*="dialog"] [class*="close"]',
    ]:
        for el in page.locator(sel).all():
            try:
                if el.is_visible():
                    el.click()
                    page.wait_for_timeout(400)
            except PlaywrightTimeout:
                pass


def _iframe(page: Page) -> FrameLocator:
    """Main content lives inside #g_iframe."""
    return page.frame_locator("#g_iframe")


def test_play_third_song_in_new_song_chart(page: Page) -> None:
    """Open music.163.com, navigate to New Song chart, click play on 3rd song."""

    # Step 1: Open homepage
    page.goto("https://music.163.com/")
    _dismiss_popups(page)

    # Step 2: Navigate to New Song chart
    page.goto(f"{LEADERBOARD_URL}?id={NEW_SONG_CHART_ID}")
    _dismiss_popups(page)

    content = _iframe(page)

    # Step 3: Confirm we are on the New Song chart
    content.locator(".mine.z-selected .name").first.wait_for(
        state="visible", timeout=15000
    )
    chart_name = content.locator(".mine.z-selected .name").first.inner_text()
    assert "新歌榜" in chart_name, f"Expected 新歌榜 but got: {chart_name}"
    print(f"  -> Chart confirmed: {chart_name}")

    # Step 4: Find the 3rd song and click play
    song_rows = content.locator("table tbody tr")
    song_rows.first.wait_for(state="attached", timeout=15000)
    assert song_rows.count() >= 3, f"Need 3+ songs, found {song_rows.count()}"
    print(f"  -> {song_rows.count()} songs loaded")

    third = song_rows.nth(2)
    song_name = (third.locator("b[title]").first.get_attribute("title") or "").strip()
    print(f"  -> Target song: {song_name}")

    play_btn = third.locator("span.ply[data-res-action='play']").first
    play_btn.wait_for(state="visible", timeout=5000)
    play_btn.click()

    # Step 5: Screenshot result (web player requires login for actual playback)
    page.screenshot(path="playback_result.png", full_page=True)
    print("  -> Screenshot saved: playback_result.png")
