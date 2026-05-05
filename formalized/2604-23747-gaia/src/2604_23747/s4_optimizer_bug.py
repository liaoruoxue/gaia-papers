"""Section 2.1: the CPU-offloaded optimizer bug in DeepSpeed.

This module formalizes (a) the precise mechanism of the bug in the gradient
accumulation routine, (b) its propagation through downstream training
frameworks (TRL, OpenRLHF, Llama-Factory), (c) the consequences for SFT
training dynamics (deflated gradient norms, shifted mean loss), and (d) the
fix and its validation.

Source: [@Limozin2026SFTthenRL, Sec. 2.1; Appendix C; Sec. 4 (Fig. 2)].
"""

from gaia.lang import claim, setting

# ---------------------------------------------------------------------------
# Setting: the gradient-accumulation contract
# ---------------------------------------------------------------------------

setup_gradient_accumulation_contract = setting(
    "**Gradient-accumulation contract.** Gradient accumulation processes "
    "a logical batch as a sequence of micro-batches, computing per-micro-"
    "batch gradients and *summing* them on the device before triggering "
    "an optimizer step. Formally, for K micro-batches with gradients "
    "$g_0, g_1, \\ldots, g_{K-1}$, the optimizer must receive the sum "
    "$g_0 + g_1 + \\cdots + g_{K-1}$ (or its mean) -- not just $g_0$. "
    "Any implementation that loses intermediate $g_i$ for $i \\geq 1$ "
    "violates the contract and silently changes the effective batch size.",
    title="Setting: the gradient-accumulation contract (sum across all micro-batches)",
)

setup_zero_offload = setting(
    "**ZeRO Stage 2 with CPU-offloaded Adam.** DeepSpeed [@DeepSpeed] "
    "ZeRO Stage 1 / 2 with optimizer offloading shards optimizer state "
    "(Adam moments) to CPU memory to reduce GPU memory consumption "
    "during SFT training. Gradients are accumulated on GPU during the "
    "micro-batch loop and copied to CPU for the optimizer to consume "
    "during the optimizer step.",
    title="Setting: DeepSpeed ZeRO Stage 1/2 with CPU-offloaded optimizer (memory saving)",
)

# ---------------------------------------------------------------------------
# Bug mechanism (claim because it can be questioned / verified)
# ---------------------------------------------------------------------------

claim_bug_mechanism = claim(
    "**Mechanism of the CPU-offloaded optimizer bug.** A bug in DeepSpeed's "
    "[@DeepSpeed] CPU-offloaded gradient accumulation routine causes only "
    "the *first* micro-batch's gradients to reach the optimizer. "
    "Specifically, the offloading code copies gradients to CPU inside an "
    "`else` branch that executes only when `micro_step_id == 0` (i.e., the "
    "first micro-batch); intermediate micro-batches accumulate gradients "
    "on GPU correctly but never trigger a copy. On the next full optimizer "
    "step, the CPU-side optimizer therefore sees only the first "
    "micro-batch's gradients rather than the accumulated sum "
    "[@Limozin2026SFTthenRL, Sec. 2.1].",
    title="Bug mechanism: only the first micro-batch's gradients are copied to CPU",
)

claim_bug_introduced_in_pr = claim(
    "**The bug was introduced in DeepSpeed PR #6550, September 2024.** "
    "It is therefore a *recent* regression rather than a long-standing "
    "issue, which explains why it was not surfaced earlier and why it "
    "primarily affects experiments published in late 2024-2026 "
    "[@Limozin2026SFTthenRL, Sec. 2.1, footnote 2; @DeepSpeed].",
    title="Bug origin: introduced in DeepSpeed PR #6550 (Sep 2024)",
)

# ---------------------------------------------------------------------------
# Propagation to downstream frameworks
# ---------------------------------------------------------------------------

claim_bug_propagation = claim(
    "**Downstream framework propagation: the bug affects any framework "
    "using DeepSpeed ZeRO Stage 1 or 2 with an offloaded optimizer.** "
    "Frameworks affected include TRL [@TRL], OpenRLHF [@OpenRLHF], and "
    "Llama-Factory [@LlamaFactory]. Specifically, LUFFY [@LUFFY] uses "
    "OpenRLHF for SFT, ReLIFT [@ReLIFT] uses Llama-Factory for SFT, "
    "and Prefix-RFT [@PrefixRFT] inherits its SFT baseline from LUFFY -- "
    "all three are therefore affected on the SFT side. Mixed-policy "
    "methods themselves are implemented in verl [@verl] which does not "
    "use DeepSpeed, so the bug only deflates the *baseline* side of "
    "every comparison [@Limozin2026SFTthenRL, Sec. 2.1].",
    title="Bug propagation: affects TRL, OpenRLHF, Llama-Factory; deflates baseline side only",
)

