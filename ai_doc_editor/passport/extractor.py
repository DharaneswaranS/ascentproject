from passporteye import read_mrz

def extract_passport_data(image_path):
    mrz = read_mrz(image_path)

    if not mrz:
        return None

    data = mrz.to_dict()
    return {
        "passport_number": data.get("number"),
        "surname": data.get("surname"),
        "given_names": data.get("names"),
        "nationality": data.get("nationality"),
        "date_of_birth": data.get("date_of_birth"),
        "sex": data.get("sex"),
        "expiry_date": data.get("expiration_date"),
        "issuing_country": data.get("country")
    }
