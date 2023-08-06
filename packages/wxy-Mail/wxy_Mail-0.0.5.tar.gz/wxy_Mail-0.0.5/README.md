# wxy-Mail

## 依赖
```
twine
setuptools
```

## 使用
```python
from wxy_Mail import Mail

mail=Mail('user','pwd')
mail.add_receivers(['xxx@yy.com','aaa@bb.com'])
mail.add_subject('邮件主题')
mail.add_content('plain','this is content')
mail.add_attachment(["C:\\Users\\test.pdf","D:\\Users\\abc.png"])
mail.send()
```

