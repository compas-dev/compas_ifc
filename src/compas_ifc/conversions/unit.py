def IfcCompoundPlaneAngleMeasure_to_degrees(angle_components):
    if len(angle_components) != 4:
        raise ValueError("Input must be a list or tuple of four elements: [degrees, minutes, seconds, millionths_of_second]")

    degrees, minutes, seconds, millionths = angle_components

    # Determine the sign based on the degrees component
    sign = -1 if degrees < 0 else 1

    # Use absolute values to avoid negative components in calculation
    degrees = abs(degrees)
    minutes = abs(minutes)
    seconds = abs(seconds)
    millionths = abs(millionths)

    # Convert millionths of a second to fractional seconds
    fractional_seconds = millionths / 1_000_000

    # Total seconds including the fractional part
    total_seconds = seconds + fractional_seconds

    # Convert everything to decimal degrees
    decimal_degrees = sign * (degrees + (minutes / 60) + (total_seconds / 3600))

    return decimal_degrees
