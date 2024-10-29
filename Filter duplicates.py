import pandas as pd
from tkinter import Tk, Button, Label, filedialog
import os

def select_file1():
    # 通过对话框选择第一份文件路径
    file_path = filedialog.askopenfilename(title="上传第一份文件")
    selected_files[0] = file_path
    print("已上传第一份文件：" + file_path)

def select_file2():
    # 通过对话框选择第二份文件路径
    file_path = filedialog.askopenfilename(title="上传第二份文件")
    selected_files[1] = file_path
    print("已上传第二份文件：" + file_path)

def save_file():
    # 通过对话框选择保存文件路径
    output_path = filedialog.asksaveasfilename(title="保存文件", defaultextension=".xlsx")

    # 检查文件类型，根据不同类型进行处理
    dataframes = []
    for file in selected_files:
        if file is not None:
            file_extension = os.path.splitext(file)[1]
            if file_extension == '.xlsx':
                df = pd.read_excel(file,engine='openpyxl',header=None)
                dataframes.append(df)
            elif file_extension == '.csv':
                df = pd.read_csv(file,header=None)
                dataframes.append(df)
            else:
                print("不支持的文件类型：" + file_extension)

    if len(dataframes) != 2:
        print("请上传两份文件（xlsx 或 csv）")
        return

    # 获取两份文件的第一列数据，合并并去除重复行
    diff_rows = set(dataframes[0].iloc[:, 0]).symmetric_difference(set(dataframes[1].iloc[:, 0]))

    # 根据不同的行数据，从原始数据中筛选出所有对应的行，并合并为一个新的 DataFrame
    result_df = pd.concat([df[df.iloc[:, 0].isin(diff_rows)] for df in dataframes])

    # 将结果保存到新的 Excel 文件中
    result_df.to_excel(output_path, index=False,header=None)

    print("已保存新的 Excel 文件到：" + output_path)

root = Tk()
root.title("文件选择与保存")
root.geometry("400x200")

selected_files = [None, None]

# 第一行：上传第一份文件按钮
select_button1 = Button(root, text="上传第一份文件", command=select_file1)
select_button1.pack(pady=10)

# 第二行：上传第二份文件按钮
select_button2 = Button(root, text="上传第二份文件", command=select_file2)
select_button2.pack(pady=10)

# 第三行：保存文件按钮
save_button = Button(root, text="保存文件", command=save_file)
save_button.pack(pady=10)

root.mainloop()
