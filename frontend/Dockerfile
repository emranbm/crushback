FROM node:16.16.0-alpine3.15 as build-env
WORKDIR /app/
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

FROM alpine:3.15
COPY update-frontend-files.sh /
COPY --from=build-env /app/build/ /app/
CMD sh /update-frontend-files.sh
