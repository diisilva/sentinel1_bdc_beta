#
# This file is part of S1 process Docker.
# Copyright (C) 2022 INPE.
#
# S1 process Docker is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
# ==============================================================================
import os
import shutil
import sys
from pathlib import Path

print(f"\nTEST:{sys.argv[1]}\n")
if len(sys.argv) < 1:
    print('Please provide the input file (.zip)')
    sys.exit(1)

zipfile = sys.argv[1]

installdir = os.environ['INSTALL_DIR'] # '/opt/s1-processing'
inputdir = os.environ['INPUT_DIR'] # '/mnt/input-dir'
outdir_root = os.environ['OUTPUT_DIR'] # '/mnt/output-dir'
workdir_root = os.environ['WORK_DIR'] #'/mnt/work-dir'
srtm_root = os.environ['SRTM_DIR'] #'/mnt/srtm-dir'
orbit_root = os.environ['ORBIT_DIR'] #'/mnt/orbit-dir'

input_file = Path(inputdir) / zipfile
sceneid = input_file.stem
workdir = Path(workdir_root) / sceneid
outdir = Path(outdir_root) / sceneid
worked_filename = 'ortho_' + input_file.stem.split('_')[6] + '.tif'
output_filename = input_file.stem + '_IRDv1.tif'
output_file = outdir / output_filename

# Clean workdir and outputdir
shutil.rmtree(workdir, ignore_errors=True)
Path(workdir).mkdir(parents=True, exist_ok=True)

shutil.copy(input_file, workdir)

os.system(f'python {installdir}/S1_run.py {str(workdir)}')

# Clean workdir
Path(outdir).mkdir(parents=True, exist_ok=True)
worked_file = Path(workdir) / worked_filename
shutil.copy(worked_file, output_file)
shutil.rmtree(workdir, ignore_errors=True)
