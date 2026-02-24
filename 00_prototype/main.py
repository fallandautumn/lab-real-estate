import requests
from bs4 import BeautifulSoup
from step1_2_integration_lab import scr_for_DB
from multiple_regression import run_multiple_regression


target_districts = {
    "新宿":'https://suumo.jp/chintai/tokyo/sc_shinjuku/'
}

def run_mission():
    print("autocrawler start")
    for name,url in target_districts.items():
        print(f"targeting:{name}")
    
        scr_for_DB(url,2) #スクレイピングするページ数指定
    run_multiple_regression()
    print("accomplished.")



if __name__ == "__main__":
    run_mission()