# Cryptocurrency Data Ingestion

[![Amazon AWS](https://img.shields.io/badge/-Amazon%20AWS-orange)](https://aws.amazon.com/pt/free/) [![Zappa](https://img.shields.io/badge/-Zappa-black)](https://github.com/zappa/Zappa)

Setting up local AWS credentials:
```sh
pip install awscli
aws configure
```

Running locally with Zappa:
```sh
make init
source .venv/bin/activate
zappa deploy
```

Testing:
```sh
poetry run python -m pytest
python -m pytest
python -m pytest {folder}/{file}.py
```