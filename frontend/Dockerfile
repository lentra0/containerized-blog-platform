FROM node:18.20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund --silent
COPY . .
RUN npm run build

FROM node:18.20-alpine AS runner
WORKDIR /app

RUN addgroup -S app && adduser -S app -G app

COPY --from=builder /app .

USER app

EXPOSE 3000
ENV NODE_ENV=production
CMD ["npm", "start"]