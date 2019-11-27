# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=[
                 '/home/ovs-dl/git/Medical_IMG-viewer',
                 "C:/Python36/lib/site-packages/PyQt5/Qt/bin",
                "./qt_assets"
             ],
             binaries=[],
             datas=[
                 ('./dash_assets/package-info.json', 'dash_core_components'), 
                 ('./dash_assets/dash_core_components.min.js', 'dash_core_components'),
                 ('./dash_assets/async~datepicker.js', 'dash_core_components'), 
                 ('./dash_assets/async~dropdown.js', 'dash_core_components'), 
                 ('./dash_assets/async~graph.js', 'dash_core_components'), 
                 ('./dash_assets/async~markdown.js', 'dash_core_components'), 
                 ('./dash_assets/async~plotlyjs.js', 'dash_core_components'), 
                 ('./dash_assets/async~upload.js', 'dash_core_components'),  
                 ('./dash_assets/highlight.pack.js', 'dash_core_components'), 

                 ('./dash_assets/package-info.json', 'dash_html_components'),  
                 ('./dash_assets/dash_html_components.min.js', 'dash_html_components'), 

                 ('./dash_assets/polyfill@7.7.0.min.js', 'dash_renderer'), 
                 ('./dash_assets/dash_renderer.min.js', 'dash_renderer'), 
                 ('./dash_assets/react@16.8.6.min.js', 'dash_renderer'), 
                 ('./dash_assets/react-dom@16.8.6.min.js', 'dash_renderer'), 
                 ('./dash_assets/prop-types@15.7.2.min.js', 'dash_renderer'), 
                 ('./dash_assets/dash_renderer.min.js', 'dash_renderer'), 
                 ('assets', 'assets')
             ],
             hiddenimports=[],
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
          name='app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
