
#include <torch/extension.h>

torch::Tensor computeCov3DForward(
	const torch::Tensor& scales,
	const torch::Tensor& uquats,
	const torch::Tensor& visibility_staus);

std::tuple<torch::Tensor, torch::Tensor> computeCov3DBackward(
  const torch::Tensor& scales,
	const torch::Tensor& uquats,
	const torch::Tensor& visibility_staus,
	const torch::Tensor& dL_dcov3Ds
);