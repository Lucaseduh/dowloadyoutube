import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from pytube import YouTube
from PIL import Image, ImageTk
import io
import urllib.request
import tempfile
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
        yt = YouTube(url)

        if formato == "mp3":
            audio_stream = yt.streams.filter(only_audio=True).first()
            if audio_stream:
                nome_arquivo = remover_caracteres_invalidos(yt.title) + '.mp3'
                caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
                
                # Salvando o áudio em um arquivo temporário
                audio_tempfile = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
                audio_stream.download(output_path=tempfile.gettempdir(), filename=audio_tempfile.name)
                audio_tempfile.close()
                
                # Converter para MP3 com bitrate de 320 kbps
                audio_clip = AudioFileClip(audio_tempfile.name)
                audio_clip.write_audiofile(caminho_arquivo, bitrate='320k', codec='libmp3lame')
                
                os.remove(audio_tempfile.name)

                messagebox.showinfo("Download Concluído", "Download em MP3 concluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível encontrar o áudio.")

        elif formato == "mp4":
            video_stream = yt.streams.filter(file_extension='mp4', progressive=True, res=resolucao).first()

            # Se não encontrar na resolução desejada, pega a melhor disponível
            if not video_stream:
                video_stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()

            if video_stream:
                nome_arquivo = remover_caracteres_invalidos(yt.title) + '.mp4'
                caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)
                video_stream.download(output_path=pasta_saida, filename=nome_arquivo)
                messagebox.showinfo("Download Concluído", "Download em MP4 concluído com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível encontrar o vídeo na resolução selecionada ou em qualquer outra disponível.")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o download: {str(e)}")

def ao_clicar_em_escolher_pasta_saida():
    pasta_selecionada = filedialog.askdirectory()
    if pasta_selecionada:
        label_pasta_saida.config(text=f"Pasta selecionada: {pasta_selecionada}")

def mostrar_detalhes_video(event):
    url = entrada_url.get()
    try:
        yt = YouTube(url)
        titulo_video.config(text=yt.title)
        img_data = urllib.request.urlopen(yt.thumbnail_url).read()
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

botao_fazer_download = tk.Button(app, text="Fazer Download", command=fazer_download, font=("Arial", 12), bg="#cccccc", fg="black")
botao_fazer_download.pack(pady=20)

botao_pasta_saida = tk.Button(app, text="Escolher pasta de saída", command=ao_clicar_em_escolher_pasta_saida, font=("Arial", 12), bg="#cccccc", fg="black")
botao_pasta_saida.pack(pady=10)

label_pasta_saida = tk.Label(app, text="Nenhuma pasta selecionada.", bg="#f0f0f0", font=("Arial", 12))
label_pasta_saida.pack()

entrada_url.bind("<KeyRelease>", mostrar_detalhes_video)

app.mainloop()
