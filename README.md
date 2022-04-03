# metropi

## Overview
This project is used to display the nearest train at a specific metro stop in Washington DC. The project runs on a Raspberry Pi and the display used is the [e-ink bonnet from Adafruit](https://www.adafruit.com/product/4687).

The display shows the following information:
* Destination of the metro - example being "Shady Grove"
* The current time - example being "12:45 PM"
* Which line the train is running on - example being "RD"
* The arrival time of the nearest train - example being "5min"

## Installation
* Create API access token on the [WMATA developer site](https://developer.wmata.com/)
* Clone the repository on your Raspberry Pi with the following `git clone https://github.com/ryanwa18/metropi.git`
* Change into the working directory of the cloned repository `cd metropi`
* Create a virtual environment to work in `python3 -m venv .`
* Activate the virtual environment `source bin/activate`
* Install the required dependencies `pip install -r requirements.txt`
* Create a file named `.env` in your directory with the following content `METRO_API_KEY = 'YOUR_METRO_API_KEY'`
* Run the main program `python3 main.py`

## Configuration
* To change the station being displayed modify `line 22` in `main.py` with the station code you want to use.
* Station codes can be found in [the following JSON](https://developer.wmata.com/docs/services/5476364f031f590f38092507/operations/5476364f031f5909e4fe3311?) from the WMATA API.

![metropi](./images/metropi.png)
