import tkinter as tk
from tkinter import messagebox

recipes = {
    "계란밥":["밥","계란","간장"],
    "김치볶음밥":["밥","김치","식용유"],
    "계란볶음밥":["밥","계란","대파","식용유"],
    "참치마요덮밥":["밥","참치","마요네즈"],
    "김치찌개":["김치","돼지고기","두부"],
    "된장찌개":["된장","두부","간장","양파"],
    "프렌치토스트":["식빵","계란","우유","식용유"],
    "치즈토스트":["식빵","치즈"],
    "라면":["라면"],
    "계란라면":["라면","계란"]
}

# 레시피에 등장하는 모든 재료 목록 자동 추출
ingredients = sorted(list(set(ing for req in recipes.values() for ing in req)))

result_list = None
ingredient_vars = {}
detail_label = None
status_label = None
ingredient_frame = None

def get_selected():
    return [
        name for name, variable in ingredient_vars.items()
        if variable.get()
    ]

def clear_results():
    if result_list:
        result_list.delete(0, tk.END)
    if detail_label:
        detail_label.config(text="메뉴를 선택하면 상세 정보가 표시됩니다.")
    if status_label:
        status_label.config(text="재료 선택 후 버튼을 누르세요.")

def reset():
    for variable in ingredient_vars.values():
        variable.set(False)
    clear_results()
    if status_label:
        status_label.config(text="재료를 선택하고 추천 버튼을 누르세요.")

def recommend():
    selected = get_selected()
    result_list.delete(0, tk.END)
    detail_label.config(text="메뉴를 선택하면 필요한 재료가 표시됩니다.")
    
    if not selected:
        status_label.config(text="재료를 선택해주세요.")
        messagebox.showwarning("재료 확인", "가진 재료를 체크하세요.")
        return

    for food, required in recipes.items():
        missing = [
            ingredient for ingredient in required 
            if ingredient not in selected 
        ]

        if not missing:
            result_list.insert(tk.END, food)

    count = result_list.size()

    if count == 0:
        status_label.config(text="현재 재료로 만들 수 있는 메뉴가 없습니다.")
    else:
        status_label.config(text=f"총 {count}개의 메뉴를 추천합니다.")

def find_almost():
    selected = get_selected()

    result_list.delete(0, tk.END)
    detail_label.config(text="메뉴를 선택하면 부족한 재료가 표시됩니다.")

    if not selected:
        status_label.config(text="재료를 선택해주세요.")
        messagebox.showwarning("재료 확인", "가진 재료를 체크하세요.")
        return

    for food, required in recipes.items():
        missing = [
            ingredient for ingredient in required 
            if ingredient not in selected
        ]

        if len(missing) == 1 and len(required) > 1:
            result_list.insert(tk.END, food)

    count = result_list.size()
    status_label.config(
        text=f"재료 한 개만 더 있으면 되는 메뉴 : {count}개"
    )

def show_details(event=None):
    selection = result_list.curselection()

    if not selection:
        return

    food = result_list.get(selection[0])
    selected = get_selected()
    required = recipes[food]

    missing = [
        ingredient for ingredient in required
        if ingredient not in selected
    ]

    text = (
        f"음식 : {food}\n"
        f"필수 재료: {', '.join(required)}\n"
    )

    if missing:
        text += f"부족한 재료: {', '.join(missing)}"
    else:
        text += "필수 재료가 모두 있습니다."

    detail_label.config(text=text)

def show_help():
    messagebox.showinfo(
        "사용 방법",
        "1. 냉장고에 있는 재료를 체크하세요.\n"
        "2. '메뉴 추천' 버튼을 누르세요.\n"
        "3. 결과에서 음식을 선택하면 필요한 재료를 볼 수 있습니다.\n\n"
        "4. '한 개만 더!'를 누르면 재료 한 개가 부족한 음식을 보여줍니다.\n\n"
        "물은 기본으로 있다고 가정합니다.\n"
        "등록된 간단 레시피의 필수 재료를 기준으로 추천합니다."
    )

# --- 메인 윈도우 생성 (함수 밖으로 분리) ---
window = tk.Tk()
window.title("냉장고 털이 메뉴 추천기")
window.geometry("700x720")
window.minsize(620, 680)

menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="선택 초기화", command=reset)
file_menu.add_separator()
file_menu.add_command(label="종료", command=window.destroy)  # destory 오타 수정
menu_bar.add_cascade(label="파일", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="사용 방법", command=show_help)
menu_bar.add_cascade(label="도움말", menu=help_menu)

main_frame = tk.Frame(window, padx=20, pady=15)
main_frame.pack(fill=tk.BOTH, expand=True)  # file -> fill 수정

title_label = tk.Label(
    main_frame,
    text="냉장고 털이 메뉴 추천기",
    font=("맑은 고딕", 20, "bold")
)
title_label.pack(pady=(0, 5))

guide_label = tk.Label(
    main_frame,
    text="우리 집에 있는 재료",
    padx=10,
    pady=5
)
guide_label.pack(anchor="w")

# 누락되었던 ingredient_frame 생성 추가
ingredient_frame = tk.LabelFrame(main_frame, text="재료 선택", padx=10, pady=10)
ingredient_frame.pack(fill=tk.X, pady=5)  # file -> fill 수정

for index, name in enumerate(ingredients):
    variable = tk.BooleanVar(value=False)
    ingredient_vars[name] = variable

    checkbox = tk.Checkbutton(
        ingredient_frame,
        text=name,
        variable=variable,
        command=clear_results
    )
    checkbox.grid(
        row=index // 4,
        column=index % 4,
        sticky="w",
        padx=8,
        pady=3
    )

for column in range(4):
    ingredient_frame.columnconfigure(column, weight=1)

button_frame = tk.Frame(main_frame)
button_frame.pack(pady=12)

recommend_button = tk.Button(
    button_frame,
    text="메뉴 추천",
    width=13,
    command=recommend
)
recommend_button.pack(side=tk.LEFT, padx=5)

almost_button = tk.Button(
    button_frame,
    text="한 개만 더!",
    width=10,
    command=find_almost
)
almost_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(
    button_frame,
    text="초기화",
    width=10,
    command=reset
)
reset_button.pack(side=tk.LEFT, padx=5)

result_frame = tk.LabelFrame(
    main_frame,
    text="추천 메뉴",
    padx=8,
    pady=8
)
result_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_list = tk.Listbox(
    result_frame,
    font=("맑은 고딕", 11),
    height=5,
    exportselection=False,
    yscrollcommand=scrollbar.set  # vscrollcommand -> yscrollcommand 수정
)
result_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # file -> fill 수정
result_list.bind("<<ListboxSelect>>", show_details)

scrollbar.config(command=result_list.yview)

detail_frame = tk.LabelFrame(
    main_frame,
    text="필수 재료와 부족한 재료",
    padx=10,
    pady=10
)
detail_frame.pack(fill=tk.X, pady=5)

detail_label = tk.Label(
    detail_frame,
    text="메뉴를 선택하면 상세 정보가 표시됩니다.",
    justify=tk.LEFT,
    anchor="w",
    wraplength=540
)
detail_label.pack(fill=tk.X)

status_label = tk.Label(
    main_frame,
    text="재료를 선택하고 추천 버튼을 누르세요.",  # 누르새요 오타 수정
    fg="blue",
    anchor="w"
)
status_label.pack(fill=tk.X, pady=(5, 0))

window.mainloop()