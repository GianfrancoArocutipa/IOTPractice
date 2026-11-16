import json

def test():
    with open("c:/Users/PC/Desktop/oit/lab2/03_Circuito2_Contador_00_99_Multiplexado_Nano.txt", "r", encoding="utf-8") as f:
        content = f.read()
    print("Read success, length:", len(content))

if __name__ == "__main__":
    test()
