#!/usr/bin/env python

import pytest
from .data_generator import generate_project
import os
from peppy import Project
from ngs_toolkit.atacseq import ATACSeqAnalysis
import shutil


@pytest.fixture
def analysis(tmp_path):
    tmp_path = str(tmp_path)  # for Python2

    # Let's make several "reallish" test projects
    to_test = list()
    project_prefix_name = "test-project"
    data_type = "ATAC-seq"
    genome_assemblies = [("human", "hg19"), ("human", "hg38"), ("mouse", "mm10")]

    n_factors = 2
    n_variables = 5000
    n_replicates = 5
    for organism, genome_assembly in [genome_assemblies[0]]:
        project_name = "{}_{}_{}_{}_{}_{}".format(
            project_prefix_name,
            data_type,
            genome_assembly,
            n_factors,
            n_variables,
            n_replicates,
        )

        generate_project(
            output_dir=tmp_path,
            project_name=project_name,
            genome_assembly=genome_assembly,
            data_type=data_type,
            n_factors=n_factors,
            n_replicates=n_replicates,
            n_variables=n_variables,
            group_fold_differences=[10, 5],
            fraction_of_different=0.2,
        )

        # first edit the defaul path to the annotation sheet
        config = os.path.join(tmp_path, project_name, "metadata", "project_config.yaml")
        prj_path = os.path.join(tmp_path, project_name)
        os.chdir(prj_path)

        # project and associated analysis
        a = ATACSeqAnalysis(
            name=project_name,
            prj=Project(config),
            results_dir=os.path.join(prj_path, "results"),
        )
        a.set_project_attributes()
        a.load_data()

        a.normalize(method="rpm")
        a.annotate_samples()

        to_test.append(a)
    return to_test[0]


@pytest.fixture
def outputs(analysis):
    prefix = os.path.join(
        analysis.results_dir,
        "unsupervised_analysis_ATAC-seq",
        analysis.name + ".all_{}s.".format(analysis.var_unit_name),
    )
    outputs = [
        prefix + "isomap.svg",
        prefix + "locallylinearembedding.svg",
        prefix + "mds.svg",
        prefix + "pca.explained_variance.csv",
        prefix + "pca.explained_variance.svg",
        prefix + "pca.svg",
        prefix + "pca.variable_principle_components_association.csv",
        prefix + "pca.variable_principle_components_association.p_value.masked.svg",
        prefix + "pca.variable_principle_components_association.p_value.svg",
        prefix + "pca.variable_principle_components_association.adj_pvalue.masked.svg",
        prefix + "pca.variable_principle_components_association.adj_pvalue.svg",
        prefix + "pearson_correlation.clustermap.svg",
        prefix + "spearman_correlation.clustermap.svg",
        prefix + "spectralembedding.svg",
        prefix + "tsne.svg",
    ]
    return outputs


