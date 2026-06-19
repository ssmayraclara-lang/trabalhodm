

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import urllib.request
import urllib.parse
import threading
from html.parser import HTMLParser



class ExtratorInfoSite(HTMLParser):
    def __init__(self):
        super().__init__()
        self.no_title = False
        self.no_script = False
        self.no_style = False

        self.title = ""
        self.description = ""
        self.headings = []
        self.links = []
        self.text_parts = []

        self._current_heading = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "title":
            self.no_title = True

        elif tag == "script":
            self.no_script = True

        elif tag == "style":
            self.no_style = True

        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._current_heading = tag.upper()

        elif tag == "a":
            href = attrs.get("href", "").strip()
            if href:
                self.links.append(href)

        elif tag == "meta":
            name = attrs.get("name", "").lower()
            content = attrs.get("content", "").strip()

            if name == "description" and content:
                self.description = content

    def handle_endtag(self, tag):
        if tag == "title":
            self.no_title = False

        elif tag == "script":
            self.no_script = False

        elif tag == "style":
            self.no_style = False

        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._current_heading = None

    def handle_data(self, data):
        texto = data.strip()
        if not texto:
            return

        if self.no_script or self.no_style:
            return

        if self.no_title:
            self.title += texto + " "

        if self._current_heading:
            self.headings.append(f"{self._current_heading}: {texto}")

        self.text_parts.append(texto)

    def resultado(self):
        texto_visivel = " ".join(self.text_parts)
        texto_visivel = " ".join(texto_visivel.split())

        # Remove links repetidos e limita a quantidade
        links_unicos = []
        for link in self.links:
            if link not in links_unicos:
                links_unicos.append(link)

        return {
            "title": self.title.strip(),
            "description": self.description.strip(),
            "headings": self.headings,
            "links": links_unicos[:100],
            "text": texto_visivel,
        }


class WebViewerSimples:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Viewer Simples")
        self.root.geometry("1100x750")

        self.arquivo_atual = None

        self.criar_interface()

    def criar_interface(self):
        # Parte de cima
        topo = ttk.Frame(self.root, padding=10)
        topo.pack(fill="x")

        ttk.Label(topo, text="URL:").pack(side="left")

        self.url_var = tk.StringVar(value="https://example.com")
        self.url_entry = ttk.Entry(topo, textvariable=self.url_var)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)

        ttk.Button(topo, text="Buscar site", command=self.buscar_site).pack(side="left", padx=4)
        ttk.Button(topo, text="Abrir arquivo", command=self.abrir_arquivo).pack(side="left", padx=4)
        ttk.Button(topo, text="Salvar", command=self.salvar_arquivo).pack(side="left", padx=4)

        # Área de informações
        frame_info = ttk.LabelFrame(self.root, text="Informações do site", padding=8)
        frame_info.pack(fill="both", expand=False, padx=10, pady=(0, 10))

        self.caixa_info = ScrolledText(frame_info, height=10, wrap="word", font=("Arial", 10))
        self.caixa_info.pack(fill="both", expand=True)

        # Área de texto principal
        frame_texto = ttk.LabelFrame(self.root, text="Texto visível da página", padding=8)
        frame_texto.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.caixa_texto = ScrolledText(frame_texto, wrap="word", font=("Consolas", 10))
        self.caixa_texto.pack(fill="both", expand=True)

        # Barra de status
        self.status = ttk.Label(self.root, text="Pronto", anchor="w")
        self.status.pack(fill="x", padx=10, pady=(0, 8))

    def set_status(self, texto):
        self.status.config(text=texto)
        self.root.update_idletasks()

    def buscar_site(self):
        url = self.url_var.get().strip()

        if not url:
            messagebox.showwarning("Aviso", "Digite uma URL.")
            return

        if not url.startswith(("http://", "https://")):
            messagebox.showwarning("Aviso", "A URL deve começar com http:// ou https://")
            return

        self.set_status("Baixando página...")
        threading.Thread(target=self._baixar_pagina, args=(url,), daemon=True).start()

    def _baixar_pagina(self, url):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            with urllib.request.urlopen(req, timeout=25) as response:
                html_bytes = response.read()
                charset = response.headers.get_content_charset() or "utf-8"
                html = html_bytes.decode(charset, errors="replace")

            # Extrair informações
            parser = ExtratorInfoSite()
            parser.feed(html)
            info = parser.resultado()

            # Montar texto de informações
            texto_info = []
            texto_info.append(f"URL: {url}")
            texto_info.append(f"Tamanho da página: {len(html_bytes):,} bytes")
            texto_info.append(f"Charset: {charset}")
            texto_info.append("")

            texto_info.append(f"Título: {info['title'] or '(não encontrado)'}")
            texto_info.append(f"Descrição: {info['description'] or '(não encontrado)'}")
            texto_info.append("")

            texto_info.append("Cabeçalhos:")
            if info["headings"]:
                for h in info["headings"][:50]:
                    texto_info.append(f"  - {h}")
            else:
                texto_info.append("  (nenhum encontrado)")
            texto_info.append("")

            texto_info.append("Links:")
            if info["links"]:
                for link in info["links"][:50]:
                    texto_info.append(f"  - {link}")
            else:
                texto_info.append("  (nenhum encontrado)")
            texto_info.append("")

            texto_info.append("Texto visível da página:")
            texto_info.append(info["text"] if info["text"] else "(nenhum texto encontrado)")

            # Atualizar a interface na thread principal
            self.root.after(0, lambda: self.mostrar_resultado("\n".join(texto_info), info["text"], url))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))
            self.root.after(0, lambda: self.set_status("Erro ao buscar site"))

    def mostrar_resultado(self, info, texto, url):
        self.caixa_info.delete("1.0", tk.END)
        self.caixa_info.insert("1.0", info)

        self.caixa_texto.delete("1.0", tk.END)
        self.caixa_texto.insert("1.0", texto)

        self.arquivo_atual = None
        self.set_status(f"Site carregado: {url}")

    def abrir_arquivo(self):
        nome = filedialog.askopenfilename(
            title="Abrir arquivo",
            filetypes=[
                ("Arquivos de texto", "*.txt *.md *.csv *.log"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not nome:
            return

        try:
            with open(nome, "r", encoding="utf-8", errors="replace") as f:
                conteudo = f.read()

            self.caixa_texto.delete("1.0", tk.END)
            self.caixa_texto.insert("1.0", conteudo)

            self.caixa_info.delete("1.0", tk.END)
            self.caixa_info.insert("1.0", f"Arquivo aberto:\n{nome}")

            self.arquivo_atual = nome
            self.set_status(f"Arquivo aberto: {nome}")

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def salvar_arquivo(self):
        nome = filedialog.asksaveasfilename(
            title="Salvar arquivo",
            defaultextension=".txt",
            filetypes=[
                ("Arquivo de texto", "*.txt"),
                ("Todos os arquivos", "*.*")
            ]
        )

        if not nome:
            return

        try:
            conteudo = self.caixa_texto.get("1.0", tk.END)

            with open(nome, "w", encoding="utf-8") as f:
                f.write(conteudo)

            self.set_status(f"Salvo em: {nome}")

        except Exception as e:
            messagebox.showerror("Erro", str(e))


def main():
    root = tk.Tk()

    try:
        style = ttk.Style()
        style.theme_use("clam")
    except:
        pass

    WebViewerSimples(root)
    root.mainloop()


if __name__ == "__main__":
    main()
