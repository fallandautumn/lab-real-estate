import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Integer,Float
from sqlalchemy.orm import sessionmaker, declarative_base
import time
import re
import os
from dotenv import load_dotenv
load_dotenv()

# ---設定---
DATABASE_URL = os.getenv("DATABASE_URL")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

Base = declarative_base()

class LabProperty(Base):
    __tablename__ = "properties_integration_lab"
    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String)
    building_type = Column(String)
    price = Column(Integer,index=True)
    admin_num = Column(Integer)
    address = Column(String)
    age = Column(Integer)
    madori = Column(String)
    menseki =Column(Float)
    room_floor = Column(Integer)
    building_floor = Column(Integer)

# ---補助関数---
def safe_extract(parent, selector):
    target = parent.select_one(selector)
    return target.get_text(strip=True) if target else "不明"

def cleaning_lab(raw_data):
    if not raw_data:
        return 0
    if "新築" in str(raw_data):
        return 0
    match = re.search(r'(\d+\.?\d*)', str(raw_data))
    if match:
        val = float(match.group(1))        
        return val*10000 if "万円" in str(raw_data) else val
    return 0

# ---メインロジック---
def scr_for_DB(target_url,max_pages=3):
     # 開発中は構造変更が多いため、毎回リセットする
    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    total = 0

    print(f"収集開始{target_url}")
    for page in range(1,max_pages+1):
        url = f"{target_url}?page={page}"
        print(f"---{page}ページ目を処理中---")
        
       

        try:
            res = requests.get(url, headers=HEADERS)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select('.cassetteitem')
            count = 0

            for item in items:
                raw_building_type = safe_extract(item,'.cassetteitem_content-label ')
                raw_title = safe_extract(item,'.cassetteitem_content-title')
                raw_address = safe_extract(item,'.cassetteitem_detail-col1')
                # 築年数・総階数の取得
                detail_col3 = item.select_one('.cassetteitem_detail-col3')
                divs = detail_col3.find_all('div')
                raw_age ="0"
                raw_building_floor = "0"

                for d in divs:
                    text = d.get_text(strip=True)
                    if "築" in text:raw_age = text
                    elif "階建" in text:raw_building_floor = text
                    
                age = cleaning_lab(raw_age)
                building_floor = cleaning_lab(raw_building_floor)

                # 部屋ごとのループ
                rooms = item.select('.js-cassette_link')
                for room in rooms:
                    prop = LabProperty(
                        title = raw_title,
                        building_type = raw_building_type,
                        price = cleaning_lab(safe_extract(room,'.cassetteitem_other-emphasis')),
                        admin_num = cleaning_lab(safe_extract(room,'.cassetteitem_price--administration')),
                        madori = safe_extract(room,'.cassetteitem_madori'),
                        menseki = cleaning_lab(safe_extract(room,'.cassetteitem_menseki')),
                        age = age,
                        room_floor = cleaning_lab(room.find_all('td')[2].get_text(strip=True) if len(room.find_all('td')) > 2 else '0'),
                        building_floor = building_floor,
                        address = raw_address,
                    )
                    session.add(prop)
                    count+=1
            total+=count
            session.commit()
            time.sleep(1)

            print(f"{count}件のデータがDBに格納されました。")

        except Exception as e:
            print(f"{page}目でエラー発生{e}")
            session.rollback()
        finally:
            session.close()
    print("-"*20)
    print(f"合計:{total}件のデータがDBに格納されました")

if __name__ == "__main__":
    DEFAULT_URL = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/'
    scr_for_DB(DEFAULT_URL)
