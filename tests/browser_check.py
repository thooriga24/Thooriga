"""Real browser/API checks. No AI responses are intercepted or fabricated.

Requires both local servers and Playwright/Chromium. Set THOORIGA_BASE_URL or
CHROMIUM_PATH to adapt to another local setup. Real inference is deliberately
not started automatically when a model is available; verify it separately.
"""
import io
import json
import os
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = os.environ.get('THOORIGA_BASE_URL', 'http://127.0.0.1:5173').rstrip('/')
DOCS = ROOT / 'docs'
DOCS.mkdir(exist_ok=True)
SAMPLE = ROOT / 'backend' / 'samples' / 'astronaut.png'


def card_order(page):
    return page.locator('.photo-card .photo-heading strong').all_text_contents()


def no_overflow(page):
    return page.evaluate('document.documentElement.scrollWidth <= innerWidth')


with sync_playwright() as playwright:
    chromium = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium')
    launch = {'headless': True}
    if chromium:
        launch['executable_path'] = chromium
    # Container execution only: a native desktop can run its Chromium sandbox.
    if os.name != 'nt' and hasattr(os, 'geteuid') and os.geteuid() == 0:
        launch['args'] = ['--no-sandbox']
    browser = playwright.chromium.launch(**launch)
    page = browser.new_page(viewport={'width': 1440, 'height': 1100})
    page_errors = []
    requests = []
    page.on('pageerror', lambda error: page_errors.append(str(error)))
    page.on('request', lambda request: requests.append(request.url))
    report = {'base_url': BASE_URL, 'mocked_ai': False, 'checks': {}, 'viewports': []}
    checks = report['checks']
    try:
        page.goto(BASE_URL)
        expect(page.get_by_role('heading', name='Photo library', exact=True)).to_be_visible()
        expect(page.get_by_role('button', name='Analyze collection')).to_be_disabled()
        assert no_overflow(page)
        page.screenshot(path=str(DOCS / 'desktop.png'), full_page=True)
        model_available = page.request.get(BASE_URL + '/api/models/status').json()['available']
        report['model_available'] = model_available

        photo_bytes = SAMPLE.read_bytes()
        page.locator('input[type=file]').set_input_files([
            {'name': 'nasa-sample-a.png', 'mimeType': 'image/png', 'buffer': photo_bytes},
            {'name': 'nasa-sample-b.png', 'mimeType': 'image/png', 'buffer': photo_bytes},
        ])
        expect(page.locator('.photo-card')).to_have_count(2)
        assert card_order(page) == ['Frame 01', 'Frame 02']
        checks['real_upload_preview'] = True

        page.get_by_label('Selection mode').select_option('Mood / Atmosphere')
        expect(page.get_by_label('Selection mode')).to_have_value('Mood / Atmosphere')
        page.get_by_label('Output format').select_option('original')
        page.get_by_label('Shortlist size').select_option('2')
        checks['mode_format_size_selection'] = True

        page.get_by_role('button', name=re.compile(r'^Assessed')).click()
        expect(page.locator('.photo-card')).to_have_count(0)
        expect(page.get_by_role('heading', name='No matching photographs')).to_be_visible()
        page.get_by_role('button', name=re.compile(r'^Similar')).click()
        expect(page.locator('.photo-card')).to_have_count(2)
        page.get_by_role('button', name=re.compile(r'^All photos')).click()
        page.get_by_label('Search photographs').fill('frame 02')
        expect(page.locator('.photo-card')).to_have_count(1)
        assert card_order(page) == ['Frame 02']
        page.get_by_label('Search photographs').fill('')
        page.get_by_label('Sort photographs').select_option('fit')
        expect(page.get_by_label('Sort photographs')).to_have_value('fit')
        page.get_by_label('Sort photographs').select_option('upload')
        checks['filter_search_sort'] = True
        checks['duplicate_group_visible'] = page.get_by_text('Similar group · 2 frames', exact=True).count() == 2
        page.screenshot(path=str(DOCS / 'library.png'), full_page=True)

        for index in range(2):
            page.locator('.photo-card').nth(index).get_by_role('button', name='Compare', exact=True).click()
        page.get_by_role('button', name='Compare two', exact=True).click()
        expect(page.get_by_role('heading', name='Compare photographs', exact=True)).to_be_visible()
        expect(page.locator('.compare-grid figure')).to_have_count(2)
        page.get_by_role('button', name='Select photo', exact=True).nth(0).click()
        page.get_by_role('button', name='Select photo', exact=True).click()
        page.get_by_role('button', name='Close comparison').click()
        checks['side_by_side_comparison'] = True

        page.locator('.sidebar nav button').nth(1).click()
        expect(page.get_by_role('heading', name='Shortlist', exact=True)).to_be_visible()
        assert card_order(page) == ['Frame 01', 'Frame 02']
        page.locator('.photo-card').nth(0).get_by_role('button', name='Move photo down').click()
        assert card_order(page) == ['Frame 02', 'Frame 01']
        page.locator('.photo-card').nth(0).get_by_role('button', name='Deselect photo').click()
        expect(page.locator('.photo-card')).to_have_count(1)
        assert card_order(page) == ['Frame 01']
        page.locator('.sidebar nav button').nth(0).click()
        page.locator('.photo-card').nth(1).get_by_role('button', name='Select photo', exact=True).click()
        page.locator('.sidebar nav button').nth(1).click()
        assert card_order(page) == ['Frame 01', 'Frame 02']
        checks['selection_deselection_restore_reorder'] = True

        with page.expect_download() as download_info:
            page.get_by_role('button', name='Export 2', exact=True).click()
        download = download_info.value
        with zipfile.ZipFile(io.BytesIO(Path(download.path()).read_bytes())) as archive:
            assert archive.namelist() == ['thooriga-01.jpg', 'thooriga-02.jpg']
            assert all(len(archive.read(name)) > 0 for name in archive.namelist())
        checks['real_zip_export'] = True

        page.locator('.sidebar nav button').nth(0).click()
        page.get_by_role('button', name='Analyze collection', exact=True).click()
        expect(page.get_by_role('alert')).to_contain_text('Write a creative brief')
        page.get_by_role('button', name='Dismiss error').click()
        checks['brief_validation'] = True
        if not model_available:
            page.locator('#brief').fill('Find a clear portrait photograph with simple framing')
            page.get_by_role('button', name='Analyze collection', exact=True).click()
            expect(page.get_by_text('The local model could not finish.', exact=True)).to_be_visible(timeout=30000)
            assert page.get_by_text('Local model unavailable or timed out', exact=True).count() == 2
            checks['real_missing_model_error'] = True
        else:
            checks['real_missing_model_error'] = 'skipped: model available; no inference started automatically'
        page.locator('.photo-card').nth(1).get_by_role('button', name='Remove photo').click()
        expect(page.locator('.photo-card')).to_have_count(1)
        checks['photo_removal'] = True
        page.get_by_role('button', name='Clear collection', exact=True).click()
        expect(page.get_by_role('heading', name='Add photographs', exact=True)).to_be_visible()
        page.get_by_role('button', name='Try a public-domain sample').click()
        expect(page.locator('.photo-card')).to_have_count(1)
        expect(page.get_by_text('512 × 512', exact=True)).to_be_visible()
        page.get_by_role('button', name='Clear collection', exact=True).click()
        expect(page.get_by_role('heading', name='Add photographs', exact=True)).to_be_visible()
        checks['clear_and_public_domain_sample'] = True
        page.locator('#brief').fill('')

        for width, height in [(320, 780), (390, 844), (768, 1024)]:
            page.set_viewport_size({'width': width, 'height': height})
            assert no_overflow(page), f'Horizontal overflow at {width}px'
            page.locator('.workspace-footer').get_by_role('button', name='Privacy & storage').click()
            expect(page.get_by_role('heading', name='Privacy & storage', exact=True)).to_be_visible()
            assert no_overflow(page), f'Privacy horizontal overflow at {width}px'
            page.get_by_role('button', name='Back to photo library', exact=True).click()
            expect(page.get_by_role('heading', name='Photo library', exact=True)).to_be_visible()
            if width == 390:
                page.screenshot(path=str(DOCS / 'mobile.png'), full_page=True)
            report['viewports'].append({'width': width, 'height': height, 'no_horizontal_overflow': True, 'privacy_navigation': True})
        checks['responsive_and_phone_privacy'] = True

        assert not page_errors, page_errors
        expected_origin = urlparse(BASE_URL).netloc
        outbound = [url for url in requests if urlparse(url).scheme in ('http', 'https', 'ws', 'wss') and urlparse(url).netloc != expected_origin]
        assert not outbound, outbound
        checks['no_browser_page_errors'] = True
        checks['browser_requests_local_origin_only'] = True
        report['page_errors'] = page_errors
        report['observed_request_count'] = len(requests)
        report['status'] = 'passed'
        report['limitations'] = [
            'Real Gemma vision inference is not verified by this browser check.',
            'Browser request observations are not an OS-level network audit.',
            'No relevance, effort-saving, VRAM, or physical phone networking claim is made.',
            'Screenshots use empty UI or public-domain NASA sample; no AI results are fabricated.',
        ]
        print(json.dumps(report, indent=2))
    except Exception as error:
        report['status'] = 'failed'
        report['failure'] = str(error)
        page.screenshot(path=str(DOCS / 'browser-failure.png'), full_page=True)
        raise
    finally:
        (DOCS / 'browser-check-results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        browser.close()
