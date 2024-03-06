from Magritte.MAModel_class import MAModel

class SubscriptionPlan(MAModel):

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def __str__(self):
        return f"{self.name} [{self.price==0 and 'Free' or f'${self.price}/month'}]"

SubscriptionPlan.entries = [
    SubscriptionPlan("Community", 0, "Free plan for non-commercial use"),
    SubscriptionPlan("Basic", 10, "Basic plan - good entry point for small teams"),
    SubscriptionPlan("Pro", 25, "Pro plan"),
    SubscriptionPlan("Enterprise", 40, "Enterprise plan for most demanding users"),
]