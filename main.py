import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from data import competitor_listings, our_listing, rooms

# Set up Selenium with ChromeDriver
options = Options()
options.headless = True  # Run in headless mode

# Set the user agent to an iPhone so that we get the mobile version of the website
user_agent = ("Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
              "CriOS/121.0.0.0 Mobile/15E148 Safari/604.1")
options.add_argument(f'--user-agent={user_agent}')

# Set the window size to 360x640
driver = webdriver.Chrome(options=options)

# Get today's date and tomorrow's date
today = time.strftime("%Y-%m-%d")
tomorrow = time.strftime("%Y-%m-%d", time.gmtime(time.time() + 86400))


def open_url():
    one_bedroom_report_data = {"room_type": "One Bedroom", "competitor_prices": [], "our_prices": []}
    two_bedroom_report_data = {"room_type": "Two Bedroom", "competitor_prices": [], "our_prices": []}
    for listing in competitor_listings:
        url = f'{listing["link"]}?checkin={today}&checkout={tomorrow}'
        driver.get(url)
        # Wait for the page to load (you can adjust the sleep time)
        time.sleep(5)
        # Now the page is loaded, get the page source and use BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        room_names = soup.find_all('span', class_='room__title-text')
        for index, room_name in enumerate(room_names):
            room_name = room_name.text.strip()

            one_room_exists = any(room_name == room["name"] and room["category"] == "one_bedroom" for room in rooms)
            if one_room_exists:
                price = check_price(soup, index)
                one_bedroom_report_data["competitor_prices"].append(price)

            two_room_exists = any(room_name == room["name"] and room["category"] == "two_bedroom" for room in rooms)
            if two_room_exists:
                price = check_price(soup, index)
                two_bedroom_report_data["competitor_prices"].append(price)
    # Now get the prices for our listing
    url = f'{our_listing["link"]}?checkin={today}&checkout={tomorrow}'
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    room_types = soup.find_all('span', class_='room__title-text')
    # open('test.html', 'w').write(str(soup))

    for index, room_type in enumerate(room_types):
        room_name = room_type.text.strip()

        one_room_exists = any(room_name == room["name"] and room["category"] == "one_bedroom" for room in rooms)
        if one_room_exists:
            price = check_price(soup, index)
            one_bedroom_report_data["our_prices"].append(price)

        two_room_exists = any(room_name == room["name"] and room["category"] == "two_bedroom" for room in rooms)
        if two_room_exists:
            price = check_price(soup, index)
            two_bedroom_report_data["our_prices"].append(price)

    report_data = [one_bedroom_report_data, two_bedroom_report_data]
    print(report_data)  # For debugging
    # send_notification(report_data)


def check_price(page_source, index):
    prices = page_source.find_all('div', class_='bui-price-display__value')
    price = prices[index].text
    # Remove the currency symbol and any extra whitespace
    price = price.replace('SAR', '').strip()
    # Remove commas
    price = price.replace(',', '')
    # Convert to integer
    price = int(price)
    return price


def price_is_below_threshold(price):
    # Compare with your threshold
    if price < 2000:
        return True
    else:
        return False


def send_notification(report_data):
    # Send an email or other type of notification

    # Email you're sending the message from
    from_email = "7atem96@gmail.com"
    # Password for your email account
    password = os.environ['EMAIL_PASSWORD']

    # Email you're sending the message to
    # to_email = "hatimalattas@outlook.com"
    receiver_emails = ["hatimalattas@outlook.com",
                       "A1009000@hotmail.com",
                       "walattas2000@gmail.com",
                       "Sooo.djooo.1@gmail.com"]

    # Email subject
    subject = "DAMAC | Booking.com (MOBILE) | Prices Report | " + today

    body = ""

    # Email body
    for room in report_data:
        body += f"Room Type: {room['room_type']}\n"
        body += "Competitor Prices: " + ", ".join(map(str, room['competitor_prices'])) + "\n"
        body += "Our Prices: " + ", ".join(map(str, room['our_prices'])) + "\n"
        body += "-" * 40 + "\n"

    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = from_email
    # msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Server information (e.g., Gmail's SMTP server)
    smtp_server = "smtp.gmail.com"  # This is for Gmail
    smtp_port = 587  # Port for TLS/STARTTLS

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection
    server.login(from_email, password)
    text = msg.as_string()
    for receiver_email in receiver_emails:
        server.sendmail(from_email, receiver_email, text)
    server.quit()


# Schedule this function to run at your desired frequency
open_url()
driver.quit()
