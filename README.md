# Browser Agent

一个用于展示 AI Agent、系统设计与工程能力的 Browser Agent 初版骨架项目。

## 项目简介

这个项目不是“让模型直接写 Playwright 脚本”的网页自动化 Demo，而是把网页环境抽象成一个可规划、可约束、可恢复的状态机式 Agent 系统。MVP 重点放在清晰的模块边界、受控工具调用、页面压缩表示和可测试性。

## 核心设计理念

- LLM 只负责高层决策，不直接生成任意浏览器脚本
- 所有浏览器动作必须经过结构化 tool registry
- 页面先做压缩快照，再交给 planner
- 主循环显式保留 observe → plan → act → reflect
- 状态、历史、日志、安全策略统一管理

## 目录结构说明

- `app/agent`: orchestrator、planner、critic 及其模型
- `app/browser`: Playwright runtime、observer、snapshot、element indexing
- `app/tools`: tool base、registry、navigation / interaction / extraction tools
- `app/memory`: state、history、store helpers
- `app/llm`: client abstraction、schemas、parser
- `app/safety`: policies and guardrails
- `app/utils`: logging, retry, serialization
- `tests`: planner、snapshot、registry、end-to-end skeleton tests

## MVP 范围

当前初版支持的目标：

- open page and browse
- search information
- extract structured content
- complete simple multi-step page tasks
- produce a final report

当前明确不做：

- login
- payment
- file upload
- CAPTCHA
- complex iframes
- drag-and-drop
- high-risk submit actions by default

## 快速开始

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
playwright install
pytest
browser-agent run "Find product listings for wireless mouse"
```

## Future Work

- real LLM provider integration
- multi-agent planning and delegated subtasks
- visual grounding mode
- benchmark and evaluation harness
- richer recovery strategies and persistent memory

## 为什么这不是普通网页脚本

普通网页脚本通常直接绑定 selector 和固定流程；这个项目则把浏览器环境抽象成状态、快照、结构化动作和反思信号。即使当前只是 MVP 骨架，后续也能自然扩展到多 Agent、视觉输入、安全分级和 benchmark 场景，而不需要推倒重写。

