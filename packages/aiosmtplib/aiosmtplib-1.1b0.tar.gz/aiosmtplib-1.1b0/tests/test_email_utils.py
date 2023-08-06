"""
Test message and address parsing/formatting functions.
"""
from email.headerregistry import Address
from email.message import EmailMessage

import pytest

from aiosmtplib.email import (
    extract_recipients,
    extract_sender,
    flatten_message,
    parse_address,
    quote_address,
)


@pytest.mark.parametrize(
    "address, expected_address",
    (
        ('"A.Smith" <asmith+foo@example.com>', "asmith+foo@example.com"),
        ("Pepé Le Pew <pépe@example.com>", "pépe@example.com"),
        ("<a@new.topleveldomain>", "a@new.topleveldomain"),
        ("email@[123.123.123.123]", "email@[123.123.123.123]"),
        ("_______@example.com", "_______@example.com"),
        ("B. Smith <b@example.com", "b@example.com"),
    ),
    ids=("quotes", "nonascii", "newtld", "ipaddr", "underscores", "missing_end_<"),
)
def test_parse_address(address, expected_address):
    parsed_address = parse_address(address)
    assert parsed_address == expected_address


@pytest.mark.parametrize(
    "address, expected_address",
    (
        ('"A.Smith" <asmith+foo@example.com>', "<asmith+foo@example.com>"),
        ("Pepé Le Pew <pépe@example.com>", "<pépe@example.com>"),
        ("<a@new.topleveldomain>", "<a@new.topleveldomain>"),
        ("email@[123.123.123.123]", "<email@[123.123.123.123]>"),
        ("_______@example.com", "<_______@example.com>"),
        ("B. Smith <b@example.com", "<b@example.com>"),
    ),
    ids=("quotes", "nonascii", "newtld", "ipaddr", "underscores", "missing_end_quote"),
)
def test_quote_address(address, expected_address):
    quoted_address = quote_address(address)
    assert quoted_address == expected_address


def test_flatten_message():
    message = EmailMessage()
    message["To"] = Address(username="bob", domain="example.com")
    message["Subject"] = "Hello, World."
    message["From"] = Address(username="alice", domain="example.com")
    message.set_content("This is a test")

    flat_message = flatten_message(message)

    expected_message = b"""To: bob@example.com\r
Subject: Hello, World.\r
From: alice@example.com\r
Content-Type: text/plain; charset="utf-8"\r
Content-Transfer-Encoding: 7bit\r
MIME-Version: 1.0\r
\r
This is a test\r
"""
    assert flat_message == expected_message


@pytest.mark.parametrize(
    "utf8, cte_type, expected_chunk",
    (
        (False, "7bit", b"=?utf-8?q?=C3=A5lice?="),
        (True, "7bit", b"From: \xc3\xa5lice@example.com"),
        (False, "8bit", b"=?utf-8?q?=C3=A5lice?="),
        (True, "8bit", b"\xc3\xa5lice@example.com"),
    ),
    ids=("ascii-7bit", "utf8-7bit", "ascii-8bit", "utf8-8bit"),
)
def test_flatten_message_utf8_options(utf8, cte_type, expected_chunk):
    message = EmailMessage()
    message["From"] = Address(username="ålice", domain="example.com")

    flat_message = flatten_message(message, utf8=utf8, cte_type=cte_type)

    assert expected_chunk in flat_message


def test_flatten_message_removes_bcc_from_message_text():
    message = EmailMessage()
    message["Bcc"] = Address(username="alice", domain="example.com")

    flat_message = flatten_message(message)

    assert flat_message == b"\r\n"  # empty message


