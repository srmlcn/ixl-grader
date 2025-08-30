from ixl_grader.argument_parser import get_args
from ixl_grader.report import Report


def main():
    args = get_args()

    report = Report()
    report.import_report(csv_path=args.input_file)
    report.grade(smart_score_threshold=args.smart_score)
    report.export_report(output_path=args.output_file)


if __name__ == "__main__":
    main()
