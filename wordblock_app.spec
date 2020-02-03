# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['wordblock_app.py'],
             pathex=['/home/commander/project/python/wordBlock'],
             binaries=[],
             datas=[],
             hiddenimports=['pyttsx3.drivers', 'pyttsx3.drivers.espeak'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='wordblock_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
