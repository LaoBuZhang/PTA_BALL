import pickle

def asr_main():
    dict = {}
    # 写入
    with open("dict.pkl", "wb") as f:
        pickle.dump(dict, f)