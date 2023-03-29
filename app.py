import os

from flask import Flask, request
import json
import subprocess
from pathlib import Path
import shutil

app = Flask(__name__)


@app.route('/align', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.data)
        media = data.get('media')
        subtitle = data.get('subtitle')
        media_posix = Path(media)

        temp_path = media_posix.parents[0] / Path('temp' + media_posix.suffix)
        media_path = f"{media}"
        subtitle_path = f"{subtitle}"
        single_aligned_path = f"""{subtitle + ".aligned"}"""
        dual_aligned_path = f"""{subtitle + ".aligned_dual"}"""  

        if subprocess.run(["subaligner",
                           "-m",
                           "single",
                           "-v",
                           media_path,
                           "-s",
                           subtitle_path,
                           "-o",
                           single_aligned_path]):

            if subprocess.run(["subaligner",
                               "-m",
                               "dual",
                               "-v",
                               media_path,
                               "-s",
                               subtitle_path,
                               "-o",
                               dual_aligned_path]):

                if subprocess.run(["mkvmerge",
                                   "-o",
                                   temp_path,
                                   media_path,
                                   "--language",
                                   "0:eng",
                                   "--track-name",
                                   "0:Aligned-Single",
                                   single_aligned_path,
                                   "--language",
                                   "1:eng",
                                   "--track-name",
                                   "1:Aligned-Dual",
                                   dual_aligned_path
                                   ]):
                    print('here')
                    # shutil.move(temp_path, media_path)
                    # os.remove(single_aligned_path)
                    # os.remove(dual_aligned_path)

        return 'Success', 200
