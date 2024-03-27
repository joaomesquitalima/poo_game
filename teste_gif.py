from PIL import Image
import os
def extract_frames_from_gif(gif_file, output_folder):
    try:
        gif = Image.open(gif_file)

        # Garanta que o diretório de saída exista
        os.makedirs(output_folder, exist_ok=True)

        # Extraia cada frame do GIF
        while True:
            try:
                frame = gif.copy()
                frame.save(os.path.join(output_folder, f"frame_{gif.tell():03d}.png"))
                gif.seek(gif.tell() + 1)
            except EOFError:
                break

        print("Frames extraídos com sucesso.")
    except IOError:
        print("Erro ao abrir o arquivo GIF.")

# Caminho para o arquivo GIF de entrada
gif_file = "brain_boss.gif"

# Pasta de saída para os frames PNG
output_folder = "frames_output"

# Extraia os frames do GIF e salve-os como imagens PNG
extract_frames_from_gif(gif_file, output_folder)
