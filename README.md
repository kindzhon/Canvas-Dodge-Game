# 飞镖风暴 · Dart Storm（Streamlit 版）

一个纯 Canvas 手绘的单文件躲避小游戏：左右方向键控制小人闪避从天而落的飞镖，
擦身加分、逐档提速、粒子爆裂与屏幕震动一应俱全。现已封装为可直接部署到
[Streamlit Community Cloud](https://share.streamlit.io) 的应用。

## 文件结构

| 文件 / 目录 | 作用 |
| --- | --- |
| `app.py` | Streamlit 入口：读取并把 `index.html` 嵌入页面 |
| `index.html` | 游戏本体（单文件，无任何外部图片 / 脚本） |
| `requirements.txt` | 依赖清单（仅 `streamlit`） |
| `.streamlit/config.toml` | 深色主题与页面配置 |

## 本地运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

浏览器自动打开 `http://localhost:8501` 即可游玩。

## 部署到 Streamlit Cloud

1. 将本仓库推送到 GitHub（确保包含上表中的 4 个文件 / 目录）
2. 打开 [share.streamlit.io](https://share.streamlit.io)，用 GitHub 账号登录
3. 点击 **New app**：
   - Repository：选择你的仓库
   - Branch：`main`
   - Main file path：`app.py`
4. 点击 **Deploy**，等待 1–2 分钟即可在线游玩

> 提示：Streamlit 会将游戏放进 iframe 中运行，首次游玩请先**点击一次游戏画面**，
> 让键盘焦点进入游戏窗口，方向键才会生效。

## 玩法速览

- `← / →` 或 `A / D`：左右移动
- `空格 / 回车 / R`：开始 / 重新开始
- `P / Esc`：暂停，`M`：静音
- 被飞镖击中即结束；镖尖擦身触发「好险」连击加分；每 12 秒提速一档
