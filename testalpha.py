import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import pandas as pd
import json

class SpreadsheetApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Spreadsheet App")
        
        self.load_data()
        self.create_widgets()

    def load_data(self):
        try:
            # Đọc dữ liệu từ tệp JSON
            with open('data.json') as f:
                data = json.load(f)
            # Tạo DataFrame từ dữ liệu JSON
            self.data = pd.DataFrame(data)
        except FileNotFoundError:
            # Nếu không tìm thấy tệp JSON, tạo một DataFrame trống
            self.data = pd.DataFrame(columns=["Name", "Age", "City"])

    def create_widgets(self):
        self.table = tk.Frame(self.master)
        self.table.grid(row=0, column=0, padx=10, pady=10)

        self.entries = []  # Danh sách các ô nhập liệu

        # Tạo ô nhập liệu cho mỗi ô trong DataFrame
        for i, column in enumerate(self.data.columns):
            tk.Label(self.table, text=column).grid(row=0, column=i)
            for j in range(len(self.data)):
                entry = tk.Entry(self.table, width=10)
                entry.grid(row=j + 1, column=i)
                # Đặt giá trị của ô nhập liệu dựa trên dữ liệu từ DataFrame
                entry.insert(tk.END, str(self.data.iloc[j, i]))
                self.entries.append(entry)

        # Tạo nút để cập nhật dữ liệu
        self.update_button = tk.Button(self.master, text="Update Data", command=self.update_data)
        self.update_button.grid(row=1, column=0, padx=10, pady=5)

        # Tạo nút để thêm hàng mới
        self.add_row_button = tk.Button(self.master, text="Add Row", command=self.add_row)
        self.add_row_button.grid(row=1, column=1, padx=10, pady=5)

        # Tạo nút để xóa hàng
        self.delete_row_button = tk.Button(self.master, text="Delete Row", command=self.delete_row)
        self.delete_row_button.grid(row=1, column=2, padx=10, pady=5)

        # Tạo nút để thêm cột mới
        self.add_column_button = tk.Button(self.master, text="Add Column", command=self.add_column)
        self.add_column_button.grid(row=1, column=3, padx=10, pady=5)

    def update_data(self):
        try:
            # Lấy dữ liệu từ các ô nhập liệu và cập nhật DataFrame
            for entry in self.entries:
                row = entry.grid_info()["row"] - 1
                column = entry.grid_info()["column"]
                value = entry.get()
                self.data.iloc[row, column] = value

            # Hiển thị DataFrame đã cập nhật
            messagebox.showinfo("Success", "Data updated successfully!")
            print(self.data)

            # Cập nhật tệp JSON
            self.data.to_json('data.json', orient='records')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update data: {str(e)}")

    def add_row(self):
        # Thêm một hàng mới vào DataFrame và cập nhật giao diện người dùng
        new_row = pd.Series(["" for _ in range(len(self.data.columns))], index=self.data.columns)
        self.data = pd.concat([self.data, new_row.to_frame().T], ignore_index=True)
        self.update_ui()

    def delete_row(self):
        # Xóa hàng được chọn khỏi DataFrame và cập nhật giao diện người dùng
        try:
            selected_row = int(self.master.focus_get().grid_info()["row"]) - 1
            self.data.drop(index=selected_row, inplace=True)
            self.update_ui()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete row: {str(e)}")

    def add_column(self):
        # Yêu cầu người dùng nhập tên cột mới
        new_column_name = askstring("Add Column", "Enter name for new column:")
        if new_column_name:
            # Thêm cột mới vào DataFrame và cập nhật giao diện người dùng
            self.data[new_column_name] = ""
            self.update_ui()

    def update_ui(self):
        # Cập nhật giao diện người dùng với dữ liệu mới từ DataFrame
        for entry in self.entries:
            entry.grid_forget()
            entry.destroy()

        self.entries.clear()

        for i, column in enumerate(self.data.columns):
            tk.Label(self.table, text=column).grid(row=0, column=i)
            for j in range(len(self.data)):
                entry = tk.Entry(self.table, width=10)
                entry.grid(row=j + 1, column=i)
                entry.insert(tk.END, str(self.data.iloc[j, i]))
                self.entries.append(entry)

def main():
    root = tk.Tk()
    app = SpreadsheetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
