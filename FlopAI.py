import tkinter as tk
from tkinter import scrolledtext
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# ========== MODELO Y TOKENIZADOR ==========
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token  # Evita errores de padding
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.resize_token_embeddings(len(tokenizer))
model.eval()

# ========== FUNCIÓN DE GENERACIÓN ==========
def generate_text(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            inputs.input_ids,
            max_length=max_length,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# ========== INTERFAZ GRÁFICA ==========
window = tk.Tk()
window.title("FlopAI")

tk.Label(window, text="Escribe tu pregunta o prompt:").pack(pady=5)
entry = tk.Entry(window, width=60)
entry.pack(pady=5)

def process():
    prompt = entry.get()
    generated_text = generate_text(prompt, max_length=50)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, generated_text)

tk.Button(window, text="Procesar", command=process).pack(pady=10)

output_text = scrolledtext.ScrolledText(window, width=80, height=15)
output_text.pack(padx=10, pady=10)

window.mainloop()
