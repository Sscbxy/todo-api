from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class TodoItem(Base):
    __tablename__ = "todos"  # 数据库里的表名叫 todos

    # 定义表的列（字段）
    id = Column(Integer, primary_key=True, index=True)  # 主键，自动递增
    title = Column(String, index=True)                  # 标题，文字类型
    done = Column(Boolean, default=False)  
    
    # 新增这一行：标记是否被删除，默认是 False（没删）
    is_deleted = Column(Boolean, default=False)              # 是否完成，默认 False