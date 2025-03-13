import os,sys, requests as req
import vision
from datetime import datetime
import bucket
import base64

USAGE = "Please upload a picture and I will tell you what I see"
FORM = [
  {
    "label": "any pics?",
    "name": "pic",
    "required": "true",
    "type": "file"
  },
]

def form(args):
  res = {}
  out = USAGE
  inp = args.get("input", "")

  if type(inp) is dict and "form" in inp:
    img = inp.get("form", {}).get("pic", "")
    print(f"uploaded size {len(img)}")
    vis = vision.Vision(args)
    out = vis.decode(img)

    buc = bucket.Bucket(args)
    dt = str(datetime.now()).replace(" ","-").replace(".","-").replace(":","-")
    result = buc.write(dt,img)

    url = buc.exturl(dt, 50000)
    #res['html'] = f'<img src="data:image/png;base64,{img}">'
    print(url)
    res['html'] = f"<img src='{url}'>"
   

  res['form'] = FORM
  res['output'] = out
  return res
