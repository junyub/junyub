from flask import Flask, jsonify, request
import openai
import aiohttp
import asyncio
import logging
from threading import Thread
from cachetools import TTLCache
import pandas as pd
from datetime import datetime

# 로그 설정
logging.basicConfig(level=logging.INFO)

application = Flask(__name__)

# OpenAI API 키 설정
OPENAI_API_KEY = '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'

# 사용자 세션 상태를 저장하기 위한 딕셔너리 및 캐시 설정
session_data = {}
response_cache = TTLCache(maxsize=100, ttl=300)  # 캐시 최대 크기와 TTL(초) 설정

# 파일 경로
csv_files = {
    "meal_data": '학식_ver2.csv',
    "number_data": '전화번호.csv',
    "professor_data": '교수정보.csv',
    "bus_data": '버스정보.csv',
    "facility_data": '시설정보.csv',
    "academic_schedule_data": '학사일정.csv'
}

# 인코딩을 시도할 목록
encodings = ['utf-8']


# 각 파일의 데이터를 읽어 메모리에 저장
def read_csv_with_multiple_encodings(file):
    for encoding in encodings:
        try:
            return pd.read_csv(file, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("파일을 읽을 수 없습니다. 지원되는 인코딩이 아닙니다.")


cache = {}
for key, file in csv_files.items():
    data = read_csv_with_multiple_encodings(file)
    cache[key] = data.to_dict(orient='records')


async def fetch_response_from_gpt(user_id, question, prompt):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                    'https://api.openai.com/v1/chat/completions',
                    json={
                        'model': 'gpt-4o',
                        'messages': [{'role': 'user', 'content': prompt}],
                        'max_tokens': 300,
                        'temperature': 0,
                        'n': 1,
                        'stop': None
                    },
                    headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
                    timeout=10
            ) as resp:
                logging.info(f'Response status: {resp.status}')
                if resp.status == 200:
                    result = await resp.json()
                    response_text = result['choices'][0]['message']['content'].strip()
                    logging.info(f'API Response: {result}')
                    session_data[user_id] = response_text
                    response_cache[question] = response_text
                else:
                    session_data[user_id] = f'AI 응답 중 오류가 발생했어요. 상태 코드: {resp.status}'
        except asyncio.TimeoutError:
            session_data[user_id] = '미안해요, 아토의 답변 지연되고 있어요.'
        except Exception as e:
            logging.error(f'Error occurred: {e}')
            session_data[user_id] = f'오류가 발생했어요: {str(e)}'


def fetch_openai_response(user_id, question, prompt):
    asyncio.run(fetch_response_from_gpt(user_id, question, prompt))


def create_prompt(question, cache):
    # 현재 날짜 가져오기
    current_date = datetime.now().strftime("%Y-%m-%d")
    general_prompt = f"""
    You are a university guide chatbot. Respond to user inquiries concisely, providing only essential information in Korean.
    Make sure to provide the most accurate and up-to-date information available.
    Be polite and professional in your responses.

    Today's date is {current_date}.

    After answering each question, end with the following sentence: "다음 질문을 하고 싶다면 다시 한번 아토를 불러주세요!"
    """

    if '식단' in question or '메뉴' in question or '학식' in question or '점심' in question or '저녁' in question or '아침' in question:
        meal_data = cache['meal_data']
        prompt = f"""
        {general_prompt}

        Here is the meal data:
        {meal_data}

        Provide meal information along with an estimated calorie count for each meal. Respond to the following question and any related follow-up questions in Korean:
        Question: {question}
        """

    elif '번호' in question or '전화번호' in question or '연락처' in question:
        number_data = cache['number_data']
        prompt = f"""
        {general_prompt}

        Here is the number data:
        {number_data}

        Based on the above information, respond to the following question and any related follow-up questions in Korean:
        Question: {question}
        """
    elif '교수' in question:
        professor_data = cache['professor_data']
        prompt = f"""
        {general_prompt}

        Here is the professor data:
        {professor_data}

        Based on the above information, respond to the following question and any related follow-up questions in Korean:
        Question: {question}
        """
    elif '버스' in question or '노선' in question:
        bus_data = cache['bus_data']
        prompt = f"""
        {general_prompt}

        Here is the bus data:
        {bus_data}

        Based on the above information, respond to the following question and any related follow-up questions in Korean:
        Question: {question}
        """
    elif '시설' in question:
        facility_data = cache['facility_data']
        prompt = f"""
        {general_prompt}

        Here is the facility data:
        {facility_data}

        Based on the above information, respond to the following question and any related follow-up questions in Korean:
        Question: {question}
        """
    elif '학사 일정' in question or '일정' in question:
        academic_schedule_data = cache['academic_schedule_data']
        prompt = f"""
        {general_prompt}

        Here is the academic schedule data:
        {academic_schedule_data}

        Based on the above information, respond to the following question and any related follow-up questions in Korean:
        Question: {question}
        """
    else:
        prompt = f"""
        {general_prompt}

        Respond to the following question and any related follow-up questions in Korean:
        Question: {question}
        """
    return prompt


@application.route('/webhook/', methods=['POST'])
def webhook():
    request_data = request.get_json()
    user_id = request_data['user']
    session_data[user_id] = request_data['result']['choices'][0]['message']['content']
    return 'OK'


@application.route('/question', methods=['POST'])
def get_question():
    request_data = request.get_json()
    user_id = request_data['userRequest']['user']['id']
    question = request_data['action']['params']['question']

    response = {
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {'text': '아토가 질문을 배달하고 있어요. 3초 후에 "답변"을 입력해주세요!'}
            }]
        }
    }
    session_data[user_id] = '아토가 아직 생각하고 있어요. 잠시후에 다시 "답변"을 입력해주세요!'

    prompt = create_prompt(question, cache)
    thread = Thread(target=fetch_openai_response, args=(user_id, question, prompt))
    thread.start()
    return jsonify(response)


@application.route('/ans', methods=['POST'])
def get_answer():
    request_data = request.get_json()
    user_id = request_data['userRequest']['user']['id']
    response_text = session_data.get(user_id, '질문을 하신적이 없어보여요. 아토를 불러주세요')
    response = {
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': f"답변: {response_text}"
                }
            }]
        }
    }
    return jsonify(response)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5152, debug=True)
