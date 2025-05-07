# 🌆 Stability AI - Image Generator

Gerador de imagens que utiliza modelo de inteligência artificial dá Stability, para criar artes digitais a partir de descrições textuais. Desenvolvido com Python e Streamlit, oferece uma interface simples e intuitiva para usuários que desejam explorar o potencial criativo da IA.

## 🖼️ Projeto:
![Pagina Inicial](./assets/image.png)

## 🚀 Funcionalidades

* 🎯 Prototipagem visual rápida
* 💡 Geração de ilustrações para blogs

## ⚙️ Pré-requisitos

* Python 3.10+
* Conta no Stability AI
* Conexão com internet

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/yyhago/stabilityai-imagegene.git
cd stabilityai-imagegene
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Crie um arquivo .env na raiz do projeto:
```bash
STABILITY_API_KEY=sua_chave_aqui
```

## 🖥️ Como Usar

1. Execute o aplicativo:
```bash
streamlit run src/main.py
```

No navegador, digite sua mensagem e interaja com a IA!

## 🧩 Estrutura do Projeto

```
stabilityai-imagegene/
├── src/
│   ├── main.py             # Interface principal (Streamlit)
│   └── image_generator.py  # Integração com a API Gemini e Configuração
│   └── style.css           # Estilização CSS
├── .env                    # Configurações sensíveis
├── requirements.txt        # Dependências
└── README.md               # Documentação
```