import argparse
import os

from context import ApplicationContext

def main():

    # Initialize application context
    ctx = ApplicationContext()

    try:
        check_status = ctx.check_use_case.check_databases()

        if not check_status:
            print(f"Databases check failed.")
            os.exit(1)
        else:
            print(check_status.message)
            print(f"Inconsistent Accounts: {check_status.accounts}")
    finally:
        # Shutdown the application context
        ctx.shutdown()


if __name__ == "__main__":
    main()