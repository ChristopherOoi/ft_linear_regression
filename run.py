def getThetas():
    """
    Reads the theta values from a file named 'thetas.txt'.
    """
    try:
        with open("thetas.txt", "r") as file:
            lines = file.readlines()
            theta0 = float(lines[0].strip())
            theta1 = float(lines[1].strip())
        return theta0, theta1
    except Exception as e:
        print(f"Error reading thetas: {e}")
        return None, None


def estimatePrice(mileage):
    """
    Estimates the price of a car based on its mileage.
    """
    theta0, theta1 = getThetas()
    if not any([theta0, theta1]):
        raise ValueError("Thetas not found or invalid.")
    return theta0 + theta1 * mileage


def main():
    try:
        while True:
            inp = input("""Enter mileage or 'exit' to quit: """).strip()
            if inp.lower() == "exit":
                print("Exiting the program.")
                break
            mileage = float(inp)
            if mileage < 0:
                raise ValueError("Mileage cannot be negative.")
            price = estimatePrice(mileage)
            print(f"The estimated price of the car is: ${price:.2f}")
    except ValueError as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()
