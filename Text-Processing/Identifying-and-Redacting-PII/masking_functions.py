"""
Masks the matching criteria
"""
# masking_functions.py

def mask_email(match):
    """
    Masks an email address by replacing the local part (excluding the first character)
    with asterisks, preserving the domain.
    """
    return match.group(1) + "****" + match.group(3)

def mask_phone(match):
    """
    Masks a phone number by replacing the first six digits with asterisks and
    preserving the last four digits.
    """
    return "***-***-" + match.group(4)

def mask_ssn(match):
    """
    Masks a Social Security Number (SSN) by replacing the first five digits with asterisks,
    preserving only the last four digits.
    """
    return "***-**-" + match.group(3)

def mask_credit_card(match):
    """
    Masks a credit card number by replacing the first 12 digits with asterisks,
    preserving only the last four digits.
    """
    return "****-****-****-" + match.group(4)

def mask_date_of_birth(match):
    """
    Masks a date of birth by replacing the day and month with asterisks,
    preserving only the year.
    """
    return "****/**/" + match.group(3)

def mask_passport(match):
    """
    Masks a passport number by replacing the first six digits with asterisks,
    preserving only the last three digits.
    """
    return "***-***-" + match.group(3)

def mask_driver_license(match):
    """
    Masks a driver's license number by replacing the middle section with asterisks,
    preserving the initial part and format.
    """
    return match.group(1) + "-***-***"

def mask_bank_account(match):
    """
    Masks a bank account number by replacing all but the last four digits with asterisks.
    """
    return "****" + match.group(0)[-4:]

def mask_ip_address(match):
    """
    Masks an IP address by replacing the first three octets with asterisks,
    preserving only the last octet.
    """
    return "***.***.***." + match.group(4)

def mask_mac_address(match):
    """
    Masks a MAC address by replacing the first five groups with asterisks,
    preserving only the last group.
    """
    return "**:**:**:**:**:" + match.group(2)

def mask_physical_address(match):
    """
    Masks a physical address by replacing the street number with asterisks,
    preserving the rest of the address.
    """
    return "*** " + match.group(2)

# Dictionary mapping function names to actual functions
mask_function_mapping = {
    'mask_email': mask_email,
    'mask_phone': mask_phone,
    'mask_ssn': mask_ssn,
    'mask_credit_card': mask_credit_card,
    'mask_date_of_birth': mask_date_of_birth,
    'mask_passport': mask_passport,
    'mask_driver_license': mask_driver_license,
    'mask_bank_account': mask_bank_account,
    'mask_ip_address': mask_ip_address,
    'mask_mac_address': mask_mac_address,
    'mask_physical_address': mask_physical_address,
}
