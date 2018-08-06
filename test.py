import zipfile
import os
from io import BytesIO

path2zip = os.getcwd() +  os.path.join(r"\archives", 'Response-80-44697788.zip')

with zipfile.ZipFile(path2zip, "r") as zip_ref:
  innerZipFileName = [f for f in  zip_ref.namelist() if f[-4:] == '.zip'][0]
  with zip_ref.open(innerZipFileName) as nested:
    nested_filedata = BytesIO(nested.read())
    with zipfile.ZipFile(nested_filedata) as n:
      n.extractall(os.getcwd() +  os.path.join(r"\xml"))