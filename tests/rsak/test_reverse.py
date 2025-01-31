import sys 
sys.path.append("packages/rsak/reverse")
import reverse

def test_reverse():
   # args = {}
   # res = reverse.reverse(args)
   # assert res["output"] == reversed
    args = {"input": "Mike"}
    res = reverse.main(args)
    assert res["body"] == "ekiM"
