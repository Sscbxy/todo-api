# Todo API (待办事项后端接口)

基于 Python + FastAPI + SQLite + SQLAlchemy 开发的待办事项 RESTful API 项目，完整实现了数据的增删改查（CRUD）以及企业级的软删除恢复机制。

## 🛠 技术栈
- **Web 框架**: FastAPI
- **数据校验**: Pydantic
- **ORM 框架**: SQLAlchemy
- **数据库**: SQLite
- **包管理器**: uv

## ✨ 核心功能
- [x] **创建待办事项 (POST)**：接收前端 JSON 数据并存入数据库。
- [x] **获取列表 (GET)**：支持通过 `?done=true/false` 查询参数进行条件过滤。
- [x] **修改事项 (PUT)**：根据 ID 更新指定待办事项的标题和完成状态。
- [x] **软删除 (DELETE)**：不物理销毁数据，而是将 `is_deleted` 标记为 True。
- [x] **恢复删除 (PUT)**：将误删的数据状态恢复为正常可用。

## 🚀 本地运行指南
1. 克隆项目：`git clone https://github.com/Sscbxy/todo-api.git`
2. 安装依赖：`uv sync`
3. 启动服务：`uv run fastapi dev`
4. 打开浏览器访问自动生成的交互式接口文档：`http://127.0.0.1:8000/docs`