from downward.reports.compare import ComparativeReport

from downward.reports.scatter import ScatterPlotReport

import os

import itertools

def create_comparative_report(*args):
    exp, config_nicks, revisions, attributes, pair_size = args[0]
    configs = []
    algorithm_pairs = []
    n = int(pair_size)
    for config_nick, _ in config_nicks:
        configs.append(config_nick)

    for i in range(len(configs) // n):
        algorithms = []
        for rev in revisions:
            for j in range(n):
                algorithms.append(f"{rev}-{configs[i * n + j]}")

        revision_pairs = [(rev1, rev2) for rev1, rev2 in itertools.combinations(algorithms, 2)]

        for j, (rev1, rev2) in enumerate(revision_pairs):
                algorithm_pairs.append(
                    (
                        rev1,
                        rev2,
                        f"Diff {i * n + j}"
                    )
                )
    report = ComparativeReport(algorithm_pairs, attributes=attributes)
    outfile = os.path.join(
    exp.eval_dir,
    "%s-comparison.%s" % (
        exp.name, report.output_format))
    report(exp.eval_dir, outfile)

def domain_as_category(run1, run2):
    # run2['domain'] has the same value, because we always
    # compare two runs of the same problem.
    return run1["domain"]

def create_scatter_plot_report(*args):
    exp, config_nicks, revisions, attributes, pair_size = args[0] # labels only accepts 2 values, for comparisons of 3 algorithms create separate reports
    configs = []
    algorithm_pairs = []
    n = int(pair_size)
    for config_nick, _ in config_nicks:
        configs.append(config_nick)

    for i in range(len(configs) // n):
        algorithms = []
        for rev in revisions:
            for j in range(n):
                algorithms.append(f"{rev}-{configs[i * n + j]}")

        revision_pairs = [(rev1, rev2) for rev1, rev2 in itertools.combinations(algorithms, 2)]

        for j, (rev1, rev2) in enumerate(revision_pairs):
                if "unrolling" in rev1:
                    xlabel = "Unrolling"
                elif "approximate-cycle" in rev1:
                    xlabel = "Approximate Negative Cycles"
                elif "approximate" in rev1:
                    xlabel = "Approximate Negative"

                if "unrolling" in rev2:
                    ylabel = "Unrolling"
                elif "approximate-cycle" in rev2:
                    ylabel = "Approximate Negative Cycles"
                elif "approximate" in rev2:
                    ylabel = "Approximate Negative"
                if not "Unrolling" in [xlabel, ylabel]:
                    continue
                
                if "-add-" in rev1:
                    algo = "Add"
                elif "-ff-" in rev1:
                    algo = "FF"
                elif "-lm-" in rev1:
                    algo = "LM"
                    
                algorithm_pairs.append(
                    (
                        rev1,
                        rev2,
                        f"Diff {i * n + j}"
                    )
                )
    for attribute in attributes:
        for algorithm_pair in algorithm_pairs:
            report = ScatterPlotReport(attributes=attribute, 
                                       filter_algorithm=[algorithm_pair[0], algorithm_pair[1]], 
                                       xlabel=xlabel, 
                                       ylabel=ylabel, 
                                       get_category=domain_as_category)
            outfile = os.path.join(
            exp.eval_dir,
            "%s-%s-%s-%s.%s" % (
                xlabel, ylabel, algo, attribute, report.output_format))
            report(exp.eval_dir, outfile)

