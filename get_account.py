import argparse
import os

from context import ApplicationContext

def main(account_id: str):

    # Initialize application context
    ctx = ApplicationContext()

    try:

        # Use the GetAccountUseCase to retrieve account information
        account = ctx.get_account_use_case.get_account(account_id)

        if not account:
            print(f"Account with ID {account_id} not found.")
            os.exit(1)
        else:
            print(f"Account ID: {account.id}")
            print(f"Account Name: {account.name}")
            print(f"Account Balance: {account.balance}")
    finally:
        # Shutdown the application context
        ctx.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get account information")
    parser.add_argument("--debug", "-d", action="store_true", help="Enable debug mode")
    parser.add_argument("account_id", type=int, help="The ID of the account to retrieve")
    args = parser.parse_args()
    main(args.account_id)