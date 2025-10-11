from fdp.orchestration.runner import run_pipeline


def main():
    """Entry point for the Federal Data Processor"""
    run_pipeline("federal_register_daily")

if __name__ == "__main__":
    main()