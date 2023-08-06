# Cipher Tools
This is a python library that contains some tools for making ciphers.
In was originaly made of use at a childrens workshop at PyCon UK 2019.

## Installation
Run the following to install:
```python
pip install cipher_tools
```

## Usage
### Shift
Shift some text by an arbitrary amount. Text case is preserved.

Code:
```python
from cipher_tools import shift

shifted_text = shift("AbCdEfgYZ", 2)
print(shifted_text)
```
Output:
```
CdEfGhiAB
```
### Rot13
You can encrypt / decrypt text using rot13.

Code:
```python
from cipher_tools import rot13

# Apply Rot13 to a phrase
cipher_text = rot13("Hello, World!")
print(cipher_text)
```
Output:
```
Uryyb, Jbeyq!
```

Code:
```python
from cipher_tools import rot13

# Decrtpt the text
plain_text = rot13("Uryyb, Jbeyq!")
print(plain_text)
```
Output:
```
Hello, World!
```


