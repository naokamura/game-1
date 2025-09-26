import tkinter as tk
import random

class GameOver(Exception):
    pass

inventory = []
visited_events = set()

# ---------------- GUI 初期化 ---------------- #
root = tk.Tk()
root.title("磯野家からの脱出ゲーム")
root.geometry("500x300")

text_area = tk.Label(root, text="", wraplength=480, justify="left", font=("Arial", 12))
text_area.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

buttons = []

def clear_buttons():
    for b in buttons:
        b.destroy()
    buttons.clear()

def set_text(msg,delay=50):
    """文字を一文字ずつ表示する"""
    text_area.config(text="")
    
    def show(i=0):
        if i <=len(msg):
            text_area.config(text=msg[:i])
            root.after(delay,show,i+1)
    show()

def add_button(label, command):
    b = tk.Button(button_frame, text=label, command=command, width=25)
    b.pack(pady=2)
    buttons.append(b)

# ---------------- スタート ---------------- #
def start():
    set_text("サザエさんにみつからないように、家を脱出しよう！")
    clear_buttons()
    add_button("台所に行く", daidokoro)
    add_button("居間に行く", ima)
    add_button("玄関に行く", lambda: game_over("波平に捕まった！"))

# ---------------- ゲームオーバー ---------------- #
def game_over(reason):
    set_text("ゲームオーバー！ " + reason)
    clear_buttons()
    add_button("もう一度遊ぶ", restart)
    add_button("終了する", root.quit)

def restart():
    inventory.clear()
    visited_events.clear()
    start()

# ---------------- 台所 ---------------- #
def daidokoro():
    set_text("台所に来ました...")
    clear_buttons()

    events = [daidokoro_fune, daidokoro_trap, daidokoro_animal]
    available = [e for e in events if e.__name__ not in visited_events]

    if not available:
        set_text("特に何も起こらなかった。居間に移動する。")
        root.after(1500, ima)  # 1.5秒後に自動で移動
        return

    event = random.choice(available)
    visited_events.add(event.__name__)
    event()

def daidokoro_fune():
    msg = "フネが現れた！\n"
    if "おやつ" not in inventory:
        inventory.append("おやつ")
        msg += "フネは『おやつ』をくれた！"
    else:
        msg += "フネは夕飯の準備をしている。"
    msg += "\n\n台所から居間に向かう。"
    set_text(msg)
    clear_buttons()
    add_button("居間に行く", ima)

def daidokoro_trap():
    if "おやつ" in inventory:
        set_text("⚠️ いくらちゃんが現れた！\nおやつをあげたら喜んでいる。\n居間に向かう。")
        clear_buttons()
        add_button("居間に行く", ima)
    else:
        game_over("いくらちゃんに捕まった！\n脱出失敗！")

def daidokoro_animal():
    set_text("🐱 たまが飛びかかってきた！")
    clear_buttons()
    add_button("逃げる", ima)
    add_button("遊ぶ", lambda: play_with_tama())

def play_with_tama():
    if "おやつ" in inventory:
        set_text("少し遊んだら、たまは寝てしまった。\n居間に向かう。")
        clear_buttons()
        add_button("居間に行く", ima)
    else:
        game_over("たまに捕まった！\n脱出失敗！")

# ---------------- 居間 ---------------- #
def ima():
    events = [ima_masuo, ima_wakame, ima_nothing]
    random.choice(events)()

    set_text("居間についた...\n\n次はどうしますか？")
    clear_buttons()
    add_button("マスオの部屋に向かう" , ima_masuo)
    add_button("ワカメの部屋に向かう", ima_wakame)
    add_button("玄関に向かう",genkan)

def ima_masuo():
    if "バット" not in inventory:
        inventory.append("バット")
        set_text("マスオさんが現れた！\nバットをもらった！")
    else:
        set_text("マスオさんは通り過ぎた。")
    clear_buttons()
    add_button("居間に戻る",ima)
def ima_wakame():
    if "おやつ" in inventory:
        set_text(" ワカメ:『バットとおやつがあれば脱出できるわよ！\n玄関に行って！』")
    else:
        set_text(" ワカメ:『さっき中島くんが来てたわよ』")
    clear_buttons()
    add_button("居間に戻る",ima)

def ima_nothing():
    set_text("…特に何も起こらなかった。")
    clear_buttons()
    add_button("居間に戻る",ima)

# ---------------- ボス戦 ---------------- #
def genkan():
    set_text("サザエさんが玄関で通せんぼしている！")  
    clear_buttons()
    root.after(1500,check_genkan_end)

def check_genkan_end():    
    if "バット" in inventory and "おやつ" in inventory:
        set_text("サザエさんの隙をついて脱出成功！\n🎉 エンディング１：ハッピーエンド！")
    elif "バット"in inventory:
        set_text("サザエさんに挑んだが、おやつがなくて説得失敗…\n エンディング２：バッドエンド！")
    elif "おやつ"in inventory:
        set_text("おやつを渡したら、サザエさんは玄関を通してくれた！\n エンディング３：トゥルーエンド！")
    else:
        set_text("何もできずにサザエさんに捕まった…\n エンディング４：ノーマルバッドエンド！")

    clear_buttons()
    add_button("もう一度遊ぶ", restart)
    add_button("終了する", root.quit)
    

# ---------------- ゲーム開始 ---------------- #
start()
root.mainloop()
