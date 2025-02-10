# Define a imagem base (sistema operacional host).
FROM python:3.11-alpine

# Definir o diretório de trabalho.
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho.
COPY requirements.txt ./

# Instalar as dependências do projeto.
RUN pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos do projeto para o diretório de trabalho.
COPY . .

# Expor a porta da aplicação.
EXPOSE 5000

# Iniciar a aplicação.
CMD ["python", "app.py"]