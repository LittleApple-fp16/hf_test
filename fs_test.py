import os
from textwrap import dedent
from hbutils.system import TemporaryDirectory
from huggingface_hub import CommitOperationAdd, HfApi, HfFileSystem

_GITLFS = dedent("""
*.7z filter=lfs diff=lfs merge=lfs -text
*.arrow filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
*.bz2 filter=lfs diff=lfs merge=lfs -text
*.ckpt filter=lfs diff=lfs merge=lfs -text
*.ftz filter=lfs diff=lfs merge=lfs -text
*.gz filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
*.joblib filter=lfs diff=lfs merge=lfs -text
*.lfs.* filter=lfs diff=lfs merge=lfs -text
*.mlmodel filter=lfs diff=lfs merge=lfs -text
*.model filter=lfs diff=lfs merge=lfs -text
*.msgpack filter=lfs diff=lfs merge=lfs -text
*.npy filter=lfs diff=lfs merge=lfs -text
*.npz filter=lfs diff=lfs merge=lfs -text
*.onnx filter=lfs diff=lfs merge=lfs -text
*.ot filter=lfs diff=lfs merge=lfs -text
*.parquet filter=lfs diff=lfs merge=lfs -text
*.pb filter=lfs diff=lfs merge=lfs -text
*.pickle filter=lfs diff=lfs merge=lfs -text
*.pkl filter=lfs diff=lfs merge=lfs -text
*.pt filter=lfs diff=lfs merge=lfs -text
*.pth filter=lfs diff=lfs merge=lfs -text
*.rar filter=lfs diff=lfs merge=lfs -text
*.safetensors filter=lfs diff=lfs merge=lfs -text
saved_model/**/* filter=lfs diff=lfs merge=lfs -text
*.tar.* filter=lfs diff=lfs merge=lfs -text
*.tar filter=lfs diff=lfs merge=lfs -text
*.tflite filter=lfs diff=lfs merge=lfs -text
*.tgz filter=lfs diff=lfs merge=lfs -text
*.wasm filter=lfs diff=lfs merge=lfs -text
*.xz filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.zst filter=lfs diff=lfs merge=lfs -text
*tfevents* filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
""").strip()

repo_name = 'AppleHarem'


def deploy_to_huggingface(workdir: str, revision: str = 'main'):
    name = os.path.basename(workdir)
    repository = f'{repo_name}/{name}'

    hf_client = HfApi(token=os.environ.get('HF_TOKEN'))
    hf_fs = HfFileSystem(token=os.environ.get('HF_TOKEN'))
    if not hf_fs.exists(f'{repository}/.gitattributes'):
        hf_client.create_repo(repo_id=repository, repo_type='model', exist_ok=True)

    if not hf_fs.exists(f'{repository}/.gitattributes') or \
            '*.png filter=lfs diff=lfs merge=lfs -text' not in hf_fs.read_text(f'{repository}/.gitattributes'):
        with TemporaryDirectory() as td:
            _git_attr_file = os.path.join(td, '.gitattributes')
            with open(_git_attr_file, 'w', encoding='utf-8') as f:
                print(_GITLFS, file=f)

            operations = [
                CommitOperationAdd(
                    path_in_repo='.gitattributes',
                    path_or_fileobj=_git_attr_file,
                )
            ]

            commit_message = f'upload'
            hf_client.create_commit(
                repository,
                operations,
                commit_message=commit_message,
                repo_type='model',
                revision=revision,
            )


if __name__ == '__main__':
    deploy_to_huggingface('hf_test')
    hug_fs = HfFileSystem(token=os.environ.get('HF_TOKEN'))
    hug_fs_sec = HfFileSystem()
    print(f"Result with token: {hug_fs.exists(f'{repo_name}/hf_test/.gitattributes')} And Result with no token: {hug_fs_sec.exists(f'{repo_name}/hf_test/.gitattributes')}")
