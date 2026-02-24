from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

             # "postgresql://ユーザー名:パスワード@ホスト:ポート/データベース名"
DATABASE_URL = os.getenv("DATABASE_URL")

# 「pythonの世界」と「DBの世界」をつなぐ物理的なトンネルがengine
engine = create_engine(DATABASE_URL)
# 「pythonのクラス(Property)」と「DBのテーブル(properties)」を紐付けるための接着剤
Base = declarative_base()

class Property(Base):
    __tablename__ = 'properties_lab'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    price = Column(String)
    address = Column(String)
    age = Column(String)
    menseki = Column(String)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

def run_db_lab():
    print("実験開始； Phase 2 (Database Mastery)")

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        test_item = Property(
            title="実験用：神楽坂レジデンス",
            price="15.5万円",
            address="東京都新宿区山吹町",
            age="築10年",
            menseki="25.5m2"
            )
        
        session.add(test_item)
        session.commit()
        print("DBへの保存に成功しました")

        print("保存されたデータを再取得中")
        saved_item = session.query(Property).first()
        print(f"取得結果：{saved_item.title} / {saved_item.price}")

    except Exception as e:
        print(f"エラー発生{e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    run_db_lab()

        