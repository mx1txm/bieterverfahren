# Bieterverfahren

- Prepare dev environment with Python 3.11 and poetry:
```
curl https://pyenv.run | bash
pyenv install 3.11.1
pyenv local 3.11.1
curl -sSL https://install.python-poetry.org | python3 -
```

- Install pre-commit from https://pre-commit.com/
- Install dependencies with `poetry install`
- Prepare DB with `poetry run ./manage.py migrate`
- Prepare Tailwind with `poetry run ./manage.py tailwind install`
- During dev, keep Tailwind compiler running in another tab: `poetry run ./manage.py tailwind start`
