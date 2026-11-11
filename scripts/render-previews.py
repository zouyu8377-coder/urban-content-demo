"""Render referenced PDF pages to static JPEG assets using Poppler.

Usage: python scripts/render-previews.py --source-dir <PDF-directory>
Only referenced pages are included; complete PDFs are not copied.
"""
import argparse,json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);args=p.parse_args()
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data'/'content.json').read_text(encoding='utf-8'))
dest=root/'assets'/'previews';dest.mkdir(parents=True,exist_ok=True)
refs=sorted({(r['doc'],r['page']) for m in data['materials'] for r in m['refs']})
def run(ref):
 doc,page=ref;source=args.source_dir/data['sources'][doc]['name'];target=dest/f'{doc}-{page}'
 subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-scale-to','1500','-jpeg','-jpegopt','quality=70,optimize=y',str(source),str(target)],check=True,capture_output=True)
 return target.with_suffix('.jpg').stat().st_size
with ThreadPoolExecutor(max_workers=3) as pool:sizes=list(pool.map(run,refs))
print(f'{len(sizes)} referenced page previews; {sum(sizes)/1024/1024:.1f} MiB')
