import os
import sys
import tempfile
import subprocess

import util

def command(args):
    if args.port:
        selected_port = args.port
    else:
        selected_port = util.select_port()

    # obnizOSのクローンおよび更新
    print()
    ## 一時ファイルにobnizOSをクローンしてくる
    with tempfile.TemporaryDirectory() as dirname:
        proc = subprocess.run(
            "git clone git@github.com:obniz/obnizos-esp32w.git",
            shell=True,
            cwd=dirname
        )
        # obnizOSの書き込み
        print()
        proc = subprocess.run(
            "esptool.py --port {} -b {} --after hard_reset write_flash 0x1000 bootloader.bin 0x10000 obniz.bin 0x8000 partitions.bin".format(selected_port, args.bps),
            shell=True,
            cwd=os.path.join(dirname, "obnizos-esp32w")
        )
