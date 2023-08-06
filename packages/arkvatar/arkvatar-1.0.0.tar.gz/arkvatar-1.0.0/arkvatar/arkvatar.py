from arkvatar.client import Client


client = Client()


async def verify(identifier: str):
    """Verify the given identifier to get his type. If multiple types, a list
    will be returned

    Parameters:
        identifier (str): The identifier to verify

    Returns:
        dict: JSON response containing the matching type, or a list of possible
        types in the case of multiple cryptocurrencies detected
    """
    r = await client.post('https://arkvatar.com/api/verify', {
        "identifier": identifier}, {'content-type': 'application/json'})

    return r


async def show(identifier: str):
    r = await client.get(f"https://arkvatar.com/api/{identifier}", {'content-type': 'application/json'})

    return r


async def store(arkvatar_type: str, identifier: str, qr_code: bool = False,
                vertical_gradient: bool = False, no_background: bool = False):
    """Create a new arkvatar

    Parameters:
        arkvatar_type (str): The Type (Email or Crypto) of the Arkvatar to be created
        identifier (str): The identifier of the Arkvatar to be created
        qr_code (bool): Include a QR code in the generation
        vertical_gradient (bool): Generate the gradient vertically
        no_background (bool): Generate the Arkvatar without a background

    Returns:
        dict: JSON response containing the url of the generated Arkvatar
    """

    r = await client.post('https://arkvatar.com/api/store', {
        "type": arkvatar_type, "identifier": identifier, "qr_code": qr_code,
        "vertical_gradient": vertical_gradient, "no_background": no_background
        }, {'content-type': 'application/json'})

    return r
