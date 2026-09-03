# -*- coding: utf-8 -*-
"""飞镖风暴 · Dart Storm —— Streamlit 启动器。

将同目录下的单文件游戏 index.html 嵌入 Streamlit 页面，
可直接部署到 Streamlit Community Cloud (share.streamlit.io)。
本地运行：streamlit run app.py
"""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent
GAME_FILE = ROOT / "index.html"

st.set_page_config(
    page_title="飞镖风暴 · Dart Storm",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- 页面样式：深色街机厅外壳 ----------
st.markdown(
    """
    <style>
      .stApp {
        background:
          radial-gradient(900px 480px at 88% -8%, rgba(255,45,85,.16), transparent 62%),
          radial-gradient(760px 420px at 4% -6%, rgba(64,224,208,.10), transparent 60%),
          radial-gradient(1200px 800px at 50% 120%, rgba(20,26,44,.9), transparent 70%),
          #0a0e1a;
      }
      .block-container { max-width: 1180px; padding-top: 12px; padding-bottom: 28px; }
      #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
      header[data-testid="stHeader"] { background: transparent; }

      /* 报头：左对齐排印 + 右侧按键芯片 */
      .ds-head { display:flex; align-items:flex-end; justify-content:space-between;
        gap:18px; flex-wrap:wrap; padding: 4px 2px 14px; }
      .ds-eyebrow { display:inline-flex; align-items:center; gap:9px;
        font-size:11.5px; letter-spacing:.34em; color:#ff2d55; font-weight:700;
        margin-bottom:7px; }
      .ds-title { margin:0;
        font-family: Impact, Haettenschweiler, "Arial Narrow Bold", "Noto Sans SC", "Microsoft YaHei", sans-serif;
        font-size: clamp(36px, 5vw, 56px); line-height: .95; color:#f2f5ff;
        letter-spacing:.03em; text-shadow: 0 0 26px rgba(255,45,85,.38); }
      .ds-title .en { color:#ff2d55; font-size:.4em; letter-spacing:.36em;
        vertical-align: middle; margin-left:12px; }
      .ds-sub { margin:8px 0 0; color:#93a0c2; font-size:13.5px; letter-spacing:.04em; }
      .ds-chips { display:flex; gap:8px; flex-wrap:wrap; padding-bottom:8px; }
      .ds-chips span { border:1px solid rgba(147,160,194,.35); color:#c6d0ea;
        background: rgba(20,26,44,.72); padding:5px 12px; border-radius:6px;
        font-size:12.5px; letter-spacing:.06em; transition: all .18s ease; }
      .ds-chips span:hover { border-color:#ff2d55; color:#fff;
        box-shadow: 0 0 14px rgba(255,45,85,.4); transform: translateY(-2px); }
      .ds-chips b { color:#ffd23e; font-weight:700; margin-right:2px; }

      /* 游戏舱：给 components.html 的 iframe 包一层边框外壳 */
      div:has(> iframe[title="streamlit_html"]) {
        height: 76vh !important;
        border: 1px solid rgba(255,45,85,.45); border-radius: 12px; padding: 6px;
        background: rgba(10,14,26,.62);
        box-shadow: 0 20px 55px rgba(0,0,0,.55), 0 0 36px rgba(255,45,85,.13);
      }
      iframe[title="streamlit_html"] {
        height: calc(76vh - 14px) !important; width: 100%;
        border-radius: 8px; display: block;
      }

      .ds-hint { display:flex; gap:10px; align-items:center; margin:13px 2px 0;
        color:#93a0c2; font-size:13px; line-height:1.6; }
      .ds-hint .dot { width:8px; height:8px; border-radius:50%; background:#40e0d0;
        box-shadow: 0 0 10px #40e0d0; animation: dsPulse 1.6s ease-in-out infinite; flex:none; }
      @keyframes dsPulse { 50% { opacity:.3; transform: scale(.8); } }
      .ds-hint b { color:#e8ecf8; }

      .ds-foot { margin-top:20px; padding-top:12px; color:#5b6785; font-size:12px;
        border-top:1px solid rgba(91,103,133,.22);
        display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap; }

      [data-testid="stExpander"] { background: rgba(20,26,44,.6);
        border:1px solid rgba(147,160,194,.25); border-radius:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 报头 ----------
st.markdown(
    """
    <div class="ds-head">
      <div>
        <span class="ds-eyebrow">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="10" stroke="#ff2d55" stroke-width="2.4"/>
            <circle cx="12" cy="12" r="5.2" stroke="#ffd23e" stroke-width="2.2"/>
            <circle cx="12" cy="12" r="1.7" fill="#40e0d0"/>
          </svg>
          CANVAS 单文件街机 · STREAMLIT 云版
        </span>
        <h1 class="ds-title">飞镖风暴<span class="en">DART STORM</span></h1>
        <p class="ds-sub">左右闪避落镖 · 擦身触发「好险」连击 · 每 12 秒提速一档 —— 看你能撑几秒</p>
      </div>
      <div class="ds-chips">
        <span><b>← →</b>移动</span>
        <span><b>P</b>暂停</span>
        <span><b>M</b>静音</span>
        <span><b>R</b>重开</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- 游戏本体 ----------
if not GAME_FILE.exists():
    st.error("未找到游戏文件 index.html，请确认它与 app.py 位于同一目录。")
    st.stop()

game_html = GAME_FILE.read_text(encoding="utf-8")

# Streamlit 的 components.html 运行在沙箱 iframe 中（无 allow-same-origin），
# 直接访问 localStorage 会抛异常。注入一个内存版垫片，让最高分功能继续可用；
# 即便垫片注入失败，游戏自身的 try/catch 也保证不会崩溃。
LS_SHIM = (
    "<script>(function(){try{window.localStorage.setItem('__ds_t','1');"
    "window.localStorage.removeItem('__ds_t');}catch(e){var m={};"
    "try{Object.defineProperty(window,'localStorage',{configurable:true,"
    "get:function(){return{getItem:function(k){return Object.prototype."
    "hasOwnProperty.call(m,k)?m[k]:null;},setItem:function(k,v){"
    "m[k]=String(v);},removeItem:function(k){delete m[k];},"
    "clear:function(){m={};}};}});}catch(e2){}}})();</script>"
)
game_html = game_html.replace("<head>", "<head>" + LS_SHIM, 1)

components.html(game_html, height=720, scrolling=False)

st.markdown(
    """
    <div class="ds-hint"><span class="dot"></span>
      <span>首次游玩请先<b>点击一次游戏画面</b>，让键盘焦点进入游戏窗口，
      随后用 <b>← / →</b>（或 A / D）移动。最佳纪录保存在本机浏览器。</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- 说明 ----------
with st.expander("玩法说明 · 本地运行 · 部署到 Streamlit Cloud"):
    st.markdown(
        """
**操作**
- `← / →` 或 `A / D`：左右移动
- `空格 / 回车 / R`：开始 / 重新开始
- `P / Esc`：暂停（切出窗口自动暂停），`M`：静音

**规则**
- 被飞镖击中立即结束；镖尖擦身而过触发「好险」连击加分
- 每 12 秒提速一档；22 秒后出现重型金镖，45 秒后出现旋转漂移镖

**本地运行**
```bash
pip install -r requirements.txt
streamlit run app.py
```

**部署到 Streamlit Cloud**
1. 将本仓库（`app.py`、`index.html`、`requirements.txt`、`.streamlit/`）推送到 GitHub
2. 打开 share.streamlit.io → **New app**
3. Main file path 填 `app.py`，点击 **Deploy**
"""
    )

st.markdown(
    """
    <div class="ds-foot">
      <span>飞镖风暴 · 场景与角色全部由 Canvas 手绘，零外部图片 / 脚本</span>
      <span>STREAMLIT COMMUNITY CLOUD READY</span>
    </div>
    """,
    unsafe_allow_html=True,
)
