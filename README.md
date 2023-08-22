# guag-khlbot 点歌表情包机器人


![github stars](https://img.shields.io/github/stars/zhubin12134/guag-khlbot?style=social)

Kyouka is a simple and powerful music bot for [KOOK](https://www.kookapp.cn/), it is easy to use and develop.


## Contents

- [声明](#声明)
- [特性](#特性)
- [依赖](#依赖)
- [安装与部署](#安装与部署)
  - [基于docker部署](#基于docker部署)
  - [基于源码部署](#基于源码部署)
- [使用指南](#使用指南)
  - [快速上手](#快速上手)
  - [操作指令](#操作指令)
- [开发](#开发)
  - [贡献源码](#贡献源码)
  - [许可协议](#许可协议)
- [社区](#社区)
- [致谢](#致谢)

## 声明

本项目仅供Python爱好者学习使用, 若您基于本项目进行商业行为, 您将承担所有的法律责任, 作者与其他贡献者将不承担任何责任.  
最后, 如有侵权, 请联系我删除该项目.  

## 特性

+ 多平台/多架构支持
+ 全异步设计
+ 容器化服务

## 依赖

+ ffmpeg, 如果你基于源码部署,需要ffmpeg
+ Python >= 3.9, 推荐使用docker

## 安装与部署

### 基于docker部署

基于docker部署示例


1. 确认你的docker是否已经就绪

```bash
docker version
```

2. 拉取[guag-khlbot 点歌表情包机器人 源码](https://github.com/zhubin12134/guag-khlbot.git)

```bash
git clone https://github.com/zhubin12134/guag-khlbot.git
```

3. 构建镜像

```bash
cd guag-khlbot
docker build -t guag-khlbot .
```

4. 配置 `.env` 文件.

> 警告: 不要在配置项所在的行末添加任何无用的字符(包括但不限于 空格, 注释), 否则会导致Json解析失败

```bash
# 你的机器人的 token
TOKEN=1/MTY1OTU=/pglPBi9LPVe/aaaaaaaa==

# 默认绑定的语音频道ID
CHANNEL=2559449076697969
```

5. 创建本地music和log挂载目录,后续音乐可以直接传到music目录里

```bash
mkdir music
mkdir log
```

6. 创建机器人镜像的容器
直接使用docker-compose

```bash
docker-compose up -d
```
或者直接部署
```bash
docker run --name guag_khlbot -v log:/app/log -v .env:/app/.env -v music:/app/music --restart always -d guag-khlbot
```

7. 此时你的机器人已开始运行, 在你的频道中发送 `+ping` 命令, 如果 guag回复你消息了, 那么代表你的部署已经完成! 请尽情享用
> 警告: 请提前确定你已经授予了你的机器人阅读和发送消息的权限

### 基于源码部署

略

## 使用指南

### 快速上手

在你的频道发送 `+六花` 命令,获取帮助
前缀可以更改,更改config/common.py中的register_startswith值即可,双引号不可以省略,缩进也不能修改

```base
register_startswith: str = "+"
``` 

### 操作指令
使用时应该是 前缀 + 指令,例如 来 应该为 `+来`
1. `鲁迅说 不是我说的` :鲁迅表情包
2. `麦克说 不是我说的` :麦克阿瑟表情包
3. `爬 @用户` :爬表情包
4. `来` :绑定放歌频道
5. `本地 歌名` :需要先绑定再点歌
6. `切歌` :切歌
7. `列表` :查看播放列表
8. `本地列表` :查看本地歌曲,默认显示15条
9. `清空歌单` :清空播放列表
10. `ping` :验证存活

todo:
各大主流音乐平台播放

## 开发
### 贡献源码
- 使用 issue 进行记录  
通过创建 issue 来提出新功能请求, 反馈 BUG 或提出问题, 这也是与此项目开发者以及其他对该问题感兴趣的人建立联系的一个好方法

- 更换代码工作区  
通俗地说，你应该 fork 这个仓库，在你自己 fork 的仓库中进行修改，然后提交一个PR, 并且所有的 commit message 应该满足 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)

### 许可协议
本项目是根据 [MIT 许可协议](./LICENSE)的条款进行授权的


## 致谢
本项目参考XCWQW1的思路 [kookbot2](https://github.com/XCWQW1/kookbot2)

播放连接为hank999的[khl-voice-API](https://github.com/Knoooooooow/khl-voice-API.git)

联系作者: [戳这里](https://kook.top/94E6PE)
