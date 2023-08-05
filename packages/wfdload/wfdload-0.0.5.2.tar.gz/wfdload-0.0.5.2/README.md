# wfdload

## 概要
wavetoneの独自フォーマットであるwfdをpythonで使える形にします。

## インストール
```sh
$ pip install wfdload
```


## 使い方
### スペクトルステレオ
```python
>>> from wfdload import WFD
>>> w = WFD("./test.wfd")
>>> w.spectrumStereo
```

### コード
```python
>>> from wfdload import WFD
>>> w = WFD("./test.wfd")
>>> time = 1
>>> w.chordresult.split(time)
```
timeは実際の秒数です