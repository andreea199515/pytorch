# Owner(s): ["module: functorch"]
from functools import wraps
import typing
import unittest

from torch.testing._internal.common_utils import (
    _TestParametrizer,
    TestCase,
    run_tests,
    instantiate_parametrized_tests,
)

from torch._C import (
    _dispatch_get_registrations_for_dispatch_key as get_registrations_for_dispatch_key,
)

xfail_functorch_batched = {
    "aten::flatten.using_ints",
    "aten::gather_backward",
    "aten::imag",
    "aten::is_nonzero",
    "aten::isfinite",
    "aten::isreal",
    "aten::item",
    "aten::linalg_matrix_power",
    "aten::linalg_matrix_rank.atol_rtol_float",
    "aten::linalg_matrix_rank.atol_rtol_tensor",
    "aten::linalg_pinv",
    "aten::linalg_pinv.atol_rtol_float",
    "aten::linalg_slogdet",
    "aten::linear",
    "aten::log_sigmoid",
    "aten::log_softmax.int",
    "aten::logdet",
    "aten::masked_select_backward",
    "aten::movedim.intlist",
    "aten::one_hot",
    "aten::real",
    "aten::relu6",
    "aten::relu6_",
    "aten::selu",
    "aten::selu_",
    "aten::silu_backward",
    "aten::special_xlogy",
    "aten::special_xlogy.other_scalar",
    "aten::special_xlogy.self_scalar",
    "aten::tensor_split.indices",
    "aten::tensor_split.sections",
    "aten::to.device",
    "aten::to.dtype",
    "aten::to.dtype_layout",
    "aten::to.other",
    "aten::upsample_bicubic2d.vec",
    "aten::upsample_bilinear2d.vec",
    "aten::upsample_linear1d.vec",
    "aten::upsample_nearest1d.vec",
    "aten::upsample_nearest2d.vec",
    "aten::upsample_nearest3d.vec",
    "aten::upsample_trilinear3d.vec",
    "aten::where",
}

xfail_functorch_batched_decomposition = {
    "aten::diagonal_copy",
    "aten::is_same_size",
    "aten::t",
    "aten::t_",
    "aten::unfold_copy",
}

