# Client Server Face Collector

Simple Flask and Keras application to run a client-server application of face recognition to automatically change "ephemeral" parameters.

## Prerequisites

- Windows 7+ with support of Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017 and 2019 compiler *OR* Ubuntu 16.04+ *OR* MacOS 10.12.6+ 64 bit
- Python 3.6+
- Microsoft Office Access

## Installation

1. `git clone` the repository.
2. Install requirements: `pip install -r requirements.txt`

## Usage

1) Launch `server/server.py`
2) Navigate to `http://127.0.0.1:8000/`
3) Enter the user number

Refresh the page if the number entered was not accepted.

4) Launch `main.py`

If the entered user number is in the database, the program will begin face identification and, after the face has been confirmed as related to the user number, the parameters in the `mainInfo.json` will change. After that, the program will start collecting more images of the user for better classification one in every 5 seconds.

To stop the program, enter `s` int the command line.

After the client has been stopped, the CNN is being trained again with the new images and rewriting of the user parameters in case the user changed them is performed. Also a new log entry is recorded into the database.

If the user number was not found in the database, the identification part is being skipped and the rest is the same.

If the user number does not match the detected face, after three of such occurrences, the program will stop and write an error to the log.
