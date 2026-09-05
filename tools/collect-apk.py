from pathlib import Path
import shutil,hashlib
p=Path(__file__).resolve().parents[1]
files=list((p/'build/android-qa/proj/build').glob('*/outputs/apk/debug/*.apk'))
assert len(files)==1,files
(p/'releases').mkdir(parents=True,exist_ok=True)
out=p/'releases/Bento-Buddies-0.3.0-QA.apk';shutil.copy2(files[0],out)
h=hashlib.sha256(out.read_bytes()).hexdigest();(p/'releases/SHA256SUMS').write_text(h+'  '+out.name+'\n');print(out);print(h)
