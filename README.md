# Pocket48
-----------------------------------
@mail: ssr@yinheng.xyz
#### 部分逻辑参考[chinshin/CQBot_hzx](https://github.com/chinshin/CQBot_hzx)
### 口袋48APP 监控(Python3)，该项目实现以下功能:
* 成员房间消息监控
* 摩点监控
* 支持多账号登录
* 支持多成员监控
* mongodb存放数据
* 通过酷Q向群和私人发送消息

## Update Log
--------------------------
#### 2019.04.29 Ver 1.2.0

增加摩点监控功能

#### 2019.04.29 Ver 1.1.1

删除botserver,修复已知bug

#### 2019.04.23 Ver 1.1.0

修复消息部分格式化bug，参考chinshin/CQBot_hzx

#### 2019.04.22 Ver 1.0.0

1.增加计划任务支持，支持多偶像监控

2.增加token管理，支持多账号登录

3.改善项目结构

#### 2019.04.19 Ver.0.2 

增加对酷Q机器人的支持

#### 2019.04.18 Ver.0.1
实现基本功能

## 使用方法
--------------------------
1. win server: 安装酷Q Pro，进入开发者模式；
2. 把 `io.github.richardchien.coolqhttpapi.cpk`([release地址](https://github.com/richardchien/coolq-http-api/releases)) 加入酷Q文件夹下app文件夹，重启酷Q并在应用管理中打开该http-api；
3. 安装`cqhttp` 和 `apscheduler`，终端输入：`pip install cqhttp` 和 `pip install apscheduler `，环境为py2的使用pip3安装；
4. 开启`mongodb`本地服务器,开启酷Q；
5. 修改`main.py`中的用户名、密码、偶像名、摩点项目编号；
6. 修改`cqapi.py`中的QQ号；
7. 开启`main.py`

## 方法说明
--------------------------
|方法|功能|参数|
| :----------: | :-----------:|:-----------:|
| login   | 登录  | 手机，密码 |
| searchroom   |  查询指定成员roomId  | 成员全名 |
| chatroom   |  查询成员房间消息  | roomId,ownerId |
| livedetail   |  查询直播详情  | liveId |
| orders   | 获取摩点订单消息  | sort_by: 排序方式 1：支付时间倒序 0：下单时间倒序 int page: 页码 int |
| rank   |  获取摩点集资排名  | type: 排行榜类型 1：金额榜 2：打卡榜 int page: 页码 int|
| detail   |  获取摩点项目详情  | self |
| call   |  QQ事件处理  | 事件内容 |

## 数据库
-------------------------------------------
### 本项目使用MongoDB作为数据库：
|数据库|表名|数据|
| :----------: | :-----------:| :-----------:|
| Poket48   | dbtoken | 所有登录账号token |
| Poket48   |  { room_id1 }  | 成员1的房间消息 |
| Poket48   |  { room_id2 }  | 成员2的房间消息 |
| modian   |  { pro_id }  | 摩点项目pro_id的订单 |

## LICENSE

GPL-3.0-only

