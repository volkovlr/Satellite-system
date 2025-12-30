GROUP_PARAM_KEYS = [
    "height",  # The height of each orbit above the Earth
    "orb_inclin",  # Orbit inclination
    "longitude_asc",  # The longitude of the ascending node
    "count_orbits",  #  Count of orbits in a group
    "count_satellites",  # Count of satellites in a group
    "phase_shift",  # Phase shift between neighboring orbits
    "ph_first_sat",  # The phase of the first satellite in the first orbit
    "t0",  # Time when the grouping was created
    "view_angle"  # Half of the viewing angle of each satellite
]

CALCULATOR_PARAM_KEYS = [
    "group_number",  # The number of counting group
    "resolution",  # Hexes/area
    "target_time"  # Coverage is calculated for this time
]