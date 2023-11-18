import string
import secrets
from enum import Enum


class Strongness(Enum):
    """
    Enum that represents the strongness of a password.
    Contains string representation and min length of the type.
    """

    STRONG = ("Strong", 14)
    MODERATE = ("Moderate", 10)
    WEAK = ("Weak", 0)


def generate_password(**kwargs) -> (str, str):
    """
    Generates a password, based on the provided config.
    lowercase, upercase, digis, special chars can be used to generate the pass

    Returns:
        password: the password
        strongness: password's strongness
    """

    string_set = {
        "lowercase":  string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "digits": string.digits,
        "special_char": string.punctuation
    }

    alphabet = "".join([string_set[k]
                       for k, v in kwargs.items() if v and k != "length"])

    while True:
        password = ''.join(secrets.choice(alphabet)
                           for i in range(kwargs['length']))

        is_pass_valid = (
            (not kwargs['lowercase'] or any(c.islower() for c in password)),
            (not kwargs['uppercase'] or any(c.isupper() for c in password)),
            (not kwargs['digits'] or any(c.isdigit() for c in password)),
            (not kwargs['special_char'] or any(
                c in string.punctuation for c in password))
        )

        if all(is_pass_valid):
            break

    return (password, password_strongness(password))


def password_strongness(password: str) -> str:
    """
    Calculates password strongness.
    A password is considered to be:

    strong if it has a lowercase, uppercase, digit and special char and the length is bigger than 14
    moderate if it has  an uppercase, digit or special char and the length is bigger than 10
    weak otherwise

    Args:
        password str: the password

    Returns:
        strongness: str: password's strongness
    """

    pass_length = len(password)
    hasLower = False
    hasUpper = False
    hasDigit = False
    specialChar = False

    for i in range(pass_length):
        if password[i].islower():
            hasLower = True
        if password[i].isupper():
            hasUpper = True
        if password[i].isdigit():
            hasDigit = True
        if password[i] in string.punctuation:
            specialChar = True

    if (hasLower and hasUpper and
            hasDigit and specialChar and pass_length >= Strongness.STRONG.value[1]):
        return Strongness.STRONG.value[0]

    elif (((hasUpper and hasDigit) or specialChar)
          and pass_length >= Strongness.MODERATE.value[1]):
        return Strongness.MODERATE.value[0]

    return Strongness.WEAK.value[0]
