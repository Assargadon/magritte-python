from Magritte.MAModel_class import MAModel

class SubscriptionPlan(MAModel):

    @classmethod
    def subscriptionPlan(cls, name, price, description):
        p = cls()
        p.name = name
        p.price = price
        p.description = description
        return p

    def __init__(self):
        self.name = None
        self.price = None
        self.description = None

    def __str__(self):
        return f"{self.name} [{self.price==0 and 'Free' or f'${self.price}/month'}]"


    @classmethod
    def entries(cls):
        #lasy initialization
        if not hasattr(cls, "_entries"):
            cls._entries = [
                SubscriptionPlan.subscriptionPlan("Community", 0, "Free plan for non-commercial use"),
                SubscriptionPlan.subscriptionPlan("Basic", 10, "Basic plan - good entry point for small teams"),
                SubscriptionPlan.subscriptionPlan("Pro", 25, "Pro plan"),
                SubscriptionPlan.subscriptionPlan("Enterprise", 40, "Enterprise plan for most demanding users"),
            ]
        return cls._entries