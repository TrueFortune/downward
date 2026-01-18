#! /usr/bin/env python3

import os

from lab.environments import LocalEnvironment, BaselSlurmEnvironment

from lab.reports import Attribute

import common_setup
from common_setup import IssueConfig, IssueExperiment

from custom_parser import unrolling_parser

from custom_report import create_comparative_report, create_scatter_plot_report


ARCHIVE_PATH = "ai/downward/unrolling"
REPO_DIR = os.environ["DOWNWARD_REPO"]
BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
BUILDS = ["release"]
REVISIONS = ["7acb9a1", "8867cf3"] # random commit and latest commit from  2026-01-15
CONFIG_NICKS = [
    ("landmark-approximate", ["--search", "let(hlm, landmark_sum(lm_reasonable_orders_hps(lm_rhw()),pref=false, axioms=approximate_negative), lazy_greedy([hlm],reopen_closed=false))"]),
    ("landmark-approximate-cycles", ["--search", "let(hlm, landmark_sum(lm_reasonable_orders_hps(lm_rhw()),pref=false, axioms=approximate_negative_cycles), lazy_greedy([hlm],reopen_closed=false))"]),
    ("landmark-unrolling", ["--search", "let(hlm, landmark_sum(lm_reasonable_orders_hps(lm_rhw()),pref=false, axioms=exact_negative_cycles), lazy_greedy([hlm],reopen_closed=false))"]),
    ("eager-greedy-add-approximate", ["--search", "eager_greedy([add(axioms=approximate_negative)])"]),
    ("eager-greedy-add-approximate-cycle", ["--search", "eager_greedy([add(axioms=approximate_negative_cycles)])"]),
    ("eager-greedy-add-unrolling", ["--search", "eager_greedy([add(axioms=exact_negative_cycles)])"]),
    ("eager-greedy-ff-approximate", ["--search", "eager_greedy([ff(axioms=approximate_negative)])"]),
    ("eager-greedy-ff-approximate-cycle", ["--search", "eager_greedy([ff(axioms=approximate_negative_cycles)])"]),
    ("eager-greedy-ff-unrolling", ["--search", "eager_greedy([ff(axioms=exact_negative_cycles)])"]),
]

CONFIGS = [
    IssueConfig(
        config_nick, config, build_options=[build], driver_options=["--build", build]
    )
    for build in BUILDS
    for config_nick, config in CONFIG_NICKS
]

SUITE = common_setup.DEFAULT_SATISFICING_SUITE + ["drones-horndl", "queens-horndl", "psr-middle", "psr-large"] # all suites + those that use unrolling

ENVIRONMENT = BaselSlurmEnvironment(
    partition="infai_2",
    email="patrick01.weber@stud.unibas.ch",
    memory_per_cpu="3872M",
    export=["PATH"],
)

if common_setup.is_test_run():
    SUITE = ["psr-middle:p08-s40-n3-l4-f10.pddl"]
    ENVIRONMENT = LocalEnvironment(processes=1)

exp = IssueExperiment(
    REPO_DIR,
    revisions=REVISIONS,
    configs=CONFIGS,
    environment=ENVIRONMENT,
)
exp.add_suite(BENCHMARKS_DIR, SUITE)

exp.add_parser(exp.EXITCODE_PARSER)
exp.add_parser(exp.SINGLE_SEARCH_PARSER)
exp.add_parser(exp.PLANNER_PARSER)
exp.add_parser(unrolling_parser())

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

SPECIAL_ATTRIBUTES = [Attribute("unrolling_axioms", absolute=True), Attribute("unrolling_variables", absolute=True)]
ATTRIBUTES = exp.DEFAULT_TABLE_ATTRIBUTES + SPECIAL_ATTRIBUTES
SCATTER_ATTRIBUTES = ["planner_time", "search_time", "memory", "initial_h_value", "expansions", "evaluations", "generated" "cost"]

exp.add_absolute_report_step(attributes=ATTRIBUTES)
exp.add_comparison_table_step(attributes=ATTRIBUTES)
#exp.add_step("make-comparison-tables", create_comparative_report, [exp, CONFIG_NICKS, REVISIONS, ATTRIBUTES, 2])
#exp.add_scatter_plot_step(relative=False, attributes=["planner_time", "search_time", "memory", "initial_h_value", "expansions", "evaluations"])
exp.add_step("make_scatter_plots", create_scatter_plot_report, [exp, CONFIG_NICKS, REVISIONS, SCATTER_ATTRIBUTES, 2])

#exp.add_archive_step(ARCHIVE_PATH)
#exp.add_archive_eval_dir_step(ARCHIVE_PATH)

exp.run_steps()

