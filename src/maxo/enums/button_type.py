from enum import StrEnum


class ButtonType(StrEnum):
    CALLBACK = "callback"
    CLIPBOARD = "clipboard"
    LINK = "link"
    MESSAGE = "message"
    OPEN_APP = "open_app"
    REQUEST_CONTACT = "request_contact"
    REQUEST_GEO_LOCATION = "request_geo_location"
