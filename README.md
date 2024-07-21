# Web Scraping Tool with FastAPI

This project is a web scraping tool built with Python's FastAPI framework. It scrapes product information (name, price, image) from [dentalstall.com](https://dentalstall.com/shop/) and stores the data in a local JSON file.

## Project Structure

### `app/`

- **`__init__.py`**: Initializes the `app` package.
- **`main.py`**: Contains the FastAPI application and endpoint definitions.
- **`models.py`**: Defines the data model for product information using Pydantic.
- **`scraper.py`**: Implements the `Scraper` class that handles the web scraping logic.
- **`settings.py`**: Contains configuration settings for the scraper, including page limit and proxy settings.
- **`utils.py`**: Utility functions for saving and loading data to/from JSON files.

### `requirements.txt`

Lists all the dependencies required for the project.

### `run.py`

The entry point to run the FastAPI application.

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/web-scraping-tool.git
    cd web-scraping-tool
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    ```bash
    source venv/bin/activate
    ```

4. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the FastAPI application**:

    ```bash
    python run.py
    ```

2. **Test the scraping endpoint**:

    You can test the endpoint using Postman or Curl:

    ```bash
    curl -X POST "http://127.0.0.1:8000/scrape" -H "accept: application/json" -H "Authorization: Bearer test_token"
    ```

    The default page_limit is set to 5, you can change it in the `settings.py` file

### Data Storage

The scraped data is stored in a local JSON file (`products.json`). Images are downloaded and saved in the `images` directory.
