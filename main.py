from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from data import competitor_listings, our_listing, one_bedroom_suite_names, two_bedroom_suite_names

# Set up Selenium with ChromeDriver
options = Options()
options.headless = True  # Run in headless mode
driver = webdriver.Chrome(options=options)

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
        room_types = soup.find_all('span', class_='hprt-roomtype-icon-link')
        for index, room_type in enumerate(room_types):
            room_type = room_type.text.strip()
            if room_type in one_bedroom_suite_names:
                price = check_price(soup, index)
                one_bedroom_report_data["competitor_prices"].append(price)
            elif room_type in two_bedroom_suite_names:
                price = check_price(soup, index)
                two_bedroom_report_data["competitor_prices"].append(price)
    # Now get the prices for our listing
    url = f'{our_listing["link"]}?checkin={today}&checkout={tomorrow}'
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    room_types = soup.find_all('span', class_='hprt-roomtype-icon-link')
    # open('test.html', 'w').write(str(soup))

    for index, room_type in enumerate(room_types):
        room_type = room_type.text.strip()
        if room_type in one_bedroom_suite_names:
            price = check_price(soup, index)
            one_bedroom_report_data["our_prices"].append(price)
        elif room_type in two_bedroom_suite_names:
            price = check_price(soup, index)
            two_bedroom_report_data["our_prices"].append(price)
    report_data = [one_bedroom_report_data, two_bedroom_report_data]
    # print(report_data)  # For debugging
    send_notification(report_data)


def check_price(page_source, index):
    prices = page_source.find_all('span', class_='prco-valign-middle-helper')
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
    password = ""

    # Email you're sending the message to
    to_email = "hatimalattas@outlook.com"
    receiver_emails = ["hatimalattas@outlook.com", "A1009000@hotmail.com", "walattas2000@gmail.com", "Sooo.djooo.1@gmail.com"]

    # Email subject
    subject = "DAMAC | Booking.com (WEB) | Prices Report | " + today

    body = ""

    # Email body
    for room in report_data:
        body += f"Room Type: {room['room_type']}\n"
        body += "Competitor Prices: " + ", ".join(map(str, room['competitor_prices'])) + "\n"
        body += "Our Prices: " + ", ".join(map(str, room['our_prices'])) + "\n"
        body += "-" * 40 + "\n"

    print(body)  # For debugging
    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
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
