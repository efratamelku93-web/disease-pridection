from eee import ThermostatAgent


class LoggingThermostat(ThermostatAgent):
    """Also knows the electricity price and trades comfort against cost."""

    def __init__(self, target=22.0, cheap_tolerance=1.0, expensive_tolerance=3.0):
        super().__init__(target, cheap_tolerance)
        self.cheap_tolerance = cheap_tolerance
        self.expensive_tolerance = expensive_tolerance
        self.history = []                      # internal model of the past

    def act(self, temperature, price="cheap"):
        # Wider comfort range when electricity is expensive
        if price == "expensive":
            self.tolerance = self.expensive_tolerance
        else:
            self.tolerance = self.cheap_tolerance

        action = super().act(temperature)      # reuse the reflex rule
        self.history.append((temperature, price, action))
        return action


agent = LoggingThermostat()
percepts = [(15, "cheap"), (21.5, "cheap"), (24.5, "cheap"),
            (24.5, "expensive"), (27, "expensive"), (30, "expensive")]
for t, p in percepts:
    agent.act(t, p)

print("History:", agent.history)
print("COOL actions:", sum(1 for _, _, a in agent.history if a == "COOL"))