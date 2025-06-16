from argparse import ArgumentParser
from pandas import read_csv, DataFrame
import matplotlib.pyplot as plt


def getData(file_path):
    """
    reads data from csv
    """
    with open(file_path, "r") as file:
        data = read_csv(file, sep=",")
    assert data.shape[0] > 0, "Empty file?"
    assert data.shape[1] == 2, "Expected two columns in the CSV file"
    return data


def evaluate(e: list, p: list, mil: list, step: int):
    """
    evaluates coefficient of determination
    and plots the regression line
    e: estimated values
    p: actual values
    plot to graph
    """
    ss_res = sum((p[i] - e[i]) ** 2 for i in range(len(e)))
    ss_tot = sum((p[i] - sum(p) / len(p)) ** 2 for i in range(len(p)))
    r2 = 1 - (ss_res / ss_tot)
    print(f"Coefficient of determination (R^2): {r2}")
    plt.scatter(mil, p, color="blue", label="Actual Data")
    plt.plot(mil, e, color="red", label="Regression Line")
    plt.xlabel("Mileage (km)")
    plt.ylabel("Price")
    plt.title(f"Epoch {step + 1}")
    plt.legend()
    plt.savefig(f"step_{step + 1}")
    plt.close()
    return r2


def train(data: DataFrame, lr: float, epochs: int):
    """
    Training function
    _theta0: lr*1/m*summation(i=0 to m-1)(estimated(mil[i]) - price[i])
    _theta1: lr*1/m*summation(i=0 to m-1)(estimated(mil[i] - price[i])*mil[i]
    theta0: theta0 + _theta0
    theta1: theta1 + _theta1
    m: dataset size
    """
    m = data.shape[0]
    t0 = 0
    t1 = 0
    mil = list(data["km"].values)
    p = list(data["price"].values)
    milmax = max(mil)
    milmin = min(mil)
    mil = [(x - milmin) / (milmax - milmin) for x in mil]
    for step in range(epochs):
        est = [mil[i] * t1 + t0 for i in range(m)]
        delta = [est[i] - p[i] for i in range(m)]
        t0 -= lr / m * sum(delta)
        t1 -= lr / m * sum(delta[i] * mil[i] for i in range(m))
        if (step + 1) % 100 == 0:
            evaluate(est, p, mil, step)
    scaled_t1 = t1 / (milmax - milmin)
    scaled_t0 = t0 - milmin * scaled_t1
    scaled_est = [scaled_t0 + scaled_t1 * x for x in list(data["km"].values)]
    evaluate(scaled_est, p, list(data["km"].values), -1)
    print(f"Final coefficients: t0 = {scaled_t0}, t1 = {scaled_t1}")
    with open("thetas.txt", "w") as f:
        f.write(f"{scaled_t0}\n{scaled_t1}\n")


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Path to the file to process",
    )
    parser.add_argument(
        "-lr",
        type=int,
        default=0.05,
        help="Learning rate for the training",
    )
    parser.add_argument(
        "-e",
        type=int,
        default=10000,
        help="Number of epochs for training",
    )
    args = parser.parse_args()
    try:
        train_data = getData(args.file)
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    print(train_data)
    print(train_data.shape)
    train(train_data, args.lr, args.e)


if __name__ == "__main__":
    main()
