# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['full.py'],
    pathex=[],
    binaries=[],
    datas=[('apply_button.png', '.'), ('arrow.png', '.'), ('bot.session', '.'), ('confirm_delete.png', '.'), ('day_message.png', '.'), ('delete_option.png', '.'), ('delete.png', '.'), ('demo1.py', '.'), ('demo2.py', '.'), ('demo3.py', '.'), ('demo4.py', '.'), ('done_button.png', '.'), ('explore_text.png', '.'), ('google_docs.png', '.'), ('https_button.png', '.'), ('links_in_full_document.txt', '.'), ('login_email_button.png', '.'), ('login_page_verified.png', '.'), ('login_page_verifying.png', '.'), ('login_password_button.png', '.'), ('login_screen.png', '.'), ('login_sign_in_button.png', '.'), ('my_account.session', '.'), ('my_bot.session', '.'), ('numbered_list_button.png', '.'), ('one_button.png', '.'), ('publish_button.png', '.'), ('retry_random.png', '.'), ('review-automation007-148b61262097.json', '.'), ('review-automation007-f8f92fc64114.json', '.'), ('session_name.session', '.'), ('telegram.png', '.'), ('telegram.svg', '.'), ('test.py', '.'), ('warning.txt', '.'), ('web.png', '.'), ('website_builder_button.png', '.'), ('website_builder_page.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='full',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