# ---------------------------------------------------------------------------
# Consequences (training-dynamics observations)
# ---------------------------------------------------------------------------

claim_grad_norm_suppressed = claim(
    "**Consequence: the buggy configuration reports substantially lower "
    "gradient norms than correct training.** Figure 2 (right) of the "
    "paper shows that the buggy OpenRLHF SFT exhibits a markedly lower "
    "gradient norm trace throughout training compared to (i) the "
    "patched optimizer, (ii) the GPU-resident OpenRLHF optimizer, and "
    "(iii) the verl FSDP optimizer. This is a direct empirical "
    "signature of the bug -- only the first micro-batch's gradients "
    "(rather than the K-fold accumulated sum) reach the optimizer, so "
    "the reported norms are roughly 1/K of the correct values "
    "[@Limozin2026SFTthenRL, Fig. 2 right; Sec. 4].",
    title="Consequence: gradient norms in buggy training are roughly 1/K of correct values",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 2 (right)",
        "caption": "Fig. 2 right: gradient norm trace; only the optimizer bug shifts the trace; loss-aggregation bug has no effect on grad norm.",
    },
)

claim_mean_loss_shifted = claim(
    "**Consequence: the buggy configuration produces a shifted mean SFT "
    "loss.** Figure 2 (left) of the paper shows that the buggy OpenRLHF "
    "SFT loss curve has both a shifted mean and high variability "
    "compared to the verl reference. Fixing the CPU-offloaded optimizer "
    "alone corrects the mean level but leaves the variability "
    "untouched (the variability is the loss-aggregation bug's "
    "signature, see s5 module). Fixing both bugs brings the loss "
    "curve in line with verl: correct mean, low variability "
    "[@Limozin2026SFTthenRL, Fig. 2 left; Sec. 4].",
    title="Consequence: optimizer bug shifts mean SFT loss (variability comes from the other bug)",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 2 (left)",
        "caption": "Fig. 2 left: SFT training loss; aggregation bug = variability, optimizer bug = mean shift, both fixes match verl.",
    },
)

# ---------------------------------------------------------------------------
# Fix and validation
# ---------------------------------------------------------------------------

claim_optimizer_fix = claim(
    "**Fix: move the `copy_gradients_to_cpu()` call outside the `else` "
    "branch.** The patch removes the `else:` guard so that the gradient "
    "copy executes after every micro-batch's accumulation, restoring "
    "the gradient-accumulation contract. The patch is two lines (one "
    "removed, one re-indented) in "
    "`deepspeed/runtime/zero/stage_1_and_2.py` "
    "[@Limozin2026SFTthenRL, Appendix C, Fig. 4].",
    title="Fix: remove the `else:` guard so gradient copy runs every micro-batch",
    metadata={
        "figure": "artifacts/2604.23747.pdf, Fig. 4 / Appendix C",
        "caption": "Fig. 4: two-line patch to deepspeed/runtime/zero/stage_1_and_2.py removing the else-guard around copy_gradients_to_cpu.",
    },
)

claim_optimizer_fix_validated = claim(
    "**The fix is validated against two independent baselines: the "
    "GPU-resident DeepSpeed optimizer in OpenRLHF and the PyTorch FSDP "
    "[@FSDP] optimizer in verl [@verl].** The patched DeepSpeed CPU-"
    "offload optimizer matches both reference baselines on average loss "
    "and on gradient norms, confirming that the fix restores correct "
    "gradient accumulation behavior. The fix has been merged upstream "
    "(DeepSpeed PR #7967) [@Limozin2026SFTthenRL, Sec. 2.1; Sec. 4; "
    "Appendix C].",
    title="Fix validated against two independent baselines (GPU-resident + verl FSDP); merged upstream",
)

__all__ = [
    "setup_gradient_accumulation_contract",
    "setup_zero_offload",
    "claim_bug_mechanism",
    "claim_bug_introduced_in_pr",
    "claim_bug_propagation",
    "claim_grad_norm_suppressed",
    "claim_mean_loss_shifted",
    "claim_optimizer_fix",
    "claim_optimizer_fix_validated",
]
