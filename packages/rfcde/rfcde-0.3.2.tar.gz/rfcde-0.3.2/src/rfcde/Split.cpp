// Copyright Taylor Pospisil 2018.
// Distributed under MIT License (http://opensource.org/licenses/MIT)

#include <vector>
#include <algorithm>
#include <random>
#include "Split.h"
#include "helpers.h"

typedef std::vector<int>::iterator ivecit;

Split find_best_split(double* x_train, double* z_basis,
                      const std::vector<int>& weights,
                      ivecit idx_begin, ivecit idx_end,
                      int n_train, int n_basis, int n_var, int mtry,
                      int node_size, int& last_var) {
  Split best_split;

  // Initialize total_sum and total_weight
  int total_weight = 0;
  std::vector<double> total_sum(n_basis, 0.0);
  for (auto it = idx_begin; it != idx_end; ++it) {
    total_weight += weights[*it];
    for (int bb = 0; bb < n_basis; bb++) {
      total_sum[bb] += z_basis[bb * n_train + *it] * weights[*it];
    }
  }

  // Can quit early if not enough weight for split
  if (total_weight < 2 * node_size) {
    return best_split;
  }

  double initial_loss = 0.0;
  for (int bb = 0; bb < n_basis; bb++) {
    initial_loss -= total_sum[bb] / total_weight * total_sum[bb];
  }

  static auto rng = std::default_random_engine {};
  std::vector<int> vars(n_var);
  std::iota(vars.begin(), vars.end(), 0);
  std::shuffle(vars.begin(), vars.end(), rng);

  for (int ii = 0; ii < mtry; ii++) {
    int var = vars[ii];
    if (var != last_var) {
      sortby(idx_begin, idx_end, &x_train[var * n_train]);
      last_var = var;
    }

    Split split = evaluate_split(&x_train[var * n_train],
                                 z_basis, weights, idx_begin, idx_end,
                                 n_train, n_basis, node_size,
                                 total_weight, total_sum);

    if (split.loss_delta < best_split.loss_delta) {
      best_split = split;
      best_split.var = var;
    }
  }

  best_split.loss_delta = initial_loss - best_split.loss_delta;
  return best_split;
}

Split evaluate_split(const double* x_train, const double* z_basis,
                     const std::vector<int>& weights,
                     const ivecit idx_begin, const ivecit idx_end,
                     int n_train, int n_basis, int node_size,
                     int total_weight, const std::vector<double>& total_sum) {
  // Finds the best split given an ordering of observations.
  //
  // Find best_split by incrementing through each observation
  // maintaining a running sum of the basis function values. Then
  // evaluating loss as -\sum_{j} \beta_{j}^{2} where
  // \beta_{j} = \sum_{i} w_{i}\beta_{j}(x_{i}) / \sum_{i} w_{i}
  // for each side of the split.
  //
  // Arguments:
  //   x_train: pointer to covariate vector.
  //   z_basis: pointer to basis function evaluations.
  //   weights: vector of bootstrap weights.
  //   idx: pointer to array of valid indices.
  //   n_train: number of observations, length of weights.
  //   n_basis: number of basis functions.
  //   n_idx: number of valid indices.
  //   node_size: minimum weight for a leaf node.
  //   total_weight: sum of weights for valid indices. Computed
  //     outside of this function as it can be reused for other
  //     splits.
  //   total_sum: vector of weighted sums of basis functions. Computed
  //     outside of this function as it can be reused for other
  //     splits.
  //
  // Returns: a Split object containing the best split loss and offset.
  int le_weight = 0;
  std::vector<double> le_sum(n_basis, 0.0);

  Split split;
  split.loss_delta = 0.0; // initialize zero as losses are negative
  split.offset = -1;
  for (auto it = idx_begin; it != idx_end; ++it) {
    // Update for next observation
    le_weight += weights[*it];
    for (int bb = 0; bb < n_basis; bb++) {
      le_sum[bb] += z_basis[n_train * bb + *it] * weights[*it];
    }

    // Enforce node_size constraint on minimum weight in a leaf node.
    if (le_weight < node_size) { continue; };
    if (total_weight - le_weight < node_size) { break; }

    // Enforce <= constraint
    if (x_train[*it] == x_train[*(it + 1)]) { continue; }

    // Calculate loss
    double loss = 0.0;
    for (int bb = 0; bb < n_basis; bb++) {
      loss -= le_sum[bb] * le_sum[bb] / le_weight;
      loss -= (total_sum[bb] - le_sum[bb]) * (total_sum[bb] - le_sum[bb]) /
        (total_weight - le_weight);
    }

    if (loss < split.loss_delta) {
      split.loss_delta = loss;
      split.offset = it - idx_begin;
    }
  }

  return split;
}
