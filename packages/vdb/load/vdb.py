import os, requests as req
from pymilvus import MilvusClient, DataType
from bs4 import BeautifulSoup

MODEL="mxbai-embed-large:latest"
DIMENSION=1024
LIMIT=10

class VectorDB:

  def __init__(self, args):
      uri = f"http://{args.get("MILVUS_HOST", os.getenv("MILVUS_HOST"))}"
      token = args.get("MILVUS_TOKEN", os.getenv("MILVUS_TOKEN"))    
      db_name = args.get("MILVUS_DB_NAME", os.getenv("MILVUS_DB_NAME"))
      self.client =  MilvusClient(uri=uri, token=token, db_name=db_name)

      host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
      auth = args.get("OLLAMA_TOKEN", os.getenv("AUTH"))
      self.url = f"https://{auth}@{host}/api/embeddings"

      self.collection = args.get("COLLECTION", "test")
      self.setup()

  def setup(self, drop=False):
    if drop:
      self.client.drop_collection(self.collection)
      
    if not self.collection in self.client.list_collections():
      schema = self.client.create_schema()
      schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
      schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=DIMENSION)
      schema.add_field(field_name="embeddings", datatype=DataType.FLOAT_VECTOR, dim=DIMENSION)
      
      index_params = self.client.prepare_index_params()
      index_params.add_index("embeddings", index_type="AUTOINDEX", metric_type="IP")
      self.client.create_collection(collection_name=self.collection, schema=schema, index_params=index_params)

  def embed(self, text):
    msg = { "model": MODEL, "prompt": text, "stream": False }
    res = req.post(self.url, json=msg).json()
    return res.get('embedding', [])

  def insert(self, text):
    listDic =[]
    if text.startswith("https:") or text.startswith("HTTPS:"):
       
       result = req.get(text)
       #soup = BeautifulSoup(result.text, 'html.parser')
       #body = soup.body 
       #print("soup.body****" + body.text)   
       #tokens = tokenize(body.text)          # extract sentences from text
       #i = 0
       #while i < len(tokens) and i:
        #token = tokens[i]
       #try: 
       soup = BeautifulSoup(result.text, "lxml")
       news_para = soup.find_all("p", text = True)

       for item in news_para:
            # SPLIT WORDS, JOIN WORDS TO REMOVE EXTRA SPACES
            token = (' ').join((item.text).split())
            token = token.strip(',.-').replace("‘","").replace("’","")
            if token!="" and token!="P" and token!="Output:":
             
             print("token ----" + token)
             print("LENGHT TOKEN ****" )
             print(len(token))
 
             if(len(token)>1024):
                info = token[:1000]
             else:
                info = token

            print("info ----" + info)
            print("LENGHT ****" )
            print(len(info))
            
            vec = self.embed(info)
            listDic.append({"text":info, "embeddings": vec})    
    else:
        vec = self.embed(text)
        dic= {"text":text, "embeddings": vec}
        listDic.append(dic)

    return self.client.insert(self.collection,listDic)


  def vector_search(self, inp, limit=LIMIT):
    vec = self.embed(inp)
    cur = self.client.search(
      collection_name=self.collection,
      search_params={"metric_type": "IP"},
      anns_field="embeddings", data=[vec],
      output_fields=["text"]
    )
    res = []
    if len(cur[0]) > 0:
      for item in cur[0]:
        dist = item.get('distance', 0)
        text = item.get("entity", {}).get("text", "")
        res.append((dist, text))
    return res

  def remove_by_substring(self, inp):
    cur = self.client.query_iterator(collection_name=self.collection, 
              batchSize=2, output_fields=["text"])
    res = cur.next()
    ids = []
    while len(res) > 0:
      for ent in res:
        if ent.get('text', "").find(inp) != -1:
          ids.append(ent.get('id'))
      res = cur.next()
    if len(ids) >0:
      res = self.client.delete(collection_name=self.collection, ids=ids)
      return res['delete_count']
    return 0


def tokenize3(text):

    # EMPTY LIST TO STORE PROCESSED TEXT
    proc_text = []

    try:
        #news_open = urllib.request.urlopen(webpage.group())
        news_soup = BeautifulSoup(text, "lxml")
        news_para = news_soup.find_all("p", text = True)

        for item in news_para:
            # SPLIT WORDS, JOIN WORDS TO REMOVE EXTRA SPACES
            para_text = (' ').join((item.text).split())

            # COMBINE LINES/PARAGRAPHS INTO A LIST
            proc_text.append(para_text)

    except urllib.error.HTTPError:
        pass

    return proc_text



import nltk.data 

def tokenize2(text):
  nltk.download('punkt')                   # load tokenizer model
  from nltk.tokenize import sent_tokenize
  return sent_tokenize(text)          # extract sentences from text
  #enum = enumerate(sentences, 1)           # enumerate
  #sent = next(enum)                        # extract one sentence

import re

def tokenize(text):
    tokens = text.split()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', token):
            pass
        
        elif re.match(r"\w+'s", token):
            token = re.sub(r"(\w+)'s", r"\1 's", token)
        
        elif re.match(r"\w+'\w+", token):
            token = token.replace("'", "")
        
        elif re.match(r"\w+-\w+", token):
            pass
        
        elif re.match(r"\d+(,\d+)*", token):
            pass
        
        else:
            token = re.sub(r"([^\w\s]+)", r" \1 ", token)
        
        token = re.sub(r"(\w+)\.", r"\1", token)
        token = re.sub(r"(\w+),", r"\1", token)
        token = re.sub(r"U\.S\.A\.", r"U.S.A.", token)
        
        tokens[i] = token
        i += 1
    
    return tokens

