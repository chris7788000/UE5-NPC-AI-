#!/usr/bin/env python3
"""Small dependency-free APK build, for a host with Java 17 and SDK 35 tools.
Example: python3 build_local.py --sdk /path/to/sdk --output /path/PocketDesk.apk
The SDK path may contain standard platforms/build-tools or this task's extracted layout.
"""
import argparse, os, pathlib, shutil, subprocess, zipfile, xml.etree.ElementTree as E
p=argparse.ArgumentParser()
p.add_argument('--sdk',required=True);p.add_argument('--output',default='PocketDesk.apk')
p.add_argument('--java',default='java');args=p.parse_args()
root=pathlib.Path(__file__).resolve().parent;sdk=pathlib.Path(args.sdk).resolve();out=pathlib.Path(args.output).resolve();build=root/'build-manual'
if build.exists():shutil.rmtree(build)
build.mkdir();(build/'classes').mkdir();(build/'dex').mkdir()
android=next(sdk.rglob('android.jar'));aapt=next(sdk.rglob('aapt2'));bt=aapt.parent
os.environ['LD_LIBRARY_PATH']=str(bt/'lib64')+':'+os.environ.get('LD_LIBRARY_PATH','')
for name in ['aapt2','zipalign']:(bt/name).chmod(0o755)
def run(*cmd):subprocess.run([str(x) for x in cmd],check=True,cwd=root)
E.register_namespace('android','http://schemas.android.com/apk/res/android')
manifest=E.parse(root/'app/src/main/AndroidManifest.xml');manifest.getroot().set('package','com.pocketdesk.app');manifest.write(build/'AndroidManifest.xml',encoding='utf-8',xml_declaration=True)
run(aapt,'compile','--dir',root/'app/src/main/res','-o',build/'resources.zip')
run(aapt,'link','-o',build/'resources.apk','--manifest',build/'AndroidManifest.xml','-I',android,'-A',root/'app/src/main/assets',build/'resources.zip')
sources=list((root/'app/src/main/java').rglob('*.java'))
run(args.java,'-m','jdk.compiler/com.sun.tools.javac.Main','--release','8','-classpath',android,'-encoding','UTF-8','-d',build/'classes',*sources)
run(args.java,'-cp',bt/'lib/d8.jar','com.android.tools.r8.D8','--min-api','26','--lib',android,'--output',build/'dex',*list((build/'classes').rglob('*.class')))
shutil.copyfile(build/'resources.apk',build/'unsigned.apk')
with zipfile.ZipFile(build/'unsigned.apk','a',zipfile.ZIP_DEFLATED) as z:
 for f in (build/'dex').glob('*.dex'):z.write(f,f.name)
run(bt/'zipalign','-p','-f','4',build/'unsigned.apk',build/'aligned.apk')
key=root/'signing/pocketdesk-personal.p12';key.parent.mkdir(exist_ok=True)
if not key.exists():
 run(args.java,'-m','java.base/sun.security.tools.keytool.Main','-genkeypair','-keystore',key,'-storetype','PKCS12','-storepass','pocketdesk-local-build','-keypass','pocketdesk-local-build','-alias','pocketdesk','-keyalg','RSA','-keysize','2048','-validity','10000','-dname','CN=PocketDesk Personal App, O=PocketDesk, C=AT')
out.parent.mkdir(parents=True,exist_ok=True)
run(args.java,'-jar',bt/'lib/apksigner.jar','sign','--ks',key,'--ks-pass','pass:pocketdesk-local-build','--key-pass','pass:pocketdesk-local-build','--ks-key-alias','pocketdesk','--v1-signing-enabled','true','--v2-signing-enabled','true','--v3-signing-enabled','true','--out',out,build/'aligned.apk')
run(args.java,'-jar',bt/'lib/apksigner.jar','verify','--verbose',out)
print('Built:',out,'Bytes:',out.stat().st_size)
