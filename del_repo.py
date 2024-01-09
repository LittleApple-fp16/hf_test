from huggingface_hub import delete_repo
from fs_test import repo_name
from huggingface_hub.utils import RepositoryNotFoundError

try:
    delete_repo(repo_id=f'{repo_name}/hf_test', repo_type="model")
except RepositoryNotFoundError:
    print("Repository not found, skipped.")
else:
    print("Repository deleted.")
