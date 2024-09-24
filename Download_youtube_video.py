import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import io
import urllib.request
import tempfile
import yt_dlp as youtube_dl  # Importando yt-dlp
from moviepy.editor import *

def remover_caracteres_invalidos(filename):
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def fazer_download():
    url = entrada_url.get()
    pasta_saida = label_pasta_saida.cget("text")[18:].strip()
    formato = formato_var.get()
    resolucao = resolucao_var.get()

    try:
        ydl_opts = {
            'format': 'bestaudio/best' if formato == "mp3" else f'bestvideo[height<={resolucao}]+bestaudio/best',
            'outtmpl': os.path.join(pasta_saida, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }] if formato == "mp3" else []
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            messagebox.showinfo("Download Concluído", f"{formato.upper()} download de '{title}' concluído com sucesso!")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {str(e)}")

def ao_clicar_em_escolher_pasta_saida():
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        label_pasta_saida.config(text=f"Pasta selecionada: {pasta_selecionada}")

def mostrar_detalhes_video(event):
    url = entrada_url.get()
    try:
        with youtube_dl.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            titulo_video.config(text=info_dict.get('title', 'Título não encontrado'))
            img_data = urllib.request.urlopen(info_dict.get('thumbnail')).read()
            imagem = Image.open(io.BytesIO(img_data))
            imagem.thumbnail((120, 120))
            imagem = ImageTk.PhotoImage(imagem)
            label_imagem.config(image=imagem)
            label_imagem.image = imagem
    except Exception as e:
        titulo_video.config(text="Erro ao carregar detalhes do vídeo")

app = tk.Tk()
app.title("Download de Vídeos")
app.geometry("400x600")
app.configure(bg="#f0f0f0")

titulo_video = tk.Label(app, text="Título do vídeo", bg="#f0f0f0", font=("Arial", 14, "bold"))
titulo_video.pack(pady=10)

label_imagem = tk.Label(app, bg="#f0f0f0")
label_imagem.pack(pady=10)

label_url = tk.Label(app, text="Insira a URL do vídeo:", bg="#f0f0f0", font=("Arial", 12))
label_url.pack()

entrada_url = tk.Entry(app, width=40, font=("Arial", 12))
entrada_url.pack()

label_formato = tk.Label(app, text="Escolha o formato do download:", bg="#f0f0f0", font=("Arial", 12))
label_formato.pack(pady=10)

formato_var = tk.StringVar()
formato_var.set("mp3")

opcoes_formato = [("MP3", "mp3"), ("MP4", "mp4")]

for texto, formato in opcoes_formato:
    radio = tk.Radiobutton(app, text=texto, variable=formato_var, value=formato, bg="#f0f0f0", font=("Arial", 12))
    radio.pack()

label_resolucao = tk.Label(app, text="Escolha a resolução:", bg="#f0f0f0", font=("Arial", 12))
label_resolucao.pack(pady=10)

resolucao_var = tk.StringVar()
resolucao_var.set("360p")

opcoes_resolucao = ["144p", "240p", "360p", "480p", "720p", "1080p"]

resolucao_combobox = Combobox(app, values=opcoes_resolucao, state="readonly", textvariable=resolucao_var, font=("Arial", 12))
resolucao_combobox.pack()

botao_pasta_saida = tk.Button(app, text="Escolher pasta de saída", command=ao_clicar_em_escolher_pasta_saida, font=("Arial", 12), bg="#cccccc", fg="black")
botao_pasta_saida.pack(pady=10)

label_pasta_saida = tk.Label(app, text="Nenhuma pasta selecionada.", bg="#f0f0f0", font=("Arial", 12))
label_pasta_saida.pack()

botao_fazer_download = tk.Button(app, text="Fazer Download", command=fazer_download, font=("Arial", 12), bg="#cccccc", fg="black")
botao_fazer_download.pack(pady=20)

entrada_url.bind("<KeyRelease>", mostrar_detalhes_video)

app.mainloop()
