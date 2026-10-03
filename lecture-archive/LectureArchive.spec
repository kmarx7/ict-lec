# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

playwright_data, playwright_binaries, playwright_hidden = collect_all("playwright")

a = Analysis(
    ["app.py"],
    pathex=["."],
    binaries=playwright_binaries,
    datas=playwright_data,
    hiddenimports=playwright_hidden,
    excludes=["pytest", "ruff"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Lecture Archive",
    console=False,
    target_arch=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="Lecture Archive",
)
app = BUNDLE(
    coll,
    name="Lecture Archive.app",
    bundle_identifier="com.lecturearchive.desktop",
    info_plist={
        "CFBundleDisplayName": "강의 아카이브",
        "CFBundleShortVersionString": "0.1.0",
        "NSHighResolutionCapable": True,
    },
)
