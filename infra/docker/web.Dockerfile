FROM node:22-alpine

WORKDIR /app

COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci

COPY apps/web /app
RUN npm run build

EXPOSE 3000

CMD sh -c "npm run start -- --hostname 0.0.0.0 --port ${PORT:-3000}"
