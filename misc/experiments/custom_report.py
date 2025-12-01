from downward.reports.compare import ComparativeReport

from downward.reports.scatter import ScatterPlotReport

import os

def create_comparative_report(*args):
    exp, config_nicks, revisions, attributes = args[0]
    configs = []
    algorithm_pairs = []
    for config_nick, _ in config_nicks:
        configs.append(config_nick)


    for rev in revisions:
        for i in range(len(configs) // 2):
            algorithm_pairs.append(
                (
                    f"{rev}-{configs[2*i]}",
                    f"{rev}-{configs[2*i + 1]}",
                    f"Diff {rev}_{i}"
                )
            )

    report = ComparativeReport(algorithm_pairs, attributes=attributes)
    outfile = os.path.join(
    exp.eval_dir,
    "%s-comparison.%s" % (
        exp.name, report.output_format))
    report(exp.eval_dir, outfile)


def create_scatter_plot_report(*args):
    exp, config_nicks, revisions, attributes = args[0]

    configs = []
    algorithm_pairs = []
    for config_nick, _ in config_nicks:
        configs.append(config_nick)


    for rev in revisions:
        for i in range(len(configs) // 2):
            algorithm_pairs.append(
                (
                    f"{rev}-{configs[2*i]}",
                    f"{rev}-{configs[2*i + 1]}",
                )
            )

    for attribute in attributes:
        for algorithm_pair in algorithm_pairs:
            report = ScatterPlotReport(attributes=attribute, filter_algorithm=[algorithm_pair[0], algorithm_pair[1]])
            outfile = os.path.join(
            exp.eval_dir,
            "%s-%s-%s-%s.%s" % (
                exp.name, algorithm_pair[0], algorithm_pair[1], attribute, report.output_format))
            report(exp.eval_dir, outfile)

