# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['/home/ovs-dl/git/Medical_IMG-viewer'],
             binaries=[],
             datas=[
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/package-info.json', 'dash_core_components'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/dash_core_components.min.js', 'dash_core_components'),
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/async~datepicker.js', 'dash_core_components'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/async~dropdown.js', 'dash_core_components'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/async~graph.js', 'dash_core_components'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/async~markdown.js', 'dash_core_components'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/async~plotlyjs.js', 'dash_core_components'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/async~upload.js', 'dash_core_components'),  
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_core_components/highlight.pack.js', 'dash_core_components'), 

                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_html_components/package-info.json', 'dash_html_components'),  
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_html_components/dash_html_components.min.js', 'dash_html_components'), 
                 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_renderer/polyfill@7.7.0.min.js', 'dash_renderer'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_renderer/dash_renderer.min.js', 'dash_renderer'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_renderer/react@16.8.6.min.js', 'dash_renderer'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_renderer/react-dom@16.8.6.min.js', 'dash_renderer'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_renderer/prop-types@15.7.2.min.js', 'dash_renderer'), 
                 ('/home/ovs-dl/anaconda3/envs/dl/lib/python3.6/site-packages/dash_renderer/dash_renderer.min.js', 'dash_renderer'), 
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
          console=False )
