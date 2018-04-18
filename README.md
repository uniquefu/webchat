此项目难点是如何实时接收消息

webchat主要流程：
a.客户端登录后，实时接收消息，发送消息；
b.服务器收到消息，判断是个人聊天还是组聊天，并写入队列；

webchat程序主要实现个人实时聊天，后续扩展组聊天及丰富个人聊天未读消息统计；主要是html的jquery操作。

![image](https://github.com/uniquefu/webchat/blob/master/webchat界面.png)
