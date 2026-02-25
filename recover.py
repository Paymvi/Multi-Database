import argparse
import os

from context import ApplicationContext

def main():

    # Initialize application context
    ctx = ApplicationContext()

    try:
        ctx.recover_use_case.recover()
        print(f"Recovered.")
    finally:
        # Shutdown the application context
        ctx.shutdown()


if __name__ == "__main__":
    main()