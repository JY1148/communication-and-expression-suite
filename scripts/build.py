"""Assemble independent static apps; sites.json is the sister-site registry."""
import json, pathlib, shutil, html
root=pathlib.Path(__file__).resolve().parents[1]
out=root/'dist'
if out.exists(): shutil.rmtree(out)
out.mkdir()
sites=json.loads((root/'sites.json').read_text())
for site in sites:
 source=root/'apps'/site['id']/'dist'
 assert (source/'index.html').is_file(), source
 shutil.copytree(source,out/site['id'])
# Replace only the known sister-site URLs in deploy output; source snapshots stay intact.
for page in out.rglob('*.html'):
 text=page.read_text()
 for site in sites: text=text.replace(site['currentUrl'],site['path'])
 page.write_text(text)
links=''.join('<li><a href="'+html.escape(s['path'])+'">'+html.escape(s['name'])+'</a></li>' for s in sites)
(out/'index.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>英语练习空间</title><style>body{font:18px system-ui;max-width:760px;margin:12vh auto;padding:24px;background:#f7f7f4;color:#161616}li{margin:24px 0}a{color:#1645db}</style><h1>英语练习空间</h1><ul>'+links+'</ul></html>')
print('Built '+str(len(sites))+' sites into dist/')
