# Zappa Bot Manage

### How to Create a New Release
```bash
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
twine upload --skip-existing dist/*
```


### To Do
- [x] Repo Name
  - `zappa_manage`
- [x] Figure out how to publish to `edX.org` repo
  - Change url in `setup.py`
- [x] Ask Cory about ...
  - `zappa_manage/tests/` : Is it necessary? If so, here's the [guide](https://python-packaging.readthedocs.io/en/latest/testing.html). Otherwise, delete the directory.
    - No need for tests at the moment.
  - `bin/` : Does this have CLI usage? If so, here's the [guide](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html). Otherwise, delete the repository.
    - It does have cli usage since it's used when deploying lambdas envs in GoCD.
