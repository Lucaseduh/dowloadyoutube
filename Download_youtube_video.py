import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
from pytube import YouTube
from PIL import Image, ImageTk
import io
import urllib.request

def remover_caracteres_invalidos(filename):
    # Remove caracteres inválidos em nomes de arquivo no Windows
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename

def fazer_download():
    url = entrada_url.get()
    pasta_saida = label_pasta_saida.cget("text")[18:].strip()  # Remove espaços em branco no início e no final
    formato = formato_var.get()
    resolucao = resolucao_var.get()

    try:
        yt = YouTube(url)

        # Filtrar a stream baseado no formato selecionado
        if formato == "mp4":
            video_stream = yt.streams.filter(file_extension='mp4', progressive=True, res=resolucao).first()
        else:
            video_stream = yt.streams.filter(only_audio=True).first()

        if not video_stream:
            print("Resolução não disponível. Baixando na maior resolução disponível.")
            video_stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()

        if video_stream:
            # Verifica se a pasta de saída existe e cria se não existir
            if not os.path.exists(pasta_saida):
                os.makedirs(pasta_saida)

            # Define o nome do arquivo
            nome_arquivo = remover_caracteres_invalidos(yt.title) + '.' + formato

            # Define o caminho completo do arquivo a ser baixado
            caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)

            # Faz o download
            video_stream.download(output_path=pasta_saida, filename=nome_arquivo)

            if formato == "mp4":
                messagebox.showinfo("Download Concluído", "Download em MP4 concluído com sucesso!")
            else:
                messagebox.showinfo("Download Concluído", "Download em MP3 concluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível encontrar o vídeo ou áudio na resolução selecionada.")
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

        # Carregar a miniatura do vídeo
        img_data = urllib.request.urlopen(yt.thumbnail_url).read()
        imagem = Image.open(io.BytesIO(img_data))
        imagem.thumbnail((120, 120))
        imagem = ImageTk.PhotoImage(imagem)
        label_imagem.config(image=imagem)
        label_imagem.image = imagem  # Garante que a imagem não seja coletada pelo garbage collector
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar os detalhes do vídeo: {str(e)}")

app = tk.Tk()
app.title("Download de Vídeos")
app.geometry("400x500")

titulo_video = tk.Label(app, text="Título do vídeo")
titulo_video.pack(pady=10)

label_imagem = tk.Label(app)
label_imagem.pack(pady=10)

label_url = tk.Label(app, text="Insira a URL do vídeo:")
label_url.pack()

entrada_url = tk.Entry(app, width=40)
entrada_url.pack()

label_formato = tk.Label(app, text="Escolha o formato do download:")
label_formato.pack(pady=10)

formato_var = tk.StringVar()
formato_var.set("mp4")

opcoes_formato = [
    ("MP4", "mp4"),
    ("MP3", "mp3")
]

for texto, formato in opcoes_formato:
    radio = tk.Radiobutton(app, text=texto, variable=formato_var, value=formato)
    radio.pack()

label_resolucao = tk.Label(app, text="Escolha a resolução:")
label_resolucao.pack(pady=10)

resolucao_var = tk.StringVar()
resolucao_var.set("360p")

opcoes_resolucao = ["144p", "240p", "360p", "480p", "720p", "1080p"]

resolucao_combobox = Combobox(app, values=opcoes_resolucao, state="readonly", textvariable=resolucao_var)
resolucao_combobox.pack()

botao_pasta_saida = tk.Button(app, text="Escolher pasta de saída", command=ao_clicar_em_escolher_pasta_saida)
botao_pasta_saida.pack(pady=10)

label_pasta_saida = tk.Label(app, text="Nenhuma pasta selecionada.")
label_pasta_saida.pack()

botao_fazer_download = tk.Button(app, text="Fazer Download", command=fazer_download)
botao_fazer_download.pack(pady=20)

entrada_url.bind("<KeyRelease>", mostrar_detalhes_video)

app.mainloop()
