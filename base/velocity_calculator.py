class VelocityCalculator:
    time = 0

    def get_velocity(unit_of_measurement, how_much):
        return (unit_of_measurement / 1000) * how_much

    def get_measurement(unit_of_measurement, how_much):
        return (unit_of_measurement / 100) * how_much

    def calculate_distance(velocity):
        return velocity * VelocityCalculator.time

