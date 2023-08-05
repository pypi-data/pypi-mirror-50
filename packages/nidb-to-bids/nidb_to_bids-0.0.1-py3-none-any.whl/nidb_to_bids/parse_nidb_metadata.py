
import fnmatch
from pathlib import Path
import pandas as pd
from subprocess import run
import numpy as np
from pandas.io.json import json_normalize
import json
import nibabel as nb
import click

def get_dims(img_path):
    img_shape = nb.load(img_path.as_posix()).shape
    if len(img_shape) == 3:
        img_shape = list(img_shape) + [1]
    return img_shape

def load_json_data(jp):
    filename = jp.parts[-1]
    tmpdf = json_normalize(json.loads(jp.read_text()))
    tmpdf['path'] = jp.as_posix()
    subn = filename.split('_')[0]
    # Make sure that the subject number is the expected length
    if len(subn) != 8:
        raise ValueError(f"Expected subject number to be 8 characters long."
                         f" Parsed subject number was {subn},"
                         f" which is {len(subn)} characters.")
    tmpdf['subn'] = subn
    tmpdf['sesn'] = filename.split('_')[1]
    return tmpdf

def gzip_if_needed(jp):
    ngp = Path(jp.as_posix().replace('.json', '.nii.gz'))
    nip = Path(jp.as_posix().replace('.json', '.nii'))
    if (not ngp.exists()) and nip.exists():
        # Note, this is a security 
        run(['gzip', nip], cwd=nip.parent, check=True)
    return ngp

def test_gzip_if_needed():
    test_json = Path('/tmp/test.json')
    test_img = Path('/tmp/test.nii')
    test_ngp = Path('/tmp/test.nii.gz')
    test_img.touch()
    assert ~test_ngp.exists()
    res_ngp = gzip_if_needed(test_json)
    assert res_ngp == test_ngp
    assert res_ngp.exists()
    assert ~test_img.exists()
    res_ngp.unlink()

test_gzip_if_needed()

@click.command()
@click.option('--dump_path', 
              help="Path to the root of the directories that NiDB data has been dumped to.")
@click.option('--out_path', 
              help="Path to write parsed metadata to.")
def extract_nidb_metadata(dump_path, out_path):
    """Read data from all the bids-esque jsons produced by NiDB nifti + json sidecar export option and grab scan dimensions from the scans themselves, then write all the collected metadata to a csv at the specified location."""
    if ~isinstance(dump_path, Path):
        dump_path = Path(dump_path)
    if ~isinstance(out_path, Path):
        out_path = Path(out_path)

    # We'll be nice and check paths before we start anything
    if not dump_path.exists():
        raise ValueError(f"dump_path should be an existing path. Received {dump_path}")
    if not out_path.parent.exists():
        raise ValueError(f"Can't write to {out_path} because {out_path.parent} doesn't exist.")
    
    df_data= pd.DataFrame([])
    i = 0
    click.echo("JSONs parsed:")
    for jp in dump_path.glob('**/*.json'):
        tmpdf = load_json_data(jp)
        ngp = gzip_if_needed(jp)
        tmpdf['ni'], tmpdf['nj'], tmpdf['nk'], tmpdf['nv'] = get_dims(ngp)
        df_data=df_data.append(tmpdf,sort=True)
        i += 1
        
        if i % 1000 == 0:
            print(i, end=', ', flush=True)
    df_data.to_csv(out_path)

if __name__ == '__main__':
    extract_nidb_metadata()


