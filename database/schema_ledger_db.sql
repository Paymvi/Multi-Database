CREATE TABLE "ledger" (
    "id" SERIAL PRIMARY KEY,
    "account_id" INT NOT NULL,
    "type" VARCHAR(10) NOT NULL,
    "amount" DECIMAL(10, 2) NOT NULL,
    "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "ledger" (account_id, type, amount) VALUES 
    (1, 'deposit', 1000.00),
    (2, 'deposit', 1500.00),
    (3, 'deposit', 2000.00);