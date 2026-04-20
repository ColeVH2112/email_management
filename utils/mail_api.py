"""
Fetches emails from Outlook Web App (OWA) using a saved browser session.

First run: opens a visible browser window so you can log in manually
           (handles SSO, Duo MFA, etc.) then saves the cookies.
Later runs: loads the saved cookies and runs headlessly.

Use --refresh in main.py to force a new login at any time.
"""

import asyncio
from playwright.async_api import async_playwright, Page, BrowserContext

from auth.session_manager import load_session, save_session
from config import OWA_URL, MAX_EMAILS

_LOGIN_SIGNALS = ["login", "signin", "auth", "sso", "saml", "weblogin", "microsoftonline.com/common/oauth"]


def _looks_like_login_page(url: str) -> bool:
    return any(s in url.lower() for s in _LOGIN_SIGNALS)


async def _manual_login_prompt(page: Page):
    print("\n" + "=" * 60)
    print("MANUAL LOGIN REQUIRED")
    print("=" * 60)
    print(f"A browser window is open. Please log in (including MFA).")
    print("When you can see your inbox, press Enter here to continue.")
    print("=" * 60 + "\n")
    await asyncio.get_event_loop().run_in_executor(None, input)


async def _open_context(playwright, headless: bool, cookies: list | None) -> tuple:
    browser = await playwright.chromium.launch(headless=headless)
    context = await browser.new_context()
    if cookies:
        await context.add_cookies(cookies)
    return browser, context


async def _fetch_emails_async(force_login: bool = False) -> list[dict]:
    saved_cookies = None if force_login else load_session()
    need_login = saved_cookies is None

    async with async_playwright() as p:
        browser, context = await _open_context(p, headless=not need_login, cookies=saved_cookies)
        page = await context.new_page()

        await page.goto(OWA_URL, wait_until="domcontentloaded")

        # Detect if the saved session didn't work (redirected to login)
        if not need_login and _looks_like_login_page(page.url):
            print("Saved session is no longer valid (redirected to login).")
            await browser.close()
            need_login = True
            browser, context = await _open_context(p, headless=False, cookies=None)
            page = await context.new_page()
            await page.goto(OWA_URL, wait_until="domcontentloaded")

        if need_login:
            await _manual_login_prompt(page)
            await page.wait_for_load_state("networkidle", timeout=30_000)
            cookies = await context.cookies()
            save_session(cookies)

        # Give the inbox a moment to fully render
        try:
            await page.wait_for_load_state("networkidle", timeout=15_000)
        except Exception:
            pass

        emails = await _scrape_inbox(page, MAX_EMAILS)
        await browser.close()
        return emails


# ---------------------------------------------------------------------------
# DOM scraping helpers
# ---------------------------------------------------------------------------

# OWA email list row selectors, tried in order
_ROW_SELECTORS = [
    '[role="option"]',
    '[data-convid]',
    '[role="listitem"]',
]

# Reading-pane body selectors, tried in order
_BODY_SELECTORS = [
    '[role="document"]',
    '[aria-label="Message body"]',
    '.rps_0f57',
    '.allowTextSelection',
]

# Reading-pane sender selectors
_SENDER_SELECTORS = [
    '[aria-label*="From"]',
    'span[title*="@"]',
    '.oIvO0h',
]

# Reading-pane subject selectors
_SUBJECT_SELECTORS = [
    'h1[role="heading"]',
    'h1',
    '[role="heading"][aria-level="1"]',
]


async def _first_text(page: Page, selectors: list[str], max_len: int = 3000) -> str:
    for sel in selectors:
        try:
            el = await page.query_selector(sel)
            if el:
                text = (await el.inner_text()).strip()
                if text:
                    return text[:max_len]
        except Exception:
            continue
    return ""


async def _scrape_inbox(page: Page, max_count: int) -> list[dict]:
    emails = []

    # Find email rows
    rows = []
    for sel in _ROW_SELECTORS:
        try:
            await page.wait_for_selector(sel, timeout=8_000)
            rows = await page.query_selector_all(sel)
            if rows:
                print(f"Found {len(rows)} email rows (selector: {sel!r})")
                break
        except Exception:
            continue

    if not rows:
        print("WARNING: No email rows found. Inbox may be empty, or the OWA")
        print(f"         selectors need updating for: {page.url}")
        return emails

    for i, row in enumerate(rows[:max_count]):
        try:
            await row.click()
            # Wait for reading pane to update; ignore timeout — some clicks are instant
            try:
                await page.wait_for_load_state("networkidle", timeout=4_000)
            except Exception:
                await page.wait_for_timeout(1_200)

            subject = await _first_text(page, _SUBJECT_SELECTORS, max_len=200)
            sender  = await _first_text(page, _SENDER_SELECTORS,  max_len=200)
            body    = await _first_text(page, _BODY_SELECTORS,     max_len=4_000)

            if not (subject or body):
                continue

            # Combine subject into the body string so agents get full context
            combined = f"Subject: {subject}\n\n{body}" if subject else body

            emails.append({
                "id": i + 1,
                "sender": sender or "Unknown",
                "subject": subject or "No subject",
                "body": combined,
            })
            print(f"  [{i + 1}] {sender or '?'} — {subject or '(no subject)'}")

        except Exception as e:
            print(f"  [{i + 1}] Could not read email: {e}")
            continue

    return emails


# ---------------------------------------------------------------------------
# Public synchronous interface
# ---------------------------------------------------------------------------

def fetch_emails(force_login: bool = False) -> list[dict]:
    """Fetch emails from OWA. Opens a browser; handles login automatically."""
    return asyncio.run(_fetch_emails_async(force_login=force_login))
