import argparse
import sys
from decimal import Decimal, InvalidOperation

from context import ApplicationContext


def main(account_id: int, amount: str) -> None:
    try:
        amount = Decimal(amount)
    except InvalidOperation:
        print('Amount must be a valid decimal value.')
        sys.exit(1)

    ctx = ApplicationContext()

    account = ctx.withdraw_use_case.withdraw(account_id, amount)
    if account is None:
        print('Withdraw failed. Check account ID and available balance.')
        sys.exit(1)

    print('Withdraw successful.')
    print(f'Account ID: {account.id}')
    print(f'Account Name: {account.name}')
    print(f'Updated Balance: {account.balance}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Withdraw amount from an account')
    parser.add_argument('account_id', type=int, help='The ID of the account to withdraw from')
    parser.add_argument('amount', type=str, help='The amount to withdraw')
    args = parser.parse_args()
    main(args.account_id, args.amount)