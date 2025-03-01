import sys 
sys.path.append("packages/assistant/api")
import chat

def test_api():
    args = {}
    ch = chat.Chat(args)
    msg = "user:What is the capital of Italy"
    ch.add(msg)
    out = ch.complete()
    print(out.find("Rom") )
    #assert out.find("Rom") != -1
    print(len(ch.messages) )
    assert len(ch.messages) == 2
    assert ch.messages[0]['role'] == 'system'
    assert ch.messages[1]['role'] == 'user'
   # assert ch.messages[2]['role'] == 'assistant'
    
