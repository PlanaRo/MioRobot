# 进阶

------

提醒：请务必开启python的类型检查，这有利于减少错误和编写规范的代码。此框架很多内容依赖于类型。



## 插件编写

所有插件都放在Plugins文件夹中

插件的结构应为

```
Plugin  插件文件夹
   ├─plugin_1   插件1
   │   ├─__init__.py    初始化文件
   │   ├─config.json  插件信息文件
   │   └─other.py   其他文件
   └─plugin_2   插件1
      ├─__init__.py 初始化文件
      ├─config.json   插件信息文件
      └─other.py    其他文件
```

所有的插件都必须包含 **__ init __.py**,该文件可以为空

原理：插件加载器将会扫描Plugins目录下的所有文件，文件中如果继承了插件类，将会将继承的类进行注册

测试插件示例

```python
from functools import singledispatchmethod
from Models.Context.GroupMessageContext import GroupMessageContext
from Plugin import Plugin


class MyPlugin(Plugin):
    def init(self):
        pass

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):

        if context.Event.Message[0] == "测试":
            await context.Command.Reply("测试成功")
    
    @run.register
    async def _(self, context: PrivateMessageContext):

        if context.Event.Message[0] == "测试":
            await context.Command.Reply("测试成功")

    def dispose(self) -> None:
        pass

```

插件配置文件

```json
{
    "name": "test",
    "display_name" : "test",
    "version": "1.0.0",
    "description": "test",
    "author":"sansan",
    "setting":{
        "enable": true,
        "priority": 0,
        "event":["GroupMessage"],
        "hide":false
    },
    "developer_setting": {}
}
```

### 流程

1，首先我们需要导入插件的基类`Plugin`,并建立一个属于自己的插件例如`MyPlugin`

```python
from functools import singledispatchmethod
from Models.Context.GroupMessageContext import GroupMessageContext
from Plugin import Plugin

class MyPlugin(Plugin):
    pass

```



2，实现抽象方法

对于一个插件，你应该实现三个方法，分别是`init`，`run`，`dispose`

````python
class MyPlugin(Plugin):
    def init(self):
        pass

    @singledispatchmethod
    async def run(self, context: GroupMessageContext):
        pass

    def dispose(self) -> None:
        pass
````

init方法：

用于初始化配置，将会在插件实例化时运行。不建议重写父类的构造函数，如果必须使用，请使用

```python
class MyPlugin(Plugin):
    def __init__(self):
        super().__init__
        //other code
```

dispose方法：

用于释放资源，对于有缓存资源的插件，必须重写此方法，该方法将会在必要时进行调用

```python
def dispose(self) -> None:
    pass
```

run方法：

注意：run方法是异步的

插件运行的主要方法，每次消息触发时都会调用此方法

context则为消息的上下文，通过消息上下文，你可以获取到消息数据，和进行消息回复，详细可以查看对应消息的上下文类

run方法应该使用`@singledispatchmethod`装饰器,该装饰器将会根据传入参数的类型来进行任务分配，以此来处理不同的消息

例子：

```python
@singledispatchmethod
async def run(self, context: GroupMessageContext):
	#处理群消息
	if context.Event.Message[0] == "测试":
    	await context.Command.Reply("测试成功")
    
@run.register
async def _(self, context: PrivateMessageContext):
    #处理私聊消息
	if context.Event.Message[0] == "测试":
    	await context.Command.Reply("测试成功")
```