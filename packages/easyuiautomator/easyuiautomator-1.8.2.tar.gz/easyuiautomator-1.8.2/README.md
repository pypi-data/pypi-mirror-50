# easyuiautomator

#### 介绍
Easyuiautomator是基于uiautomator开发一款底层驱动框架，用于操作android手机界面，进行功能性测试，主要分为两部分：
* Easyuiautomator python client 远程操作api
* bootstrap    

#### 软件架构
软件架构说明


#### 安装教程

1. xxxx
2. xxxx
3. xxxx

#### 使用说明

# 连接手机
```
Driver.connect_device() # 默认连接adb devices显示的第一个手机
Driver.connect_device(deivce_id, port) # 通过端口连接指定手机
```
# 打开调试模式

```
Driver.set_debug(True) # 打开底层调试开关，可追踪代码运行轨迹
```

# 查找元素

find_element\_by\_'模式'

模式分为：
* id
* name
* class_name
* accessibility_id
* xpath
* uiautomator

# 动作类型

* flick
* scrollTo
* drag_and_drop
* tap
* swipe

#### 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


#### 码云特技

1. 使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2. 码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3. 你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4. [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5. 码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6. 码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)