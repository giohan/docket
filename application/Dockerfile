FROM node:argon

# Create app directory
RUN mkdir -p /usr/src/app
RUN mkdir -p /var/log/application
WORKDIR /usr/src/app

# Install app dependencies
COPY package.json /usr/src/app/
RUN npm install

# Bundle app source
COPY . /usr/src/app

EXPOSE 8080
# CMD [ "npm", "start" ]
CMD ["/bin/sh", "-c", "npm start >> /var/log/application/server.log 2>&1"]