class TestUnsupervisedAnalysis:
    def test_no_arguments(self, analysis, outputs):
        # no arguments
        analysis.unsupervised_analysis()
        for output in outputs:
            assert os.path.exists(output)
            assert os.stat(output).st_size > 0

    def test_matrix_with_no_multiindex(self, analysis):
        analysis.unsupervised_analysis(matrix="matrix_raw")
        assert os.path.exists(
            os.path.join(analysis.results_dir, "unsupervised_analysis_ATAC-seq")
        )

    def test_various_matrices(self, analysis, outputs):
        for matrix in ["matrix_raw", "matrix_norm"]:
            analysis.annotate_samples(matrix=matrix)
            analysis.unsupervised_analysis()
            for output in outputs:
                assert os.path.exists(output)
                assert os.stat(output).st_size > 0
            shutil.rmtree(
                os.path.join(analysis.results_dir, "unsupervised_analysis_ATAC-seq")
            )
        # analysis.annotate_samples(matrix="coverage_qnorm")

    def test_too_low_numbers_of_samples_error(self, analysis):
        for i in range(2):
            with pytest.raises(ValueError):
                analysis.unsupervised_analysis(samples=analysis.samples[:i])
            assert os.path.exists(
                os.path.join(analysis.results_dir, "unsupervised_analysis_ATAC-seq")
            )
            shutil.rmtree(
                os.path.join(analysis.results_dir, "unsupervised_analysis_ATAC-seq")
            )

    def test_low_samples_no_manifolds(self, analysis):
        prefix = os.path.join(
            analysis.results_dir,
            "unsupervised_analysis_ATAC-seq",
            analysis.name + ".all_{}s.".format(analysis.var_unit_name),
        )
        outputs2 = [
            prefix + "mds.svg",
            prefix + "pca.explained_variance.csv",
            prefix + "pca.explained_variance.svg",
            prefix + "pca.svg",
            prefix + "pearson_correlation.clustermap.svg",
            prefix + "spearman_correlation.clustermap.svg",
            prefix + "tsne.svg",
            prefix + "pca.variable_principle_components_association.csv",
        ]
        not_outputs = [
            prefix + "isomap.svg",
            prefix + "locallylinearembedding.svg",
            prefix + "spectralembedding.svg",
            prefix + "pca.variable_principle_components_association.p_value.masked.svg",
            prefix
            + "pca.variable_principle_components_association.adj_pvalue.masked.svg",
            prefix + "pca.variable_principle_components_association.p_value.svg",
            prefix + "pca.variable_principle_components_association.adj_pvalue.svg",
        ]
        # here I'm picking the first and last samples just to make sure
        # they are from different values of attributes `a` and `b`
        analysis.unsupervised_analysis(samples=[analysis.samples[0]] + [analysis.samples[-1]])
        for output in outputs2:
            assert os.path.exists(output)
            assert os.stat(output).st_size > 0
        for output in not_outputs:
            assert not os.path.exists(output)

    # def test_high_samples_varying_all_outputs(self, analysis, outputs):
    #     for i in range(4, len(analysis.samples), 2):
    #         print(i)
    #         analysis.unsupervised_analysis(samples=analysis.samples[i:])
    #         for output in outputs:
    #             assert os.path.exists(output)
    #             assert os.stat(output).st_size > 0
    #         shutil.rmtree(os.path.join(analysis.results_dir, "unsupervised_analysis_ATAC-seq"))

    def test_no_plotting_attributes(self, analysis):
        with pytest.raises(ValueError):
            analysis.unsupervised_analysis(attributes_to_plot=[])
        assert os.path.exists(
            os.path.join(analysis.results_dir, "unsupervised_analysis_ATAC-seq")
        )

    def test_various_plotting_attributes(self, analysis, outputs):
        prefix = os.path.join(
            analysis.results_dir,
            "unsupervised_analysis_ATAC-seq",
            analysis.name + ".all_{}s.".format(analysis.var_unit_name),
        )
        not_outputs = [
            prefix + "pca.variable_principle_components_association.p_value.masked.svg",
            prefix + "pca.variable_principle_components_association.p_value.svg",
            prefix
            + "pca.variable_principle_components_association.adj_pvalue.masked.svg",
            prefix + "pca.variable_principle_components_association.adj_pvalue.svg",
        ]
        for i in range(1, len(analysis.group_attributes)):
            analysis.unsupervised_analysis(
                attributes_to_plot=analysis.group_attributes[:i]
            )
            for output in outputs:
                if output not in not_outputs:
                    assert os.path.exists(output)
                    assert os.stat(output).st_size > 0
            for output in not_outputs:
                assert not os.path.exists(output)
            shutil.rmtree(
                os.path.join(analysis.results_dir, "unsupervised_analysis_ATAC-seq")
            )

    def test_various_plot_prefixes_attributes(self, analysis, outputs):
        analysis.unsupervised_analysis(plot_prefix="test")
        for output in outputs:
            assert os.path.exists(
                output.replace("all_{}s".format(analysis.var_unit_name), "test")
            )
            assert (
                os.stat(
                    output.replace("all_{}s".format(analysis.var_unit_name), "test")
                ).st_size
                > 0
            )

    def test_standardized_matrix(self, analysis, outputs):
        analysis.unsupervised_analysis(standardize_matrix=True)
        for output in outputs:
            assert os.path.exists(output)
            assert os.stat(output).st_size > 0
