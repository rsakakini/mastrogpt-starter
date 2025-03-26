import sys
sys.path.append("packages/vdb/load")
import vdb, time

def test_vdb():
    args = {}

    db = vdb.VectorDB(args)
    db.setup(drop=True)
    assert len(db.embed("hello world")) == 1024

    assert len(db.vector_search("hello")) == 0
    
    db.insert("Hello world")
    db.insert("This is a test")
    db.insert("This is another test")
    time.sleep(1)

    test = db.vector_search("test")
    assert len(test) == 3
    assert test[0][1].find("test") != -1

    hello = db.vector_search("hello")
    assert hello[0][1].find("Hello") != -1

    assert db.remove_by_substring("test") == 2
    

def test_length():
    fr = "[Natural, language, processing, (, NLP, ), is, a, field, of, computer, science, ,, artificial, intelligence, and, computational, linguistics, concerned, with, the, interactions, between, computers, and, human, (, natural, ), languages, ,, and, ,, in, particular, ,, concerned, with, programming, computers, to, fruitfully, process, large, natural, language, corpora, ., Challenges, in, natural, language, processing, frequently, involve, natural, language, understanding, ,, natural, language, generation, (, frequently, from, formal, ,, machine-readable, logical, forms, ), ,, connecting, language, and, machine, perception, ,, managing, human-computer, dialog, systems, ,, or, some, combination, thereof, .]"
    temp = fr[:600]
    assert len(fr) == 709
    assert len(temp) == 600
