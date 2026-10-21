from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 指定数据库文件名为 todo.db，它会自动生成在你的文件夹里
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话工厂（用来执行增删改查）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建一个基类，后面所有的数据模型都要继承它
Base = declarative_base()