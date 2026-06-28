FROM rust:1.90

WORKDIR /app

COPY . .

RUN cargo build --release

CMD ["sh", "-c", "./target/release/auth-service"]
