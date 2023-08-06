def decode_html(string):
    """decode common html/xml entities"""
    new_string = string
    decoded = ['>', '<', '"', '&', '\'']
    encoded = ['&gt;', '&lt;', '&quot;', '&amp;', '&#039;']
    for e, d in zip(encoded, decoded):
        new_string = new_string.replace(e, d)
    for e, d in zip(encoded[::-1], decoded[::-1]):
        new_string = new_string.replace(e, d)
    return new_string
