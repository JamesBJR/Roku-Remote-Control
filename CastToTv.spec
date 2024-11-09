# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['CastToTv.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/GitHubRepos/Roku-Remote-Control/Soundeffects/269504__michorvath__button-click.wav', '.')],  # Update this line with the new path
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
    name='CastToTv',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='remoteIcon.ico',  # Update icon path
    version='version.txt',  # Reference the version file
    company_name='BJR Software',
)
