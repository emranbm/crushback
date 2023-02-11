FROM node:16.16.0-alpine3.15 as build-env
WORKDIR /app/
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.23.0-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /docker-entrypoint.d/40-crushback-entrypoint.sh
RUN chmod +x /docker-entrypoint.d/40-crushback-entrypoint.sh
COPY --from=build-env /app/build/ /app/frontend/
