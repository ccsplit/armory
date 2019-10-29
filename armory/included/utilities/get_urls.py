#!/usr/bin/python

from ...database.repositories import PortRepository


def run(db, tool=None, scope_type=None):

    results = []
    Port = PortRepository(db)

    ports = Port.all(service_name="http", tool=tool)
    ports += Port.all(service_name="https", tool=tool)
    ports += Port.all(port_number=80, tool=tool)
    ports += Port.all(port_number=443, tool=tool)

    for p in ports:

        if (
            p.ip_address
            and (scope_type == "active" and p.ip_address.in_scope)  # noqa: W503
            or (scope_type == "passive" and p.ip_address.passive_scope)  # noqa: W503
            or not scope_type  # noqa: W503
        ):
            scheme = "http"
            if p.service_name == "https" or p.port_number == 443:
                scheme = "https"
            results.append(
                "%s://%s:%s" % (scheme, p.ip_address.ip_address, p.port_number)
            )
        domain_list = [d for d in p.ip_address.domains]

        for d in domain_list:
            if (
                (scope_type == "active" and d.in_scope)
                or (scope_type == "passive" and d.passive_scope)
                or not scope_type
            ):
                scheme = "http"
                if p.service_name == "https" or p.port_number == 443:
                    scheme = "https"
                results.append("%s://%s:%s" % (scheme, d.domain, p.port_number))

    return sort_by_url(results)


def sort_by_url(data):
    d_data = {}

    for d in list(set(data)):
        host = d.split("/")[2].split(":")[0]
        scheme = d.split(":")[0]
        port = d.split(":")[2]

        if d_data.get(host, False):
            d_data[host].append([port, scheme])
        else:
            d_data[host] = [[port, scheme]]

    res = []

    for d in sorted(d_data.keys()):
        for s in sorted(d_data[d]):
            res.append("%s://%s:%s" % (s[1], d, s[0]))

    return res
