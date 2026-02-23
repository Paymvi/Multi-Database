import argparse
from context import ApplicationContext
from application.deposit_use_case import DepositUseCase
from decimal import Decimal


def main(account_id: int, amount: float):

    # Creates the application context (for the .env, database connections, and making transaction manager)
    ctx = ApplicationContext()
    use_case = DepositUseCase(ctx.tx_manager)

    # Run deposit operation
    updated = use_case.deposit(account_id, amount)

    # Print confirmation
    print("Deposit complete!")
    print(f"Account ID: {updated.id}")
    print(f"Account Name: {updated.name}")
    print(f"New Balance: {updated.balance:.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("account_id", type=int)
    parser.add_argument("amount", type=float)
    args = parser.parse_args()

    amount = Decimal(str(args.amount))
    main(args.account_id, amount)