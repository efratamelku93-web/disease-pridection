class ThermostatAgent:
    """Knows the temperature AND the electricity price, and trades comfort against cost."""

    def __init__(self, target: float = 20.0,
                 cheap_tolerance: float = 2.0,
                 expensive_tolerance: float = 3.0,
                 alarm_threshold: float = 40.0):
        self.target = target
        self.cheap_tolerance = cheap_tolerance
        self.expensive_tolerance = expensive_tolerance
        self.alarm_threshold = alarm_threshold
        self.history: list[tuple[float, str]] = []

    def act(self, temperature: float, price: str = "cheap") -> str:
        self.history.append((temperature, price))

        if temperature > self.alarm_threshold:      # safety check always comes first
            return "ALARM"

        tolerance = self.expensive_tolerance if price == "expensive" else self.cheap_tolerance

        if temperature > self.target + tolerance:
            return "COOL"
        if temperature < self.target - tolerance:
            return "HEAT"
        return "IDLE"


if __name__ == "__main__":
    agent = ThermostatAgent()
    percepts = [(15, "cheap"), (21.5, "cheap"), (21.5, "expensive"),
                (18, "cheap"), (18, "expensive"), (27, "expensive"), (45, "expensive")]
    for temp, price in percepts:
        print(f"Temperature {temp:>5} C, price {price:>9} -> action: {agent.act(temp, price)}")
    print("History:", agent.history)