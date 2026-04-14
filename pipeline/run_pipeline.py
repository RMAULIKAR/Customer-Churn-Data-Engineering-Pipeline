from pipeline.data_loader import load_raw_data
from pipeline.reset_tables import reset_tables
from ml.train_model import train_model
from ml.predict import run_predictions


def main():

    print("\nStarting Pipeline\n") 

    print("1. Resetting tables...")
    reset_tables()

    print("2. Loading data...")
    load_raw_data()

    print("3. Training model...")
    train_model()

    print("4. Running predictions...")
    run_predictions()


    print("\nPipeline completed successfully\n")


if __name__ == "__main__":
    main()