"""Collect tweets."""

from database import Database
from twitter import CollectResponse, ProcessedResponse


def main(search_term) -> None:
    """Execute all functions."""
    response: CollectResponse = CollectResponse(search_term)
    processed_response: ProcessedResponse = ProcessedResponse(response)
    database: Database = Database(processed_response.get_tables())
    database.commit_data()
    print("Completed.")


if __name__ == '__main__':
    main("CPIM")
