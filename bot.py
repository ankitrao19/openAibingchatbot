import requests
import json
import openai
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()


class MetaResponse(BaseModel):
    query: str

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable GZip compression
app.add_middleware(GZipMiddleware, minimum_size=500)
# Custom exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


@app.get('/')
def root():
    return "Success!!"

def formating_data(bing_data, query):
  foo = bing_data['webPages']['value']
  first_str = 'Generate a summary of the below conversation in the following format:\n\n'
  new_data = []
  new_data.append(first_str)
  for i in foo:
    if 'snippet' in i:
      new_d = i['snippet']
      new_data.append(new_d)
  data_str = ''.join(new_data)  
  return data_str

def bing_data(query):
  foo = query['webPages']['value']
  new_data = []
  for i in foo:
    if 'snippet' in i:
      value_n = i['snippet']
      new_data.append(value_n)
    if 'url' in i:
      key_n = i['url']
      new_data.append(key_n)
    #new_data[key_n] = value_n
  return new_data



@app.post("/bingopenai")
def getResponse(payload: MetaResponse):
    query = payload.query
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    api_key = "******************************"
    params = {"q": query, "count": 7}  # Count is Number of results to retrieve
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        bing_formated_data = formating_data(data,query)
        
        open_ai_data = {'prompt':bing_formated_data, 'temperature':0.5, 'max_tokens':1000, 'top_p':1, 'frequency_penalty':0, 'presence_penalty':0, 'best_of':1, 'stop':"None"}
        open_ai_url = "https://pepchatgpt-openai.openai.azure.com/openai/deployments/text-davinci-003/completions?api-version=2023-03-15-preview"
        open_ai_payload = json.dumps(open_ai_data)
        open_ai_headers = {'api-key': 'e9cb9f619df544f9a470c6c210713f77', 'Content-Type': 'application/json'}
        open_ai_response = requests.request("POST", open_ai_url, headers=open_ai_headers, data=open_ai_payload)
        response = open_ai_response.json()
        result_data = response['choices'][0]['text']

        
        return {'response':result_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bing")
def getResponse(payload: MetaResponse):
    query = payload.query
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    api_key = "*******************"
    params = {"q": query, "count": 7}  # Count is Number of results to retrieve
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        bing_results = bing_data(data)
        response_string = ' '.join(bing_results)
        return {'response':response_string}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
