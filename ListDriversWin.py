
import subprocess
import re
from datetime import datetime
import hashlib

import json
import argparse

BUFFER_SIZE = 131072 # 128 KB

# Platform:     Windows
# Function:     win_list_kmodules()
# parameters:   None
# Return:       returns the list of device drivers [{},{},...]
def list_kmodules_win():
    p = subprocess.Popen(['driverquery', '-V', '/FO', 'CSV'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = p.communicate()

    res = []

    if err.decode("utf-8") != b'':
    
        out = re.sub(r"\r","",out.decode("utf-8").strip())
        out = out.split("\n")
    
        fields = re.sub(r'(^"|"$)','',out[0]).split('","')
        out = out[2:]

        for module in out:
        
            # turn into dict:
            mod = dict(zip(fields, re.sub(r'(^"|"$)','',module).split('","')))
        
            # fix datetime format and store in @timestamp key:
            timestamp = "1971-01-01T00:00:00"
            ts = mod["Link Date"].split() if mod["Link Date"] != "" else None
        
            if ts:
                date = ts[0].split('/')
                time = ts[1].split(':')
                dt = datetime(int(date[2]),
                              int(date[0]),
                              int(date[1]),
                              int(time[0]),
                              int(time[1]),
                              int(time[2]),)
                timestamp = dt.strftime("%Y-%m-%d %I:%M:%S ") + ts[2]
        
                dt = datetime.strptime(timestamp,"%Y-%m-%d %I:%M:%S %p")
                timestamp = dt.strftime("%Y-%m-%dT%H:%M:%S")
        
            mod["@timestamp"] = timestamp
            
            # calculate the SHA1 hash and store it in SHA1 key:
            sha1 = hashlib.sha1()
            with open(mod["Path"], 'rb') as f:
                while True:
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    sha1.update(data)
            mod["SHA1"] = sha1.hexdigest()
            
            res.append(mod)
    return res

# main
def main():
    parser = argparse.ArgumentParser(description="KModules lists the kernel modules with SHA1 and outputs JSON.\n\n")
    parser.add_argument('outfile_abs_path', nargs=1, help="Absulote path of the output JSON file")

    outpath = parser.parse_args().outfile_abs_path[0]

    drivers = list_kmodules_win()

    try:
        with open(outpath, 'w') as of:
            json.dump(drivers,of)
    except Exception as e:
        print(e)

if __name__ == '__main__':
	main()