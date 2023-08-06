## 搜狗分词工具
### 举例
#### 使用方式 command-line

$ sougou_fenci 武汉市长江大桥
-> 
武汉市 n
长江 n
大桥 n


``` python
import sougou_fenci
resp = sougoou_fenci.get_fenci("武汉市长江大桥")
for result_item in resp.result:
    print(row_format.format(result_item[0], result_item[1]))
# 武汉市         n
# 长江         n
# 大桥         n
```