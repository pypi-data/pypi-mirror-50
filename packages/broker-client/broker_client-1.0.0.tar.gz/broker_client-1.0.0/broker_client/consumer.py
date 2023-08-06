
class Consumer():
    def __init__(self, client, query): # FIXME: add location and max services
        self.state = "initialized"
        self.client = client
        self.query = {
            "@type": self.get_param(query, "@type", "swarm:Resource"),
            "operations": self.get_param(query, "operations", ["read"]),
            "duration": self.get_param(query, "duration", 60),
            "hops": 3,
            "timeout": 1000,
            "consumer": self.client.sd,
        }
        print(self.query)
        self.contract = None
        self.contract_location = None

    def get_param(self, query, key, default):
        print(query)
        return query[key] if key in query.keys() else default

    def contract_providers(self):
        if self.search_and_contract() and self.accept_negotiation():
            print("Contract worked")
            return self.contract
        else:
            print("Contract failed at state %s" % self.state)
            return None

    def search_and_contract(self):
        negotiation = self.client.contract({"query": self.query})
        if not negotiation:
            self.state = "search_and_contract_failed"
            return None
        else:
            self.state = "waiting_accept_negotiation"
            self.contract, self.contract_location = negotiation
            return self.contract

    def accept_negotiation(self):
        contract = self.client.sign_and_send_tx(self.contract, self.contract_location)
        if not contract:
            self.state = "accept_negotiation_failed"
            return None
        else:
            self.state = "sla_established"
            self.contract = contract
            return contract

    def smart_use(self, *args, **kwargs):
        if self.state == "sla_established":
            return self.client.smart_use(self.contract, *args, **kwargs)
        else:
            print("Use service: invalid state '%s'" % self.state)

    def get_num_services(self):
        if self.contract:
            return len(self.contract['tx']['content']['output']) - 1
        else:
            print("get_num_services: contract is None")

    def contract_summary(self):
        if self.contract:
            summary = {
                "consumer_balance": self.contract["tx"]["content"]["output"][0]["value"],
                "providers": [{"provider": o["provider_id"], "price": o["value"]} for o in self.contract["tx"]["content"]["output"][1:]]
            }
            if "sig" in self.contract["tx"]["content"]["input"][0].keys():
                summary["signature"] = self.contract["tx"]["content"]["input"][0]["sig"]

            return summary