xfail_not_implemented = {
    "aten::absolute_",
    "aten::affine_grid_generator_backward",
    "aten::align_as",
    "aten::align_tensors",
    "aten::align_to",
    "aten::align_to.ellipsis_idx",
    "aten::alpha_dropout",
    "aten::alpha_dropout_",
    "aten::arccos_",
    "aten::arccosh_",
    "aten::arcsin_",
    "aten::arcsinh_",
    "aten::arctan2_",
    "aten::arctan_",
    "aten::arctanh_",
    "aten::argwhere",
    "aten::bilinear",
    "aten::bitwise_and_.Scalar",
    "aten::bitwise_or_.Scalar",
    "aten::bitwise_xor_.Scalar",
    "aten::can_cast",
    "aten::cat.names",
    "aten::chain_matmul",
    "aten::chalf",
    "aten::choose_qparams_optimized",
    "aten::clip_",
    "aten::clip_.Tensor",
    "aten::coalesce",
    "aten::column_stack",
    "aten::concat.names",
    "aten::concatenate.names",
    "aten::conj",
    "aten::conv_tbc_backward",
    "aten::ctc_loss.IntList",
    "aten::ctc_loss.Tensor",
    "aten::cudnn_is_acceptable",
    "aten::cummaxmin_backward",
    "aten::cumprod_backward",
    "aten::data",
    "aten::diagflat",
    "aten::divide.out_mode",
    "aten::divide_.Scalar",
    "aten::dropout",
    "aten::dropout_",
    "aten::embedding_bag",
    "aten::embedding_bag.padding_idx",
    "aten::embedding_sparse_backward",
    "aten::fake_quantize_per_channel_affine",
    "aten::fake_quantize_per_channel_affine_cachemask_backward",
    "aten::fake_quantize_per_tensor_affine",
    "aten::fake_quantize_per_tensor_affine.tensor_qparams",
    "aten::fake_quantize_per_tensor_affine_cachemask_backward",
    "aten::fbgemm_linear_fp16_weight",
    "aten::fbgemm_linear_fp16_weight_fp32_activation",
    "aten::fbgemm_linear_int8_weight",
    "aten::fbgemm_linear_int8_weight_fp32_activation",
    "aten::fbgemm_linear_quantize_weight",
    "aten::fbgemm_pack_gemm_matrix_fp16",
    "aten::fbgemm_pack_quantized_matrix",
    "aten::fbgemm_pack_quantized_matrix.KN",
    "aten::feature_alpha_dropout",
    "aten::feature_alpha_dropout_",
    "aten::feature_dropout",
    "aten::feature_dropout_",
    "aten::fft_ihfft2",
    "aten::fft_ihfftn",
    "aten::fill_diagonal_",
    "aten::fix_",
    "aten::flatten.DimnameList",
    "aten::flatten.named_out_dim",
    "aten::flatten.using_ints",
    "aten::flatten.using_names",
    "aten::flatten_dense_tensors",
    "aten::float_power.Scalar",
    "aten::float_power_.Scalar",
    "aten::float_power_.Tensor",
    "aten::floor_divide_.Scalar",
    "aten::frobenius_norm",
    "aten::fused_moving_avg_obs_fake_quant",
    "aten::gather_backward",
    "aten::get_gradients",
    "aten::greater.Scalar",
    "aten::greater_.Scalar",
    "aten::greater_.Tensor",
    "aten::greater_equal.Scalar",
    "aten::greater_equal_.Scalar",
    "aten::greater_equal_.Tensor",
    "aten::gru.data",
    "aten::gru.input",
    "aten::gru_cell",
    "aten::histogramdd",
    "aten::histogramdd.TensorList_bins",
    "aten::histogramdd.int_bins",
    "aten::imag",
    "aten::index_fill.Dimname_Scalar",
    "aten::index_fill.Dimname_Tensor",
    "aten::index_fill_.Dimname_Scalar",
    "aten::index_fill_.Dimname_Tensor",
    "aten::infinitely_differentiable_gelu_backward",
    "aten::is_conj",
    "aten::is_distributed",
    "aten::is_floating_point",
    "aten::is_inference",
    "aten::is_leaf",
    "aten::is_neg",
    "aten::is_nonzero",
    "aten::is_signed",
    "aten::is_vulkan_available",
    "aten::isclose",
    "aten::isfinite",
    "aten::isreal",
    "aten::istft",
    "aten::item",
    "aten::kl_div",
    "aten::ldexp_",
    "aten::less.Scalar",
    "aten::less_.Scalar",
    "aten::less_.Tensor",
    "aten::less_equal.Scalar",
    "aten::less_equal_.Scalar",
    "aten::less_equal_.Tensor",
    "aten::linalg_cond.p_str",
    "aten::linalg_eigh",
    "aten::linalg_eigh.eigvals",
    "aten::linalg_ldl_factor",
    "aten::linalg_lu_factor",
    "aten::linalg_matrix_power",
    "aten::linalg_matrix_rank",
    "aten::linalg_matrix_rank.atol_rtol_float",
    "aten::linalg_matrix_rank.atol_rtol_tensor",
    "aten::linalg_matrix_rank.out_tol_tensor",
    "aten::linalg_matrix_rank.tol_tensor",
    "aten::linalg_pinv",
    "aten::linalg_pinv.atol_rtol_float",
    "aten::linalg_pinv.out_rcond_tensor",
    "aten::linalg_pinv.rcond_tensor",
    "aten::linalg_slogdet",
    "aten::linalg_svd.U",
    "aten::linalg_tensorsolve",
    "aten::linalg_vander",
    "aten::linalg_vecdot",
    "aten::linear",
    "aten::log_sigmoid",
    "aten::log_softmax.int",
    "aten::logdet",
    "aten::logsumexp.names",
    "aten::lstm.data",
    "aten::lstm.input",
    "aten::lstm_cell",
    "aten::lu_solve",
    "aten::margin_ranking_loss",
    "aten::masked_select_backward",
    "aten::matrix_exp",
    "aten::matrix_exp_backward",
    "aten::max.names_dim",
    "aten::max.names_dim_max",
    "aten::max_pool1d",
    "aten::max_pool3d",
    "aten::mean.names_dim",
    "aten::median.names_dim",
    "aten::median.names_dim_values",
    "aten::min.names_dim",
    "aten::min.names_dim_min",
    "aten::mish_backward",
    "aten::moveaxis.int",
    "aten::movedim.intlist",
    "aten::multilabel_margin_loss",
    "aten::nanmean",
    "aten::nanmedian.names_dim",
    "aten::nanmedian.names_dim_values",
    "aten::nanquantile",
    "aten::nanquantile.scalar",
    "aten::narrow.Tensor",
    "aten::native_channel_shuffle",
    "aten::negative_",
    "aten::nested_to_padded_tensor",
    "aten::nonzero_numpy",
    "aten::norm.names_ScalarOpt_dim",
    "aten::norm.names_ScalarOpt_dim_dtype",
    "aten::norm_except_dim",
    "aten::not_equal.Scalar",
    "aten::not_equal_.Scalar",
    "aten::not_equal_.Tensor",
    "aten::one_hot",
    "aten::output_nr",
    "aten::pad_sequence",
    "aten::pdist",
    "aten::pin_memory",
    "aten::promote_types",
    "aten::qr.Q",
    "aten::quantile",
    "aten::quantile.scalar",
    "aten::quantized_gru_cell",
    "aten::quantized_lstm_cell",
    "aten::quantized_rnn_relu_cell",
    "aten::quantized_rnn_tanh_cell",
    "aten::real",
    "aten::refine_names",
    "aten::relu6",
    "aten::relu6_",
    "aten::rename",
    "aten::rename_",
    "aten::requires_grad_",
    "aten::retain_grad",
    "aten::retains_grad",
    "aten::rnn_relu.data",
    "aten::rnn_relu.input",
    "aten::rnn_relu_cell",
    "aten::rnn_tanh.data",
    "aten::rnn_tanh.input",
    "aten::rnn_tanh_cell",
    "aten::rrelu_",
    "aten::scatter.dimname_src",
    "aten::scatter.dimname_value",
    "aten::selu",
    "aten::selu_",
    "aten::set_.source_Tensor_storage_offset",
    "aten::set_data",
    "aten::silu_backward",
    "aten::slow_conv3d",
    "aten::smm",
    "aten::sort.dimname_stable",
    "aten::sort.dimname_values",
    "aten::sort.dimname_values_stable",
    "aten::sparse_bsc_tensor.ccol_row_value",
    "aten::sparse_bsc_tensor.ccol_row_value_size",
    "aten::sparse_bsr_tensor.crow_col_value",
    "aten::sparse_bsr_tensor.crow_col_value_size",
    "aten::sparse_compressed_tensor.comp_plain_value",
    "aten::sparse_compressed_tensor.comp_plain_value_size",
    "aten::sparse_coo_tensor.indices",
    "aten::sparse_coo_tensor.indices_size",
    "aten::sparse_csc_tensor.ccol_row_value",
    "aten::sparse_csc_tensor.ccol_row_value_size",
    "aten::sparse_csr_tensor.crow_col_value",
    "aten::sparse_csr_tensor.crow_col_value_size",
    "aten::special_chebyshev_polynomial_t.n_scalar",
    "aten::special_chebyshev_polynomial_t.x_scalar",
    "aten::special_chebyshev_polynomial_u.n_scalar",
    "aten::special_chebyshev_polynomial_u.x_scalar",
    "aten::special_chebyshev_polynomial_v.n_scalar",
    "aten::special_chebyshev_polynomial_v.x_scalar",
    "aten::special_chebyshev_polynomial_w.n_scalar",
    "aten::special_chebyshev_polynomial_w.x_scalar",
    "aten::special_hermite_polynomial_h.n_scalar",
    "aten::special_hermite_polynomial_h.x_scalar",
    "aten::special_hermite_polynomial_he.n_scalar",
    "aten::special_hermite_polynomial_he.x_scalar",
    "aten::special_laguerre_polynomial_l.n_scalar",
    "aten::special_laguerre_polynomial_l.x_scalar",
    "aten::special_legendre_polynomial_p.n_scalar",
    "aten::special_legendre_polynomial_p.x_scalar",
    "aten::special_shifted_chebyshev_polynomial_t.n_scalar",
    "aten::special_shifted_chebyshev_polynomial_t.x_scalar",
    "aten::special_shifted_chebyshev_polynomial_u.n_scalar",
    "aten::special_shifted_chebyshev_polynomial_u.x_scalar",
    "aten::special_shifted_chebyshev_polynomial_v.n_scalar",
    "aten::special_shifted_chebyshev_polynomial_v.x_scalar",
    "aten::special_shifted_chebyshev_polynomial_w.n_scalar",
    "aten::special_shifted_chebyshev_polynomial_w.x_scalar",
    "aten::special_xlogy",
    "aten::special_xlogy.other_scalar",
    "aten::special_xlogy.self_scalar",
    "aten::square_",
    "aten::sspaddmm",
    "aten::std.correction_names",
    "aten::std.names_dim",
    "aten::std_mean.correction_names",
    "aten::std_mean.names_dim",
    "aten::stft",
    "aten::stft.center",
    "aten::stride.int",
    "aten::subtract.Scalar",
    "aten::subtract_.Scalar",
    "aten::subtract_.Tensor",
    "aten::sum.dim_DimnameList",
    "aten::svd.U",
    "aten::tensor_split.indices",
    "aten::tensor_split.sections",
    "aten::tensor_split.tensor_indices_or_sections",
    "aten::thnn_conv2d",
    "aten::to.device",
    "aten::to.dtype",
    "aten::to.dtype_layout",
    "aten::to.other",
    "aten::to_dense",
    "aten::to_dense_backward",
    "aten::to_mkldnn_backward",
    "aten::trace_backward",
    "aten::triplet_margin_loss",
    "aten::unflatten_dense_tensors",
    "aten::unsafe_chunk",
    "aten::upsample_bicubic2d.vec",
    "aten::upsample_bilinear2d.vec",
    "aten::upsample_linear1d.vec",
    "aten::upsample_nearest1d.vec",
    "aten::upsample_nearest2d.vec",
    "aten::upsample_nearest3d.vec",
    "aten::upsample_trilinear3d.vec",
    "aten::vander",
    "aten::var.correction_names",
    "aten::var.names_dim",
    "aten::var_mean.correction_names",
    "aten::var_mean.names_dim",
    "aten::where",
    "aten::where.Scalar",
}


