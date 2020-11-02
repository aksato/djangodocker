FROM node:14

WORKDIR /app
COPY package*.json /app/
COPY webpack.config.js /app/
COPY .babelrc /app/
RUN npm install

CMD ["npm", "start"]
