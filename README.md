# Consistent Finance

Consistent Finance is a command-line (CLI) program designed to demonstrate how the Two-Phase Commit (2PC) protocol preserves data consistency across distributed database instances. The project also explores the advantages and limitations of 2PC in failure scenarios.

This project was developed as a team project for a database course.

## Features

- Demonstrates the Two-Phase Commit (2PC) protocol in a distributed database environment.
- Simulates failure scenarios (e.g., database crashes, network disruptions) using VSCode breakpoints.
- Provides a recovery mechanism to restore databases to a consistent state based on pending transactions.
- Includes a consistency checker to verify data integrity across databases.

## Architecture

The system consists of two PostgreSQL database instances:
- **Account DB**: Stores user account balances.
- **Ledger DB**: Stores an immutable log of all transactions (deposits and withdrawals).

A Two-Phase Commit coordinator manages distributed transactions across these two databases to ensure atomicity and data consistency. The coordinator persists state transitions in a durable log (SQLite) to ensure recovery safety.

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- `uv` (Python package manager)

## Setup Instructions

1. **Start the databases**
   The project uses Docker Compose to run two PostgreSQL instances.

   ```bash
   docker-compose -f database/docker-compose.yml up -d
   ```

2. **Initialize the databases**
   Apply the schema and initial data to the databases:
   ```bash
   PGPASSWORD=finance_pw psql -h localhost -p 5433 -U finance -d account_db -f database/schema_account_db.sql
   PGPASSWORD=finance_pw psql -h localhost -p 5434 -U finance -d ledger_db -f database/schema_ledger_db.sql
   ```

3. **Install dependencies**
   The project uses `uv` for dependency management.
   ```bash
   uv sync
   source .venv/bin/activate
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory with the following content:
   ```env
   ACCOUNT_DB_URL=postgresql://finance:finance_pw@localhost:5433/account_db
   LEDGER_DB_URL=postgresql://finance:finance_pw@localhost:5434/ledger_db
   ```

## Usage

The project provides several CLI entry points at the root directory:

- **Get Account Balance**:
  ```bash
  python get_account.py <account_id>
  ```

- **Deposit Funds**:
  ```bash
  python deposit.py <account_id> <amount>
  ```

- **Withdraw Funds**:
  ```bash
  python withdraw.py <account_id> <amount>
  ```

- **Check Data Consistency**:
  Verifies that the sum of all ledger entries equals the stored account balance for every account.
  ```bash
  python check.py
  ```

- **Recover Pending Transactions**:
  Moves the databases to a consistent state according to the pending transactions' state in the durable log.
  ```bash
  python recover.py
  ```

## Demonstration Guide

The primary goal of this project is to demonstrate the 2PC protocol and its behavior during failures.

1. **Normal Operation (Happy Path)**:
   Run a deposit or withdrawal and observe the successful transaction across both databases.

2. **Simulating Failures**:
   - Open the project in VSCode.
   - Set breakpoints in the 2PC coordinator code (e.g., `data_access/coordinator/two_phase_commit_coordinator.py`) during different steps of the protocol (e.g., after PREPARE, before COMMIT).
   - Run the CLI scripts using the VSCode debugger.
   - When execution pauses at a breakpoint, simulate a failure by:
     - Shutting down a database container: `docker stop account_db` or `docker stop ledger_db`.
     - Killing the Python program to simulate a coordinator crash.

3. **Recovery**:
   - Restart any stopped database containers: `docker start account_db` or `docker start ledger_db`.
   - Run `python recover.py` to resolve any pending transactions (either committing or aborting them based on the durable log).
   - Run `python check.py` to verify that data consistency has been maintained despite the failure.