class dispatch_registrations(_TestParametrizer):
    def __init__(
        self,
        dispatch_key: str,
        xfails: set,
        filter_func: typing.Callable = lambda reg: True,
    ):
        self.registrations = sorted(get_registrations_for_dispatch_key(dispatch_key))
        self.xfails = xfails
        self.filter_func = filter_func

    def _parametrize_test(self, test, generic_cls, device_cls):
        for registration in self.registrations:
            if not self.filter_func(registration):
                continue

            @wraps(test)
            def test_wrapper(*args, **kwargs):
                return test(*args, **kwargs)

            if registration in self.xfails:
                test_wrapper = unittest.expectedFailure(test_wrapper)

            yield (test_wrapper, f"[{registration}]", {"registration": registration})


CompositeImplicitAutogradRegistrations = set(
    get_registrations_for_dispatch_key("CompositeImplicitAutograd")
)
FuncTorchBatchedRegistrations = set(
    get_registrations_for_dispatch_key("FuncTorchBatched")
)
FuncTorchBatchedDecompositionRegistrations = set(
    get_registrations_for_dispatch_key("FuncTorchBatchedDecomposition")
)


def filter_vmap_implementable(reg):
    reg = reg.lower()
    if not reg.startswith("aten::"):
        return False
    if reg.startswith("aten::_"):
        return False
    if reg.endswith(".out"):
        return False
    if reg.endswith("_out"):
        return False
    if reg.endswith(".dimname"):
        return False
    if reg.endswith("_dimname"):
        return False
    return True


