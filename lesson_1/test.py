from subprocess import Popen, PIPE, call
import platform
import chardet

param = '-n' if platform.system().lower() == 'windows' else '-c'
args = ['ping', param, '1', '192.168.1.10']
with Popen(args, stdout=PIPE, stderr=PIPE) as ping_process:
    out = ping_process.stdout.read()
    coding = chardet.detect(out)
    result = out.decode(coding['encoding'])
    print(result)
