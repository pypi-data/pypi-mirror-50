import os
import sys
import tempfile
import subprocess

import requests

from . import util

def command(args):
    if args.port:
        selected_port = args.port
    else:
        selected_port = util.select_port()

    # obnizOSのクローンおよび更新
    print()
    ## 一時ファイルにobnizOSをクローンしてくる
    with tempfile.TemporaryDirectory() as dirname:
        filenames = ['bootloader.bin', 'obniz.bin', 'partitions.bin']
        for file in filenames:
            print("Downloading {}...".format(file))
            resp = requests.get("https://raw.github.com/obniz/obnizos-esp32w/master/" + file)
            save_to = os.path.join(dirname, file)
            if resp.ok:
                with open(save_to, 'wb') as save_file:
                    save_file.write(resp.content)
            else:
                print("Error: failed to download {}.".format(file))
                sys.exit(1)
        # obnizOSの書き込み
        print()
        proc = subprocess.run(
            "esptool.py --port {} -b {} --after hard_reset write_flash 0x1000 bootloader.bin 0x10000 obniz.bin 0x8000 partitions.bin".format(selected_port, args.bps),
            shell=True,
            cwd=dirname
        )
