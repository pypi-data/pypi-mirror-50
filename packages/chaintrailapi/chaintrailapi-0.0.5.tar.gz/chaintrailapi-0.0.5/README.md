# Chaintrail API Wrapper

Installation
```
pip3 install chaintrailapi
```


Import and use the package as demonstrated in `example.py` below:
```python
from chaintrailapi import Account

uuid = Account.uuid()
account = Account('0x7f5f79c034e9781c03c4b4412e1f99ae9b413658')

print('UUID response: {}'.format(uuid))
print('Info response: {}'.format(account.info()))
```


Be sure to the `CHAINTRAIL_BASE_URL` environment variable before running `example.py` as follows:
```bash
export CHAINTRAIL_BASE_URL=https://httpbin.org
python3 example.py
```
