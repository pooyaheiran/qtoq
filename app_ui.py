import customtkinter as ctk
import tkinter.messagebox
from parser import parse_input
from graph import graph_drawer
from PIL import Image
import json


ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue") 

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("QTOQ • Automata Generator")
		self.geometry("1200x750")

		ctk.set_appearance_mode("dark")

		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(1, weight=1)

		# =========================
		# Header
		# =========================

		self.header = ctk.CTkFrame(
			self,
			height=80,
			corner_radius=0
		)
		self.header.grid(
			row=0,
			column=0,
			columnspan=2,
			sticky="ew"
		)

		self.title_label = ctk.CTkLabel(
			self.header,
			text="QTOQ",
			font=("JetBrains Mono", 28, "bold")
		)
		self.title_label.pack(
			anchor="w",
			padx=20,
			pady=(10, 0)
		)

		self.subtitle_label = ctk.CTkLabel(
			self.header,
			text="Finite Automata Generator",
			font=("JetBrains Mono", 12)
		)
		self.subtitle_label.pack(
			anchor="w",
			padx=22
		)

		# =========================
		# Sidebar
		# =========================

		self.sidebar = ctk.CTkFrame(
			self,
			width=200,
			corner_radius=0
		)
		self.sidebar.grid(
			row=1,
			column=0,
			sticky="ns"
		)

		self.sidebar.grid_propagate(False)

		self.btn_run = ctk.CTkButton(
			self.sidebar,
			text="▶ Run",
			command=self.on_run,
			height=45,
			corner_radius=10,
			font=("JetBrains Mono", 14)
		)
		self.btn_run.pack(
			fill="x",
			padx=15,
			pady=(20, 10)
		)

		self.btn_save = ctk.CTkButton(
			self.sidebar,
			text="💾 Save",
			command=self.on_save,
			height=45,
			corner_radius=10,
			font=("JetBrains Mono", 14)
		)
		self.btn_save.pack(
			fill="x",
			padx=15,
			pady=10
		)

		self.btn_open = ctk.CTkButton(
			self.sidebar,
			text="📂 Open",
			command=self.on_open,
			height=45,
			corner_radius=10,
			font=("JetBrains Mono", 14)
		)
		self.btn_open.pack(
			fill="x",
			padx=15,
			pady=10
		)

		self.btn_help = ctk.CTkButton(
			self.sidebar,
			text="❓ Help",
			command=self.on_help,
			height=45,
			corner_radius=10,
			font=("JetBrains Mono", 14)
		)
		self.btn_help.pack(
			fill="x",
			padx=15,
			pady=10
		)

		# =========================
		# Editor Area
		# =========================

		self.editor_frame = ctk.CTkFrame(
			self,
			corner_radius=15
		)

		self.editor_frame.grid(
			row=1,
			column=1,
			sticky="nsew",
			padx=15,
			pady=15
		)

		self.editor_frame.grid_rowconfigure(1, weight=1)
		self.editor_frame.grid_columnconfigure(0, weight=1)

		self.editor_title = ctk.CTkLabel(
			self.editor_frame,
			text="Automata Script",
			font=("JetBrains Mono", 18, "bold")
		)

		self.editor_title.grid(
			row=0,
			column=0,
			sticky="w",
			padx=20,
			pady=(15, 5)
		)

		self.textbox = ctk.CTkTextbox(
			self.editor_frame,
			wrap="word",
			font=("JetBrains Mono", 15),
			corner_radius=10
		)

		self.textbox.grid(
			row=1,
			column=0,
			sticky="nsew",
			padx=15,
			pady=(0, 15)
		)

		# =========================
		# Status Bar
		# =========================

		self.status_frame = ctk.CTkFrame(
			self,
			height=35,
			corner_radius=0
		)

		self.status_frame.grid(
			row=2,
			column=0,
			columnspan=2,
			sticky="ew"
		)

		self.status_label = ctk.CTkLabel(
			self.status_frame,
			text="🟢 Ready",
			font=("JetBrains Mono", 12)
		)

		self.status_label.pack(
			anchor="w",
			padx=15,
			pady=5
		)

	def on_run(self):
		text = self.textbox.get("1.0", "end-1c")
		try:
			parse_input(text)
			with open("db.json", "r") as f:
				user_input = json.load(f)
			graph_drawer(user_input)        
			self.update_status(f"loading...")

		except:
			self.update_status(f"ERROR")

		image_window = ctk.CTkToplevel(self)
		image_window.title("automata")
		image_window.geometry("900x600")
		
		
		img = Image.open("automata.png")
		my_image = ctk.CTkImage(img, size=(800,500))
			
		self.image_label = ctk.CTkLabel(image_window, image=my_image, text="")
		self.image_label.pack(pady=10)
		self.update_status(f"ready")


	def on_save(self):
		file_path = tkinter.filedialog.asksaveasfilename(
			defaultextension=".txt",
			filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
			title="Save Input Text"
		)

		if file_path:
			text = self.textbox.get("1.0", "end-1c")
			with open(file_path, "w") as f:
				f.write(text)
		else:
			self.update_status("canceled saving")

	def on_open(self):
		file_path = tkinter.filedialog.askopenfilename(
			filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
			title="Open Input Text"
		)
		with open(file_path, "r") as f:
			content = f.read()
		self.textbox.delete("1.0", "end")
		self.textbox.insert("1.0", content)

	def on_help(self):
		help_window = ctk.CTkToplevel(self)
		help_window.title("Help")
		help_window.geometry("400x100")
		
		frame = ctk.CTkFrame(help_window)
		frame.pack(expand=True, fill="both", padx=20, pady=20)
		
		github_url = "https://github.com/pooyaheiran/qtoq" 
		link_textbox = ctk.CTkTextbox(
			frame, 
			width=350, 
			height=100,
		)
		link_textbox.pack(pady=10)
		
		link_textbox.insert("1.0", github_url)
		link_textbox.configure(state="disabled")
	
		

	def update_status(self, message):

		if "error" in message.lower():
			self.status_label.configure(
				text=f"🔴 {message}"
			)

		elif "load" in message.lower():
			self.status_label.configure(
				text=f"🟡 {message}"
			)

		else:
			self.status_label.configure(
				text=f"🟢 {message}"
			)
