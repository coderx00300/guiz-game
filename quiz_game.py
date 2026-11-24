import tkinter as tk
import random
import math

W, H = 900, 600
BG_COLOR = "#2e6b55"

root = tk.Tk()
root.title("Зачёт по БД")
root.geometry(f"{W}x{H}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=W, height=H, highlightthickness=0)
canvas.pack()

def load(name):
    try:
        return tk.PhotoImage(file=name)
    except Exception:
        return None

bg      = load("background.png")
teacher = load("teacher.png")
student = load("student.png")

def shrink(img, k):
    if img and k > 1:
        return img.subsample(k, k)
    return img

teacher_big = shrink(teacher, 2) if teacher else None
student_sm  = shrink(student, 2) if student else None

QUESTIONS = [
    ("Что такое база данных?",
     ["Программа для рисования", "Организованная совокупность данных", "Тип процессора"],
     "Организованная совокупность данных"),
    ("Какой язык используется для запросов к БД?",
     ["HTML", "Python", "SQL"], "SQL"),
    ("Что такое первичный ключ (PRIMARY KEY)?",
     ["Поле, уникально идентифицирующее запись", "Пароль от базы", "Название таблицы"],
     "Поле, уникально идентифицирующее запись"),
    ("Что делает команда SELECT?",
     ["Удаляет таблицу", "Выбирает данные из таблицы", "Создаёт пользователя"],
     "Выбирает данные из таблицы"),
    ("Что такое запись (строка) в таблице?",
     ["Один столбец", "Название базы", "Одна строка данных"],
     "Одна строка данных"),
    ("Что такое внешний ключ (FOREIGN KEY)?",
     ["Поле, ссылающееся на ключ другой таблицы", "Главный пароль", "Имя сервера"],
     "Поле, ссылающееся на ключ другой таблицы"),
    ("Что делает команда INSERT?",
     ["Удаляет базу", "Добавляет данные в таблицу", "Меняет пароль"],
     "Добавляет данные в таблицу"),
    ("Что такое нормализация?",
     ["Сжатие картинок", "Ускорение интернета",
      "Организация данных для уменьшения дублирования"],
     "Организация данных для уменьшения дублирования"),
    ("Что делает команда DELETE?",
     ["Удаляет данные из таблицы", "Создаёт таблицу", "Показывает данные"],
     "Удаляет данные из таблицы"),
    ("Что такое СУБД?",
     ["Система управления базами данных", "Союз умных ботов", "Сетевой удалённый доступ"],
     "Система управления базами данных"),
]

score = 0
q_index = 0
tick = 0
shake = 0
feedback = None
selected = None
answers_now = []
particles = []
scene = "intro"

def draw_bg():
    if bg:
        canvas.create_image(0, 0, image=bg, anchor="nw")
    else:
        canvas.create_rectangle(0, 0, W, H, fill=BG_COLOR, outline="")

def draw_teacher(x, y, img, talking=False):
    sway = math.sin(tick * 0.05) * 5
    canvas.create_image(x, y + sway, image=img, anchor="nw")
    hand_x = x + img.width() - 10
    hand_y = y + sway + img.height() * 0.35
    ang = math.sin(tick * 0.12) * 0.35
    px = hand_x + 90 * math.cos(ang)
    py = hand_y - 90 * math.sin(ang)
    canvas.create_line(hand_x, hand_y, px, py, width=4,
                       fill="#f5e9c8", capstyle=tk.ROUND)
    if talking and tick % 20 < 10:
        canvas.create_oval(x + img.width()*0.45, y + sway + img.height()*0.22,
                           x + img.width()*0.45 + 12, y + sway + img.height()*0.22 + 8,
                           fill="#b35", outline="")

def draw_student(x, y, img, happy=False):
    bounce = abs(math.sin(tick * 0.4)) * 15 if happy else math.sin(tick * 0.06) * 4
    canvas.create_image(x, y - bounce, image=img, anchor="nw")

def draw_intro():
    draw_bg()
    img = teacher_big or teacher
    if img:
        draw_teacher(60, 180, img, talking=True)
    bx, by = 380, 140
    phrases = ["Привет!", "Готов к зачёту по БД?", "10 вопросов. Поехали?"]
    phrase = phrases[(tick // 60) % len(phrases)]
    canvas.create_oval(bx, by, bx + 320, by + 110, fill="#fffdf0",
                       outline="#3c6e3c", width=4)
    canvas.create_polygon(bx - 15, by + 55, bx + 15, by + 70, bx + 15, by + 45,
                          fill="#fffdf0", outline="")
    canvas.create_text(bx + 160, by + 55, text=phrase,
                       font=("Arial", 18, "bold"), fill="#1e461e")
    canvas.create_rectangle(W//2 - 180, 400, W//2 - 40, 455,
                            fill="#78e68c", outline="#3c6e3c", width=3, tags="yes")
    canvas.create_text(W//2 - 110, 427, text="Да!",
                       font=("Arial", 20, "bold"), fill="#1e461e", tags="yes")
    canvas.create_rectangle(W//2 + 40, 400, W//2 + 180, 455,
                            fill="#fa8c8c", outline="#3c6e3c", width=3, tags="no")
    canvas.create_text(W//2 + 110, 427, text="Нет",
                       font=("Arial", 20, "bold"), fill="#1e461e", tags="no")
    canvas.create_text(W//2, 540, text="Нажми «Да!», чтобы начать зачёт",
                       font=("Arial", 14), fill="#ffffe0")

def draw_question():
    draw_bg()
    q, answers, correct = QUESTIONS[q_index]
    canvas.create_rectangle(40, 60, W - 40, 190, fill="#fffdf0",
                            outline="#3c6e3c", width=4)
    words, lines = q.split(), [""]
    for w_ in words:
        if len(lines[-1]) + len(w_) < 60:
            lines[-1] += " " + w_
        else:
            lines.append(" " + w_)
    for i, ln in enumerate(lines):
        canvas.create_text(W//2, 100 + i*30, text=ln.strip(),
                           font=("Arial", 22, "bold"), fill="#1e461e")
    y = 230
    for i, a in enumerate(answers_now):
        canvas.create_rectangle(60, y, W - 60, y + 60,
                                fill="#fffdf0", outline="#3c6e3c", width=3,
                                tags=("btn", str(i)))
        canvas.create_text(85, y + 30, text=f"{'АБВ'[i]})  {a}",
                           anchor="w", font=("Arial", 20), fill="#1e461e",
                           tags=("btn", str(i)))
        y += 85
    canvas.create_text(W//2, 30, text=f"Вопрос {q_index+1}/10    Счёт: {score}",
                       font=("Arial", 18, "bold"), fill="#ffffe0")
    if student_sm or student:
        draw_student(W - 130, H - 170, student_sm or student,
                     happy=(feedback == "correct"))
    draw_confetti()

def draw_confetti():
    for p in particles:
        canvas.create_rectangle(int(p[0]), int(p[1]),
                                int(p[0]) + 8, int(p[1]) + 8,
                                fill=p[4], outline="")

def answer(i):
    global feedback, score, shake
    if feedback is not None:
        return
    correct = QUESTIONS[q_index][2]
    if answers_now[i] == correct:
        score += 1
        feedback = "correct"
        spawn_confetti()
    else:
        feedback = "wrong"
        shake = 12
    btn_rects = [it for it in canvas.find_withtag("btn")
                 if canvas.type(it) == "rectangle"]
    for j, item in enumerate(btn_rects):
        if answers_now[j] == correct:
            canvas.itemconfig(item, fill="#78e68c")
        elif j == i:
            canvas.itemconfig(item, fill="#fa8c8c")
    msg = ("ВЕРНО! +1" if feedback == "correct"
           else f"НЕВЕРНО! Правильно: {correct}")
    canvas.create_text(W//2, 530, text=msg, font=("Arial", 26, "bold"),
                       fill="#78ff8c" if feedback == "correct" else "#ff7878")
    canvas.after(1200, next_question)

def next_question():
    global feedback, selected, q_index
    feedback = None
    selected = None
    q_index += 1
    if q_index >= len(QUESTIONS):
        start_result()
    else:
        prepare_answers()
        render()

def prepare_answers():
    global answers_now
    answers_now = QUESTIONS[q_index][1][:]
    random.shuffle(answers_now)

def spawn_confetti():
    colors = ["#50dc78", "#fad23c", "#5ab4fa", "#fa7878"]
    for _ in range(60):
        particles.append([random.randint(80, W - 80), random.randint(150, 300),
                          random.uniform(-2, 2), random.uniform(-5, -1),
                          random.choice(colors)])

def start_result():
    global scene
    scene = "result"
    render()

def draw_result():
    draw_bg()
    img = teacher_big or teacher
    if img:
        draw_teacher(80, 200, img, talking=True)
    if student_sm or student:
        draw_student(W - 200, H - 260, student_sm or student, happy=True)
    canvas.create_rectangle(280, 120, W - 280, 320, fill="#fffdf0",
                            outline="#3c6e3c", width=4)
    msg = ("Молодец! Зачёт сдан!" if score >= 7 else
           "Хорошо! Ещё потренируйся" if score >= 4 else
           "Зачёт не сдан, попробуй снова!")
    canvas.create_text(W//2, 170, text=f"Результат: {score} из 10",
                       font=("Arial", 28, "bold"), fill="#1e461e")
    canvas.create_text(W//2, 230, text=msg, font=("Arial", 18), fill="#3c6e3c")
    canvas.create_rectangle(W//2 - 130, 430, W//2 + 130, 490,
                            fill="#f0c850", outline="black", tags="again")
    canvas.create_text(W//2, 460, text="Играть снова",
                       font=("Arial", 18, "bold"), tags="again")
    draw_confetti()

def restart():
    global score, q_index, feedback, selected, particles, scene
    score, q_index, feedback, selected = 0, 0, None, None
    particles = []
    scene = "quiz"
    prepare_answers()
    render()

def on_click(event):
    global scene
    items = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    for item in items:
        tags = canvas.gettags(item)
        if scene == "intro" and "yes" in tags:
            scene = "quiz"
            particles.clear()
            render()
            return
        if scene == "intro" and "no" in tags:
            canvas.create_text(W//2, 500, text="Ну ладно, тогда учи! :)",
                               font=("Arial", 18, "bold"), fill="#ffffe0")
            return
        if scene == "quiz" and "btn" in tags and feedback is None:
            for t in tags:
                if t.isdigit():
                    answer(int(t))
                    return
        if scene == "result" and "again" in tags:
            restart()
            return

def render():
    if scene == "intro":
        draw_intro()
    elif scene == "quiz":
        draw_question()
    else:
        draw_result()

def animate():
    global tick, shake
    tick += 1
    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.15
    particles[:] = [p for p in particles if p[1] < H]
    if scene in ("intro", "result") or particles:
        render()
    if shake > 0:
        shake -= 1
        dx = random.randint(-shake, shake)
        dy = random.randint(-shake, shake)
        canvas.place(x=dx, y=dy)
    else:
        canvas.place(x=0, y=0)
    root.after(16, animate)

canvas.bind("<Button-1>", on_click)
prepare_answers()
render()
animate()
root.mainloop()
