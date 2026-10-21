from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from typing import Optional  # 记得在文件开头加上这个导入
import models

# 1. 告诉程序：根据 models.py 的定义，去数据库里创建表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. 接收数据的模板（和之前一样）
class TodoCreate(BaseModel):
    title: str
    done: bool = False

# 3. 依赖项：每次请求时打开数据库，请求结束自动关闭
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. 根路径（测试用）
@app.get("/")
def root():
    return {"message": "数据库已连接"}

# 5. 创建待办事项，并存入数据库
@app.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    # 把接收到的数据，变成一个数据库对象
    db_todo = models.TodoItem(title=todo.title, done=todo.done)
    # 存进数据库并刷新
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    # 返回存入后的结果（这个时候就有真实的 id 了）
    return db_todo

# 6. 新增一个接口：查询所有待办事项
@app.get("/todos")
def read_todos(done: Optional[bool] = None, db: Session = Depends(get_db)):
    # 1. 先建立一个基础查询：准备查 todos 表里的所有东西
    # 基础查询：只查没被软删除的
    query = db.query(models.TodoItem).filter(models.TodoItem.is_deleted == False)

    # 2. 如果前端传了 done 参数（不是 None），就加上过滤条件
    if done is not None:
        query = query.filter(models.TodoItem.done == done)

    # 3. 执行查询，把结果全部拿出来
    todos = query.all()
    return todos

# 7. “删除”接口 这里的 {item_id} 就是你在网址里传过来的那个数字
@app.delete("/todos/{item_id}")
def delete_todo(item_id: int, db: Session = Depends(get_db)):
    
    # 1. 去数据库里找，有没有人叫这个名字（id == item_id）
    # .first() 意思是：把找到的第一个拿出来（因为没有重复的 id，所以第一个就是唯一一个）
    # 找数据的时候，不仅要 id 对得上，而且要“没被删过”
    todo = db.query(models.TodoItem).filter(models.TodoItem.id == item_id, models.TodoItem.is_deleted == False ).first()
    
    # 2. 如果没找到（比如你传了个 999，但数据库里只有 1 和 2），就报个错
    if todo is None:
        return {"error": "找不到这个待办事项"}
    
    # 3. 如果找到了，就把它扔掉
     # 【核心变化】这里不再用 db.delete(todo)
    # 而是把它标记为已删除
    todo.is_deleted = True 
    
    # 4. 存档生效
    db.commit()
    
    # 5. 告诉前端：我删掉了
    return {"message": f"成功删除了 id 为 {item_id} 的待办事项（软删除）"}

# 8.  “修改”接口
@app.put("/todos/{item_id}")
def update_todo(item_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    # 1. 按照 id 去数据库找，找找有没有这个待办事项
    db_todo = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    
    # 2. 如果没找到，直接返回错误提示
    if db_todo is None:
        return {"error": "找不到这个待办事项"}
    
    # 3. 找到了，开始修改！把旧数据替换成新传来的数据
    db_todo.title = todo.title
    db_todo.done = todo.done
    
    # 4. 提交并刷新
    db.commit()
    db.refresh(db_todo)
    
    # 5. 把修改后的结果返回给前端
    return db_todo

# 10. "恢复"接口 (软删除的后悔药)
@app.put("/todos/{item_id}/restore")
def restore_todo(item_id: int, db: Session = Depends(get_db)):
    # 1. 去找这个 id 的数据（注意：这里【不需要】过滤 is_deleted，因为我们要找的就是被删掉的！）
    db_todo = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    
    # 2. 如果连这个 id 都根本没有过，那就报错
    if db_todo is None:
        return {"error": "这个待办事项从来没有存在过"}
    
    # 3. 如果找到了，不管它现在是什么状态，直接强行把它标记为“未删除”
    db_todo.is_deleted = False
    
    # 4. 提交保存
    db.commit()
    db.refresh(db_todo)
    
    return {"message": f"成功恢复了 id 为 {item_id} 的待办事项", "data": db_todo}