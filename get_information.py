from dotenv import load_dotenv
import os
import pandas as pd
import requests
import json

def get_information(submit_json):
  csv_file = "exercise_3/data/cleaned_top_200_rows.csv"

  submit_json = json.dumps(submit_json)

  def get_img(keyword):
    base_url = "http://apis.data.go.kr/B551011/KorService1/searchKeyword1"
    api_key = os.getenv("DATA_API_KEY")   # .env 파일에 각자 API 추가

    url = base_url
    params = {
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "serviceKey": api_key,
        "arrange": "A",
        "contentTypeId": 32,
        "_type": "json",
        "keyword": keyword
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
      data = response.json()  # JSON 형식으로 변환
      items = data.get('response', {}).get('body', {}).get('items', {}).get('item', [])
      
      for item in items:
        first_image = item.get('firstimage')
        if first_image:
          return first_image
      
      return "No image found"
    else:
      print(f"Error: {response.status_code}")

  def search_information(csv_file, ans_json):
    
    df = pd.read_csv(csv_file)

    
    # JSON 문자열을 Python 객체로 변환
    dict_json = json.loads(ans_json)
  #여기------------기------------기------------기------------
    hotel_ids = dict_json.get('hotel_id', []) 
    introduction = dict_json.get('introduction', [])
    
    # csv파일 hotel_id가 문자열 형식인지 확인 및 변환
    df['명칭'] = df['명칭'].astype(str)
    
    result = []
    
    for rec_hotel_id in hotel_ids:
      # hotel_id = rec["hotel_id"]  #hotel_id 하나씩
      row = df[df['명칭'] == rec_hotel_id]

      if not row.empty:
        # JSON 형식으로 변환
        row_json = row.to_json(orient='records')
      
        # JSON 문자열을 파싱하여 출력
        row_data = json.loads(row_json)
        
        for hotel_info in row_data:
          # introduction 추가
          hotel_info["introduction"] = introduction
          
          # url 추가
          hotel_url = f"https://www.google.com/search?q={rec_hotel_id}&oq={rec_hotel_id}"
          hotel_info["url"] = hotel_url
          
          # img 추가
          hotel_img = get_img(rec_hotel_id)
          hotel_info["img"] = hotel_img
          result.append(hotel_info)
      
    result = json.dump(result, indent=4, ensure_ascii=False)
        
    return result
  
  result = search_information(csv_file, submit_json)
  return result

if __name__ == "__main__":
  load_dotenv()  # 환경 변수 로드
  
  csv_file = "/root/LLM_Bootcamp/Project3/cleaned_top_200_rows.csv"
  ans_json = '{"introduction" : "asdf", "hotel_id" : ["백년한옥", "엘리스호텔"]}' # 예시(json으로 받아온거)

  result = get_information(ans_json)
  
  if result:
      print(result)
  else:
      print("No matching hotel_id found.")
    
