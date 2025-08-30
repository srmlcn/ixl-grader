import argparse


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="IXL Grader: A tool to grade IXL assignments."
    )

    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input file containing IXL assignments.",
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Path to the output file where grades will be saved.",
    )
    parser.add_argument(
        "-s",
        "--smart-score",
        type=int,
        choices=range(0, 101),
        required=True,
        help="SmartScore threshold for grading (0-100).",
    )

    return parser.parse_args()
