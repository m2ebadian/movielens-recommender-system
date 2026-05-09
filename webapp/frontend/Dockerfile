FROM node:20-alpine

WORKDIR /app

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

COPY package.json ./

RUN npm install

COPY . .

RUN npm run build

RUN npm install -g serve

EXPOSE 8080

CMD ["serve", "-s", "dist", "-l", "8080"]