def test_flatten_resent_message():
    message = EmailMessage()
    message["To"] = Address(username="bob", domain="example.com")
    message["Cc"] = Address(username="claire", domain="example.com")
    message["Bcc"] = Address(username="dustin", domain="example.com")

    message["Subject"] = "Hello, World."
    message["From"] = Address(username="alice", domain="example.com")
    message.set_content("This is a test")

    message["Resent-Date"] = "Mon, 20 Nov 2017 21:04:27 -0000"
    message["Resent-To"] = Address(username="eliza", domain="example.com")
    message["Resent-Cc"] = Address(username="fred", domain="example.com")
    message["Resent-Bcc"] = Address(username="gina", domain="example.com")
    message["Resent-Subject"] = "Fwd: Hello, World."
    message["Resent-From"] = Address(username="hubert", domain="example.com")

    flat_message = flatten_message(message)

    expected_message = b"""To: bob@example.com\r
Cc: claire@example.com\r
Subject: Hello, World.\r
From: alice@example.com\r
Content-Type: text/plain; charset="utf-8"\r
Content-Transfer-Encoding: 7bit\r
MIME-Version: 1.0\r
Resent-Date: Mon, 20 Nov 2017 21:04:27 -0000\r
Resent-To: eliza@example.com\r
Resent-Cc: fred@example.com\r
Resent-Subject: Fwd: Hello, World.\r
Resent-From: hubert@example.com\r
\r
This is a test\r
"""
    assert flat_message == expected_message


def test_extract_recipients():
    message = EmailMessage()
    message["To"] = Address(username="bob", domain="example.com")
    message["Cc"] = Address(username="alice", domain="example.com")

    recipients = extract_recipients(message)

    assert recipients == [message["To"], message["Cc"]]


def test_extract_recipients_includes_bcc():
    message = EmailMessage()
    message["Bcc"] = Address(username="alice", domain="example.com")

    recipients = extract_recipients(message)

    assert recipients == [message["Bcc"]]


def test_extract_recipients_resent_message():
    message = EmailMessage()
    message["To"] = Address(username="bob", domain="example.com")
    message["Cc"] = Address(username="claire", domain="example.com")
    message["Bcc"] = Address(username="dustin", domain="example.com")

    message["Resent-Date"] = "Mon, 20 Nov 2017 21:04:27 -0000"
    message["Resent-To"] = Address(username="eliza", domain="example.com")
    message["Resent-Cc"] = Address(username="fred", domain="example.com")
    message["Resent-Bcc"] = Address(username="gina", domain="example.com")

    recipients = extract_recipients(message)

    assert message["Resent-To"] in recipients
    assert message["Resent-Cc"] in recipients
    assert message["Resent-Bcc"] in recipients
    assert message["To"] not in recipients
    assert message["Cc"] not in recipients
    assert message["Bcc"] not in recipients


def test_extract_recipients_valueerror_on_multiple_resent_message():
    message = EmailMessage()
    message["Resent-Date"] = "Mon, 20 Nov 2016 21:04:27 -0000"
    message["Resent-Date"] = "Mon, 20 Nov 2017 21:04:27 -0000"

    with pytest.raises(ValueError):
        extract_recipients(message)


def test_extract_sender():
    message = EmailMessage()
    message["From"] = Address(username="alice", domain="example.com")

    sender = extract_sender(message)

    assert sender == message["From"]


def test_extract_sender_prefers_sender_header():
    message = EmailMessage()
    message["From"] = Address(username="bob", domain="example.com")
    message["Sender"] = Address(username="alice", domain="example.com")

    sender = extract_sender(message)

    assert sender != message["From"]
    assert sender == message["Sender"]


def test_extract_sender_resent_message():
    message = EmailMessage()
    message["From"] = Address(username="alice", domain="example.com")

    message["Resent-Date"] = "Mon, 20 Nov 2017 21:04:27 -0000"
    message["Resent-From"] = Address(username="hubert", domain="example.com")

    sender = extract_sender(message)

    assert sender == message["Resent-From"]
    assert sender != message["From"]


def test_extract_sender_valueerror_on_multiple_resent_message():
    message = EmailMessage()
    message["Resent-Date"] = "Mon, 20 Nov 2016 21:04:27 -0000"
    message["Resent-Date"] = "Mon, 20 Nov 2017 21:04:27 -0000"

    with pytest.raises(ValueError):
        extract_sender(message)
