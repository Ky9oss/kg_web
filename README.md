# Web 渗透工具
这里记录了我自己的一些web渗透小脚本，目前主要有：
- dirbruter.py: 网页目录暴力破解  
- passbruter.py: 网页登录表单暴力破解  
- rubbing.py: 拓印开源web框架（如wordpress）  

# 技术回顾
## requests库
用于请求网页，使用Session对象便于管理Cookie，使得session之后提交的表单都会使用已经获取了的Cookie  
## lxml库
使用etree解析html。  
- 各种类型的输入都是`<input ...>`  
- HTML规范要求name属性是必须的  

