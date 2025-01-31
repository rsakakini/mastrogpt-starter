#--kind python:default
#--web true
#--param OLLAMA_HOST $OLLAMA_HOST
#--param OLLAMA_TOKEN $AUTH
import deepseek
def main(args):
  return { "body": deepseek.deepseek(args) }
