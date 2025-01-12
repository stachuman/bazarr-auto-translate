# bazarr-auto-translate

This project automatically downloads and translates subtitles for episodes and movies using the Bazarr API.

Based on [Bazarr_AutoTranslate](https://github.com/anast20sm/Bazarr_AutoTranslate).

## Requirements

- Docker
- Bazarr API key

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/bazarr-auto-translate.git
    cd bazarr-auto-translate
    ```

2. Create a `requirements.txt` file with the following content:
    ```plaintext
    requests
    croniter
    ```

3. Build the Docker image:
    ```sh
    docker build -t bazarr-auto-translate .
    ```

## Environment Variables

- `BAZARR_HOSTNAME`: The hostname of your Bazarr instance (default: `localhost`).
- `BAZARR_PORT`: The port of your Bazarr instance (default: `6767`).
- `BAZARR_APIKEY`: Your Bazarr API key.
- `CRON_SCHEDULE`: The cron schedule for running the script (default: `*/5 * * * *`).
- `FIRST_LANG`: The first language code for subtitles (default: `pl`).
- `SECOND_LANG`: The second language code for subtitles (default: empty).

## Running the Container

Run the Docker container with the necessary environment variables:
```sh
docker run -e BAZARR_HOSTNAME=your_bazarr_hostname \
           -e BAZARR_PORT=your_bazarr_port \
           -e BAZARR_APIKEY=your_bazarr_apikey \
           -e CRON_SCHEDULE='0 6 * * *' \
           -e FIRST_LANG=pl \
           -e SECOND_LANG='' \
           bazarr-auto-translate
```

The script will run according to the specified cron schedule, downloading and translating subtitles as needed.

## Pre-built Docker Image

A pre-built Docker image is also available. You can pull and run it directly from Docker Hub:
```sh
docker pull maclucky/bazarr-auto-translate:latest
docker run -e BAZARR_HOSTNAME=your_bazarr_hostname \
           -e BAZARR_PORT=your_bazarr_port \
           -e BAZARR_APIKEY=your_bazarr_apikey \
           -e CRON_SCHEDULE='0 6 * * *' \
           -e FIRST_LANG=pl \
           -e SECOND_LANG='' \
           maclucky/bazarr-auto-translate:latest
```

