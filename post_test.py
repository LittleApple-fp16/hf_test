from huggingface_hub import HfApi, HfFileSystem
from fs_test import repo_name
import os
hug_fs = HfFileSystem(token=os.environ.get('HF_TOKEN'))
hugApi_fs = HfApi(token=os.environ.get('HF_TOKEN'))
hug_fs_sec = HfFileSystem()
print(f"Result with token: {hug_fs.exists(f'{repo_name}/hf_test/.gitattributes')} And Result with no token: {hug_fs_sec.exists(f'{repo_name}/hf_test/.gitattributes')} And Result with HfApi: {hugApi_fs.file_exists(f'{repo_name}/hf_test/.gitattributes')}")