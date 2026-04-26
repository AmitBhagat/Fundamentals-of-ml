import os
import shutil

final_sequence = [
    "content/foundations/index.md",
    "content/foundations/data_as_tensors.md",
    "content/foundations/coordinate_systems.md",
    "content/foundations/mathematical_notation.md",
    "content/foundations/computational_complexity.md",
    "content/foundations/numerical_stability.md",
    "content/foundations/quantization_math.md",
    "content/foundations/vector_databases.md",
    "content/discrete-math/index.md",
    "content/discrete-math/discrete_mathematics.md",
    "content/discrete-math/boolean_logic_and_complexity.md",
    "content/discrete-math/combinatorics.md",
    "content/discrete-math/graph_theory_basics.md",
    "content/discrete-math/trees_and_dags.md",
    "content/linear-algebra/index.md",
    "content/linear-algebra/scalars.md",
    "content/linear-algebra/vectors.md",
    "content/linear-algebra/vector_spaces.md",
    "content/linear-algebra/vector_norms_l1_l2.md",
    "content/linear-algebra/dot_product.md",
    "content/linear-algebra/linear_independence.md",
    "content/linear-algebra/basis_and_dimension.md",
    "content/linear-algebra/linear_transformations.md",
    "content/linear-algebra/determinants.md",
    "content/linear-algebra/matrices.md",
    "content/linear-algebra/matrix_inverse.md",
    "content/linear-algebra/matrix_multiplication.md",
    "content/linear-algebra/matrix_rank.md",
    "content/linear-algebra/orthogonality_and_projections.md",
    "content/linear-algebra/eigenvalues_and_eigenvectors.md",
    "content/linear-algebra/positive_definite_matrices.md",
    "content/linear-algebra/pca.md",
    "content/linear-algebra/svd.md",
    "content/linear-algebra/attention_mechanism_math.md",
    "content/numerical-methods/index.md",
    "content/numerical-methods/floating_point_and_machine_epsilon.md",
    "content/numerical-methods/numerical_stability.md",
    "content/numerical-methods/condition_number.md",
    "content/numerical-methods/matrix_decompositions_lu_qr_cholesky.md",
    "content/numerical-methods/iterative_solvers_cg.md",
    "content/numerical-methods/automatic_differentiation.md",
    "content/calculus/index.md",
    "content/calculus/derivatives.md",
    "content/calculus/partial_derivatives.md",
    "content/calculus/gradient.md",
    "content/calculus/chain_rule.md",
    "content/calculus/jacobian_matrix.md",
    "content/calculus/hessian_matrix.md",
    "content/calculus/taylor_series.md",
    "content/calculus/critical_points.md",
    "content/calculus/integral_calculus.md",
    "content/calculus/backpropagation_math.md",
    "content/differential-equations/index.md",
    "content/differential-equations/ordinary_differential_equations.md",
    "content/differential-equations/numerical_integration_euler_rungekutta.md",
    "content/differential-equations/stochastic_differential_equations.md",
    "content/differential-equations/partial_differential_equations.md",
    "content/probability/index.md",
    "content/probability/random_variables.md",
    "content/probability/probability_distributions.md",
    "content/probability/probability_density_functions_pdf.md",
    "content/probability/cumulative_distribution_functions_cdf.md",
    "content/probability/joint_distributions.md",
    "content/probability/conditional_probability.md",
    "content/probability/independence.md",
    "content/probability/mean_and_expectation.md",
    "content/probability/variance.md",
    "content/probability/standard_deviation.md",
    "content/probability/law_of_large_numbers.md",
    "content/probability/central_limit_theorem.md",
    "content/probability/bayes_theorem.md",
    "content/probability/discrete_probability_distributions_bernoulli_bernoulli.md",
    "content/probability/continuous_probability_distributions_normal_exponential.md",
    "content/probability/markov_chains.md",
    "content/probability/monte_carlo_methods.md",
    "content/statistics/index.md",
    "content/statistics/ordinary_least_squares_ols.md",
    "content/statistics/maximum_likelihood_estimation.md",
    "content/statistics/maximum_a_posteriori.md",
    "content/statistics/biasvariance_tradeoff.md",
    "content/statistics/types_of_hypothesis_h0_vs.md",
    "content/statistics/hypothesis_testing.md",
    "content/statistics/type_i_and_type_ii.md",
    "content/statistics/the_ztest.md",
    "content/statistics/ttest.md",
    "content/statistics/chisquare_test.md",
    "content/statistics/anova.md",
    "content/statistics/ab_testing.md",
    "content/statistics/confidence_intervals.md",
    "content/statistics/bootstrap_and_resampling.md",
    "content/statistics/bayesian_inference.md",
    "content/statistics/regression_diagnostics.md",
    "content/information-theory/index.md",
    "content/information-theory/selfinformation.md",
    "content/information-theory/entropy.md",
    "content/information-theory/joint_and_conditional_entropy.md",
    "content/information-theory/mutual_information.md",
    "content/information-theory/crossentropy_and_ml_loss.md",
    "content/information-theory/kl_divergence.md",
    "content/information-theory/information_geometry.md",
    "content/optimization/index.md",
    "content/optimization/gradient_descent.md",
    "content/optimization/stochastic_gradient_descent.md",
    "content/optimization/convex_optimization.md",
    "content/optimization/regularization_l1_l2.md",
    "content/optimization/momentum_and_nesterov.md",
    "content/optimization/adaptive_methods_adam_rmsprop.md",
    "content/optimization/learning_rate_schedules.md",
    "content/optimization/constrained_optimization_lagrange_kkt.md",
    "content/optimization/second_order_methods.md",
    "content/optimization/proximal_methods_and_admm.md",
    "content/optimization/loss_landscapes.md",
    "content/ml-architect/index.md",
    "content/ml-architect/linear_logistic_blueprints.md",
    "content/ml-architect/decision_trees_geometry.md",
    "content/ml-architect/support_vector_frontier.md",
    "content/ml-architect/convolutional_geometry.md",
    "content/ml-architect/transformer_blueprint.md",
    "content/ml-architect/generative_manifolds.md",
    "content/reinforcement-learning/index.md",
    "content/reinforcement-learning/bellman_equation.md",
    "content/reinforcement-learning/mdp_dynamics.md",
    "content/reinforcement-learning/policy_gradients.md",
    "content/graph-ml/index.md",
    "content/graph-ml/adjacency_laplacian_math.md",
    "content/graph-ml/gcn_message_passing.md",
    "content/conclusion/the_road_ahead.md",
    "content/conclusion/closing_thoughts.md"
]

backup_dir = "drafts-backup"
backup_files = os.listdir(backup_dir)

# Map index files specifically
index_map = {
    "content/foundations/index.md": "1_introduction.md",
    "content/discrete-math/index.md": "93_discrete_mathematics.md",
    "content/linear-algebra/index.md": "4_linear_algebra.md",
    "content/numerical-methods/index.md": "86_numerical_methods.md",
    "content/calculus/index.md": "23_calculus.md",
    "content/differential-equations/index.md": "99_differential_equations.md",
    "content/probability/index.md": "33_probability.md",
    "content/statistics/index.md": "51_statistics.md",
    "content/information-theory/index.md": "68_information_theory.md",
    "content/optimization/index.md": "75_optimization.md"
}

for target in final_sequence:
    target_name = os.path.basename(target)
    
    if target in index_map:
        match = index_map[target]
    else:
        match = None
        for b in backup_files:
            if b.endswith("_" + target_name) or b == target_name or b[b.find('_')+1:] == target_name:
                match = b
                break
    
    if match and os.path.exists(os.path.join(backup_dir, match)):
        print(f"Restoring {match} to {target}")
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copy(os.path.join(backup_dir, match), target)
    else:
        print(f"FAILED to find backup for {target}")

print("Recovery complete.")
