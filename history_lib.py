def add_history(msg):
    with open("history.txt", 'a', encoding="utf-8") as f:
        f.write(msg+"\n")

def clear_history():
    with open("history.txt", 'w') as f:
        f.write("")

def get_history():
    with open("history.txt", 'r', encoding="utf-8") as f:
        return f.readlines()