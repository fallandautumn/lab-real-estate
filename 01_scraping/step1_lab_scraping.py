import requests
from bs4 import BeautifulSoup
import time

TARGET_URL = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

def safe_extract(parent, selector):
    target = parent.select_one(selector)
    return target.get_text(strip=True) if target else "0"

def run_lab():
    print("実験開始： phase 1 (pure scaping)")

    print(f"リクエスト送信中...: {TARGET_URL}")
    res = requests.get(TARGET_URL,headers=HEADERS)
    res.encoding = 'utf-8'

    if res.status_code != 200:
        print(f"失敗：ステータスコード{res.status_code}")
        return
    
    soup = BeautifulSoup(res.text, 'html.parser')

    print("要素を探索中...")
    all_properties = []
    items = soup.select('.cassetteitem')
    if not items:
        print("物件要素(.cassetteitem)が見つかりません。サイト構造が変わった可能性があります。")
        return

    for i, item in enumerate(items):
        raw_title = item.select_one('.cassetteitem_content-title').text
        raw_address = item.select_one('.cassetteitem_detail-col1').text
        raw_price = item.select_one('.cassetteitem_other-emphasis').text
        raw_admin = safe_extract(item,'.cassetteitem_price--administration')

        detail_col3 = item.select_one('.cassetteitem_detail-col3')
        divs = detail_col3.find_all('div')

        raw_age = divs[0].text if len(divs) > 0 else "N/A"
        raw_floor = divs[1].text if len(divs) > 1 else "N/A"
        raw_madori = item.select_one('.cassetteitem_madori').text
        raw_menseki = item.select_one('.cassetteitem_menseki').text

        property_dict = {
            "title": raw_title.strip(),
            "address": raw_address.strip(),
            "price": raw_price.strip(),
            "admin": raw_admin.strip(),
            "age": raw_age.strip(),
            "floor": raw_floor.strip(),
            "madori": raw_madori.strip(),
            "menseki": raw_menseki.strip()
        }

        all_properties.append(property_dict)


    print(f" 全 {len(all_properties)}件のデータ抽出が完了しました。")

if __name__ == "__main__":
    run_lab()
