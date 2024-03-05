from data import rooms


def check_room_type(room_name, room_size):
    if any(room["name"] == room_name and room["category"] == "studio" for room in rooms):
        return "Studio"
    elif any(room["name"] == room_name and room["category"] == "one_bedroom" for room in rooms):
        return "One Bedroom"
    elif any(
            room["name"] == room_name and room["category"] == "two_bedroom_120" and room_size == 120 for room in rooms):
        return "Two Bedroom (120)"
    elif any(
            room["name"] == room_name and room["category"] == "two_bedroom_140" and room_size == 140 for room in rooms):
        return "Two Bedroom (140)"
    else:
        return None


def extract_room_size(soup):
    room_size = soup.find('span', class_='hprt-facilities-facility', attrs={'data-name-en': 'roomSize'})
    room_size = room_size.get_text(strip=True)
    room_size = room_size.replace('m²', '').strip()
    room_size = int(room_size)
    return room_size


def extract_room_price(soup):
    price = soup.find('div', class_='bui-price-display__value')
    price = price.get_text(strip=True)
    # Remove the currency symbol and any extra whitespace
    price = price.replace('SAR', '').strip()
    # Remove commas
    price = price.replace(',', '').strip()
    # Convert to integer
    price = int(price)
    return price
