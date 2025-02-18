import re, os, requests as req
#MODEL = "llama3.1:8b"
MODEL = "phi4:14b"

USAGE = """I will generate a chess with the selected elements you choosed"""

FORM = [
  {
    "name": "Queen",
    "label": "Whith a queen",
    "required": "false",
    "type": "checkbox"
  },
    {
    "name": "Rook",
    "label": "Whith a rook",
    "required": "false",
    "type": "checkbox"
  },
   {
    "name": "Knight",
    "label": "Whith a knight",
    "required": "false",
    "type": "checkbox"
  },{
    "name": "Bishop",
    "label": "Whith a bishop",
    "required": "false",
    "type": "checkbox"
  }

]


def chat(args, inp):
  host = args.get("OLLAMA_HOST", os.getenv("OLLAMA_HOST"))
  auth = args.get("AUTH", os.getenv("AUTH"))
  url = f"https://{auth}@{host}/api/generate"
  msg = { "model": MODEL, "prompt": inp, "stream": False}
  res = req.post(url, json=msg).json()
  out = res.get("response", "error")
  return  out
 
def extract_fen(out):
  pattern = r"([rnbqkpRNBQKP1-8]+\/){7}[rnbqkpRNBQKP1-8]+"
  fen = None
  m = re.search(pattern, out, re.MULTILINE)
  if m:
    fen = m.group(0)
  return fen

def puzzle(args):
  out = USAGE
  #out = "If you want to see a chess puzzle, type 'puzzle'. To display a fen position, type 'fen <fen string>'."
  inp = args.get("input", "")
  res = {}

  if inp == "":
     #out = USAGE
     res['form'] = FORM

  elif type(inp) is dict and "form" in inp:
      selection = "with "
      data = inp["form"]
      for field in data.keys():
        print(data.keys())
        if (data[field]) :
          selection += field + " "
          print(data[field])


      print(selection) 
      inp = f"""Generate a chess puzzle in FEN format"
            {selection}.
            """ 
      
      print(inp) 

      out = chat(args, inp)

  #if inp == "puzzle":
  #inp = "generate a chess puzzle in FEN format"
  # out = chat(args, inp)
      fen = extract_fen(out)
      if fen:
        print(fen)
        res['chess'] = fen
      else:
       out = "Bad FEN position."
  elif inp.startswith("fen"):
    fen = extract_fen(inp)
    if fen:
       out = "Here you go."
       res['chess'] = fen
  elif inp != "":
    out = chat(args, inp)
    fen = extract_fen(out)
    print(out, fen)
    if fen:
      res['chess'] = fen

  res["output"] = out
  return res
