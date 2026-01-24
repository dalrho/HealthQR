# Use Node 20 (LTS) to meet the >=20.9.0 requirement
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the code
COPY . .

# Set production environment
ENV NODE_ENV production

# Now this should pass!
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]