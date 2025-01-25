# Use a imagem base do Node.js
FROM node:20

# Defina o diretório de trabalho no contêiner
WORKDIR /usr/src/app

# Copie o package.json e o package-lock.json (se existir)
COPY package.json package-lock.json ./

# Instale as dependências do projeto
RUN npm install

# Copie o restante do código do projeto para o contêiner
COPY . .

# Compile o TypeScript para JavaScript
RUN npm run build

# Exponha a porta que a aplicação irá rodar
EXPOSE 3000

# Defina o comando padrão para iniciar a aplicação
CMD [ "npm", "start" ]
