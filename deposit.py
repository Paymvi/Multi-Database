import argparse
from context import ApplicationContext
from application.deposit_use_case import DepositUseCase
from decimal import Decimal
from decimal import InvalidOperation


def main(account_id: int, amount: Decimal):

    # Creates the application context (for the .env, database connections, and making transaction manager)
    ctx = ApplicationContext()
    use_case = ctx.deposit_use_case

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
    parser.add_argument("amount", type=str)
    args = parser.parse_args()

    try:
        amount = Decimal(args.amount)
    except InvalidOperation:
        raise ValueError("Invalid monetary amount")

    main(args.account_id, amount)