class TestFunctorchDispatcher(TestCase):
    @dispatch_registrations("CompositeImplicitAutograd", xfail_functorch_batched)
    def test_register_a_batching_rule_for_composite_implicit_autograd(
        self, registration
    ):
        assert registration not in FuncTorchBatchedRegistrations, (
            f"You've added a batching rule for a CompositeImplicitAutograd operator {registration}. "
            "The correct way to add vmap support for it is to put it into BatchRulesDecomposition to "
            "reuse the CompositeImplicitAutograd decomposition"
        )

    @dispatch_registrations(
        "FuncTorchBatchedDecomposition", xfail_functorch_batched_decomposition
    )
    def test_register_functorch_batched_decomposition(self, registration):
        assert registration in CompositeImplicitAutogradRegistrations, (
            f"The registrations in BatchedDecompositions.cpp must be for CompositeImplicitAutograd "
            f"operations. If your operation {registration} is not CompositeImplicitAutograd, "
            "then please register it to the FuncTorchBatched key in another file."
        )

    @dispatch_registrations(
        "CompositeImplicitAutograd", xfail_not_implemented, filter_vmap_implementable
    )
    def test_unimplemented_batched_registrations(self, registration):
        assert registration in FuncTorchBatchedDecompositionRegistrations, (
            f"Please add a registration in BatchedDecompositions.cpp for "
            f"the CompositeImplicitAutograd registration {registration}"
        )


instantiate_parametrized_tests(TestFunctorchDispatcher)

if __name__ == "__main__":
    run_tests()
