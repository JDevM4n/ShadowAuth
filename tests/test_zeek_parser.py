import pytest

from shadowauth.parsers.zeek_parser import (
    ZeekParser,
)


def test_parse_zeek_conn_event():

    parser = ZeekParser()

    event = {
        "ts": 1788811200.5,
        "uid": "CZeekConn001",
        "id.orig_h": "192.168.2.50",
        "id.orig_p": 54321,
        "id.resp_h": "192.168.2.27",
        "id.resp_p": 2222,
        "proto": "tcp",
        "service": "ssh",
        "duration": 1.25,
        "orig_bytes": 350,
        "resp_bytes": 900,
        "conn_state": "SF",
        "orig_pkts": 5,
        "resp_pkts": 7,
    }

    normalized = parser.parse(
        event
    )

    assert normalized.source == "zeek"

    assert (
        normalized.event_type
        == "zeek.conn"
    )

    assert (
        normalized.native_uid
        == "CZeekConn001"
    )

    assert normalized.session_id is None

    assert (
        normalized.network.source_ip
        == "192.168.2.50"
    )

    assert (
        normalized.network.source_port
        == 54321
    )

    assert (
        normalized.network.destination_ip
        == "192.168.2.27"
    )

    assert (
        normalized.network.destination_port
        == 2222
    )

    assert (
        normalized.network.protocol
        == "tcp"
    )

    assert (
        normalized.network.conn_state
        == "SF"
    )

    assert (
        normalized.network.duration_ms
        == pytest.approx(1250.0)
    )

    assert (
        normalized.network.bytes_sent
        == 350
    )

    assert (
        normalized.network.bytes_received
        == 900
    )

    assert (
        normalized.network.packets_sent
        == 5
    )

    assert (
        normalized.network.packets_received
        == 7
    )


def test_parse_zeek_dns_event():

    parser = ZeekParser()

    event = {
        "ts": 1788811205.0,
        "uid": "CZeekDNS001",
        "id.orig_h": "192.168.2.50",
        "id.orig_p": 53000,
        "id.resp_h": "8.8.8.8",
        "id.resp_p": 53,
        "proto": "udp",
        "query": "example.com",
        "qtype_name": "A",
        "rcode_name": "NOERROR",
        "answers": [
            "93.184.216.34"
        ],
    }

    normalized = parser.parse(
        event
    )

    assert normalized.source == "zeek"

    assert (
        normalized.event_type
        == "zeek.dns"
    )

    assert (
        normalized.native_uid
        == "CZeekDNS001"
    )

    assert (
        normalized.network.source_ip
        == "192.168.2.50"
    )

    assert (
        normalized.network.destination_port
        == 53
    )

    assert (
        normalized.network.protocol
        == "udp"
    )

    assert (
        normalized.data["query"]
        == "example.com"
    )


def test_zeek_event_id_is_deterministic():

    parser = ZeekParser()

    event = {
        "ts": 1788811210.0,
        "uid": "CZeekStable001",
        "id.orig_h": "10.0.0.10",
        "id.orig_p": 40000,
        "id.resp_h": "10.0.0.20",
        "id.resp_p": 443,
        "proto": "tcp",
        "conn_state": "SF",
    }

    first = parser.parse(
        event
    )

    second = parser.parse(
        event
    )

    assert (
        first.event_id
        == second.event_id
    )


def test_zeek_parser_rejects_missing_timestamp():

    parser = ZeekParser()

    event = {
        "uid": "CNoTimestamp",
        "id.orig_h": "10.0.0.1",
        "id.resp_h": "10.0.0.2",
        "conn_state": "S0",
    }

    with pytest.raises(
        ValueError,
        match="does not contain 'ts'",
    ):
        parser.parse(
            event
        )
