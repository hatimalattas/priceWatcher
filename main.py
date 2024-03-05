from open_url import open_url
from config import configure_driver, today, tomorrow
from data import our_listing, competitor_listings, initialize_report_data
from report_prices import report_prices
from send_notifications import send_email

driver = configure_driver()

today = today()
tomorrow = tomorrow()


def main():
    """ Main entry point of the app """
    report_data = initialize_report_data()
    soup = open_url(our_listing["link"], today, tomorrow)
    report_data = report_prices(soup, report_data, is_our_listing=True)

    for competitor in competitor_listings:
        soup = open_url(competitor["link"], today, tomorrow)
        report_data = report_prices(soup, report_data, is_our_listing=False)

    send_email(report_data)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    driver.quit()
