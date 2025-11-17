#! /usr/bin/env python3

import os

from lab.environments import LocalEnvironment, BaselSlurmEnvironment

import common_setup
from common_setup import IssueConfig, IssueExperiment


ARCHIVE_PATH = "ai/downward/unrolling"
REPO_DIR = os.environ["DOWNWARD_REPO"]
BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
BUILDS = ["release"]
REVISIONS = ["29b7a43"] # latest commit from  2025-11-14
CONFIG_NICKS = [
    ("eager-greedy-add-unrolling", ["--search", "eager_greedy([add(axioms=exact_negative_cycles)])"]),
    ("eager-greedy-add-approximate", ["--search", "eager_greedy([add(axioms=approximate_negative_cycles)])"]),
]

CONFIGS = [
    IssueConfig(
        config_nick, config, build_options=[build], driver_options=["--build", build]
    )
    for build in BUILDS
    for config_nick, config in CONFIG_NICKS
]

SUITE = common_setup.DEFAULT_OPTIMAL_SUITE

ENVIRONMENT = BaselSlurmEnvironment(
    partition="infai_3",
    email="patrick01.weber@stud.unibas.ch",
    memory_per_cpu="3872M",
    export=["PATH"],
)

if common_setup.is_test_run():
    SUITE = IssueExperiment.DEFAULT_TEST_SUITE
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

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

SPECIAL_ATTRIBUTES = ["unrolling_axioms"] # TODO: Find out how to make this work
ATTRIBUTES = exp.DEFAULT_TABLE_ATTRIBUTES + SPECIAL_ATTRIBUTES
SCATTER_ATTRIBUTES = SPECIAL_ATTRIBUTES

exp.add_absolute_report_step(attributes=ATTRIBUTES)
exp.add_comparison_table_step(attributes=ATTRIBUTES)
exp.add_scatter_plot_step(relative=False, attributes=["search_time", "expansions", "evaluations"])

#exp.add_archive_step(ARCHIVE_PATH)
#exp.add_archive_eval_dir_step(ARCHIVE_PATH)

exp.run_steps()

