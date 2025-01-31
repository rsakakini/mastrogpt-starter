import os, requests as req, json, socket
MODEL="deepseek-r1:32b"

def stream(args, lines):
    out = ""
    stream = (args.get("STREAM_HOST"), int(args.get("STREAM_PORT")))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect(stream)
      for line in lines:
          #print(line)
          dec = json.loads(line.decode('utf-8'))
          response = dec.get("response", "")
          if response == "<think>": response = "[think]"
          if response == "</think>": response = "[/think]"
          res = {"output": response}
          out += response
          s.sendall(json.dumps(res).encode('utf-8'))
      s.sendall(b"{}")
    return out


def deepseek(args):
  llm =  f"https://{args.get("OLLAMA_TOKEN")}@{args.get("OLLAMA_HOST")}/api/generate"
  out = f"Welcome to {MODEL}"
  inp = args.get("input", "")
  if inp != "":
    msg = { "model": MODEL, "prompt": inp, "stream": True }
    lines = req.post(llm, json=msg, stream=True).iter_lines()
    out = stream(args, lines)
  return { "output": out, "streaming": True}
