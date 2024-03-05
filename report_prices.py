from room_info import check_room_type, extract_room_size, extract_room_price


def report_prices(soup, report_data, is_our_listing=False):
    price_type = "our_prices" if is_our_listing else "competitors_prices"
    try:
        rooms = soup.find_all('li', class_='db-card__room')
        for room in rooms:
            room_name = room.find('span', class_='room__title-text').string.strip()
            room_size = extract_room_size(room)
            room_type = check_room_type(room_name, room_size)
            room_price = extract_room_price(room)

            if room_type in report_data:
                report_data[room_type][price_type].append(room_price)
            else:
                continue
                # print(f"Room type not found: {room_type}")

    except Exception as e:
        for key in report_data.keys():
            report_data[key][price_type].append("Sold Out")
        # print(f"All rooms sold out or error occurred: {e}")
    return report_data
