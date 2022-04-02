from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

small_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
)
icon_font = ImageFont.truetype("./meteocons.ttf", 48)

# Map the OpenWeatherMap icon code to the appropriate font character
# See http://www.alessioatzeni.com/meteocons/ for icons
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Metro_Graphics:
    def __init__(self, display):

        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font

        self.display = display

        self._metro_icon = None
        self._destination_name = None
        self._location_name = None
        self._arrival_minutes = None
        self._line = None

    def display_metro(self, metro_status):
        destination_name = metro_status['Trains'][0]['DestinationName']
        self._destination_name = destination_name
        print(destination_name)

        location_name = metro_status['Trains'][0]['LocationName']
        self._location_name = location_name
        print(location_name)

        line = metro_status['Trains'][0]['Line']
        self._line = line
        print(line)

        arrival_minutes = metro_status['Trains'][0]['Min']
        self._arrival_minutes = arrival_minutes
        print(arrival_minutes)

        self.update_time()

    def update_time(self):
        now = datetime.now()
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
        self.update_display()

    def update_display(self):
        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Draw the Icon
        #(font_width, font_height) = icon_font.getsize(self._weather_icon)
        #draw.text(
        #    (
        #        self.display.width // 2 - font_width // 2,
        #        self.display.height // 2 - font_height // 2 - 5,
        #    ),
        #    self._weather_icon,
        #    font=icon_font,
        #    fill=BLACK,
        #)

        # Draw the destination
        draw.text(
            (5, 5), self._destination_name, font=self.medium_font, fill=BLACK,
        )

        # Draw the time
        (font_width, font_height) = medium_font.getsize(self._time_text)
        draw.text(
            (5, font_height * 2 - 5),
            self._time_text,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the line
        (font_width, font_height) = large_font.getsize(self._main_text)
        draw.text(
            (5, self.display.height - font_height * 2),
            self._line,
            font=self.large_font,
            fill=BLACK,
        )

        # Draw the arrival time
        (font_width, font_height) = small_font.getsize(self._description)
        draw.text(
            (5, self.display.height - font_height - 5),
            self._arrival_minutes,
            font=self.small_font,
            fill=BLACK,
        )

        # Draw the location
        (font_width, font_height) = large_font.getsize(self._temperature)
        draw.text(
            (
                self.display.width - font_width - 5,
                self.display.height - font_height * 2,
            ),
            self._location,
            font=self.large_font,
            fill=BLACK,
        )

        self.display.image(image)
        self.display.display()
