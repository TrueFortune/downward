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

    count = 0
    for i in range(len(configs) // n):
        algorithms = []
        for rev in revisions:
            for j in range(n):
                algorithms.append(f"{rev}-{configs[i * n + j]}")

        revision_pairs = [(rev1, rev2) for rev1, rev2 in itertools.combinations(algorithms, 2)]

        for rev1, rev2 in revision_pairs:
            if not ("unrolling" in rev1 or "unrolling" in rev2):
                continue
            if (not ("-add-" in rev1 and "-add-" in rev2)) and (not ("-ff-" in rev1 and "-ff-" in rev2)) and (not ("-lm-" in rev1 and "-lm-" in rev2)):
                continue
            # Ensure unrolling is always on the right side
            if "unrolling" in rev1: 
                rev1_temp = rev2
                rev2 = rev1
                rev1 = rev1_temp

            algorithm_pairs.append(
                (
                    rev1,
                    rev2,
                    f"Diff {count}"
                )
            )
            count += 1
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
                print(f"xlabel: {xlabel}, ylabel: {ylabel}")
                if not "Unrolling" in [xlabel, ylabel]:
                    continue
                
                if "-add-" in rev1 and "-add-" in rev2:
                    algo = "Add"
                elif "-ff-" in rev1 and "-ff-" in rev2:
                    algo = "FF"
                elif "-lm-" in rev1 and "-lm-" in rev2:
                    algo = "LM"
                else:
                    continue
                
                # Ensure unrolling is always on the y-axis
                if xlabel == "Unrolling": 
                    xlabel_temp = ylabel
                    ylabel = xlabel
                    xlabel = xlabel_temp
                    rev1_temp = rev2
                    rev2 = rev1
                    rev1 = rev1_temp

                algorithm_pairs.append(
                    (
                        rev1,
                        rev2,
                        xlabel,
                        ylabel,
                        algo
                    )
                )
    for attribute in attributes:
        for algorithm_pair in algorithm_pairs:
            report = ScatterPlotReport(attributes=attribute, 
                                       filter_algorithm=[algorithm_pair[0], algorithm_pair[1]], 
                                       xlabel=algorithm_pair[2], 
                                       ylabel=algorithm_pair[3], 
                                       get_category=domain_as_category)
            outfile = os.path.join(
            exp.eval_dir,
            "%s-%s-%s-%s.%s" % (
                algorithm_pair[2], algorithm_pair[3], algorithm_pair[4], attribute, report.output_format))
            report(exp.eval_dir, outfile)

