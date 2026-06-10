# 聊天记录导出指南

## 微信聊天记录

### 推荐工具

| 工具 | 平台 | 导出格式 | 链接 |
|------|------|---------|------|
| **WeChatMsg** | Windows/Mac | txt/html/csv/json | github.com/LC044/WeChatMsg |
| **留痕** | Windows | txt/html | — |
| **PyWxDump** | Windows/Mac/Linux | json/csv | github.com/xaoyaoo/PyWxDump |

### 导出步骤（以 WeChatMsg 为例）

1. 下载并安装 WeChatMsg
2. 登录微信（PC 端已登录即可）
3. 选择联系人 → 导出聊天记录
4. 选择格式：推荐 **txt** 或 **csv**
5. 保存到本地

### 导出后

把文件丢进 `nows/{slug}/inbox/`，运行 `/now-update {slug}`。

---

## QQ 聊天记录

### 方法 1：QQ 内置导出

1. 打开 QQ 聊天窗口
2. 点击右上角「···」→「导出聊天记录」
3. 选择 txt 或 mht 格式
4. 保存

### 方法 2：合并转发（推荐）

1. 在手机 QQ 选中聊天记录
2. 点击「合并转发」
3. 发到电脑端
4. 在电脑端复制全部内容
5. 使用 `/now-feed {slug}` 粘贴

---

## 手机截图

如果以上方式都不方便：

1. 在手机上截取聊天记录（多张截图）
2. 传到电脑
3. 丢进 `nows/{slug}/inbox/`
4. 运行 `/now-update {slug}`

Skill 会自动用图像识别提取文字。

---

## 社交媒体

### 微信朋友圈
- 截图保存到 inbox

### 微博/小红书/Instagram
- 截图或复制文字
- 使用 `/now-feed {slug}` 粘贴

---

## 主观描述

不需要任何文件。直接在创建时告诉我或使用 `/now-feed {slug}` 口述：

```
/baby-feed
最近ta好像特别忙，回消息变慢了，但见面的时候还是很热情。
ta最近一直在提想换工作的事，感觉对这个很焦虑。
```
