"""Section 3: Preliminaries -- ARL formalism and LoRA.

Pure definitional content (settings) needed by later sections. The role
function $\\ell$, policy gradient (Eq. 2), and LoRA decomposition (Eq. 3)
are all introduced here.
"""

from gaia.lang import setting

# ---------------------------------------------------------------------------
# 3.1 ARL formalism
# ---------------------------------------------------------------------------

setup_trajectory = setting(
    "An LLM agent $\\pi_\\theta(c_t \\mid c_{<t})$ generates a trajectory "
    "$\\tau = (c_1, \\ldots, c_T)$ for an input query $q$, where each $c_t$ "
    "is a token. The trajectory interleaves reasoning tokens and tool-use "
    "tokens.",
    title="Trajectory definition (Eq. 1)",
)

setup_role_router = setting(
    "A **role-based router** is a deterministic function "
    "$\\ell : \\{1, \\ldots, T\\} \\to \\{r, a\\}$, where $\\ell(t)=r$ "
    "marks token $c_t$ as a reasoning token and $\\ell(t)=a$ marks it as a "
    "tool-use (action) token. In Search-R1 / DART, role boundaries are "
    "identified deterministically by special tokens such as `<think>`, "
    "`</think>`, `<search>`, `</search>`.",
    title="Role-based router $\\ell$",
)

setup_policy_gradient = setting(
    "The policy is optimized to maximize the expected reward "
    "$J(\\theta) = \\mathbb{E}[R(\\tau)]$. Its gradient is estimated as "
    "$$\\nabla_\\theta J(\\theta) \\approx "
    "\\mathbb{E}_{\\tau \\sim \\pi_\\theta}\\Big[ A(\\tau) \\sum_{t=1}^T "
    "\\nabla_\\theta \\log \\pi_\\theta(c_t \\mid c_{<t}) \\Big]$$ (Eq. 2), "
    "where $A(\\tau)$ is the advantage derived from $R(\\tau)$. In standard "
    "ARL the same parameter set $\\theta$ is updated using gradients from "
    "**both** reasoning and tool-use tokens, ignoring the role function "
    "$\\ell$.",
    title="Policy-gradient objective (Eq. 2)",
)

setup_masked_objective = setting(
    "A **token-level mask** $m = [m_1, \\ldots, m_T] \\in \\{0,1\\}^T$ can "
    "be inserted into Eq. 2 to selectively isolate parameter updates: "
    "$$\\nabla_\\theta J(\\theta) \\approx "
    "\\mathbb{E}_{\\tau \\sim \\pi_\\theta}\\Big[ \\sum_{t=1}^T "
    "\\nabla_\\theta \\log \\pi_\\theta(c_t \\mid c_{<t}) \\cdot A(\\tau) "
    "\\cdot m_t \\Big]$$ (Eq. 8). With $m_t \\equiv 1$ this recovers Eq. 2; "
    "with $m_t = \\mathbb{1}(t \\in \\mathcal{T}_\\text{reas})$ only "
    "reasoning tokens contribute, etc. This mask is the basic primitive "
    "behind both LEAS's gradient-masked training and DART.",
    title="Token-level masked policy gradient (Eq. 8)",
)

setup_token_partition = setting(
    "Define $\\mathcal{T}_\\text{reas} = \\{t : \\ell(t)=r\\}$ and "
    "$\\mathcal{T}_\\text{tool} = \\{t : \\ell(t)=a\\}$. These two sets "
    "form a disjoint partition of the trajectory's loss-bearing tokens.",
    title="Token-role partition $\\mathcal{T}_\\text{reas}, \\mathcal{T}_\\text{tool}$",
)

setup_kl_regularizer = setting(
    "All experiments use the standard RLHF KL-regularized objective "
    "$J(\\theta) = \\mathbb{E}_\\tau [R(\\tau) - \\beta\\, "
    "\\mathrm{KL}(\\pi_\\theta \\Vert \\pi_\\text{ref})]$ (Eq. 11) with "
    "fixed $\\beta = 0.001$ (Appendix A, B). The KL term acts as a "
    "token-level penalty discouraging large deviations from the reference "
    "policy. It is omitted from the main-text formulas for clarity but is "
    "active in all reported experiments.",
    title="KL-regularized objective (Eqs. 11-12, omitted from main text)",
)

# ---------------------------------------------------------------------------
# 3.2 LoRA
# ---------------------------------------------------------------------------

setup_lora = setting(
    "**Low-Rank Adaptation (LoRA)** [@Hu2022] freezes the pretrained weight "
    "matrix $W \\in \\mathbb{R}^{d \\times k}$ and introduces a low-rank "
    "trainable update $\\Delta W = B A$ with $B \\in \\mathbb{R}^{d \\times r}$, "
    "$A \\in \\mathbb{R}^{r \\times k}$, $r \\ll \\min(d,k)$. The forward "
    "pass becomes $h'_t = W h_t + B A h_t$ (Eq. 3). Only $A, B$ are updated "
    "during training. Standard LoRA applies the same $\\Delta W$ to **all** "
    "tokens of a trajectory.",
    title="LoRA (Eq. 3)",
)

# ---------------------------------------------------------------------------
# Reward design (Appendix B)
# ---------------------------------------------------------------------------

setup_em_reward = setting(
    "All experiments use a rule-based outcome reward: "
    "$r_\\phi(x, y) = \\mathrm{EM}(a_\\text{pred}, a_\\text{gold})$ "
    "(Eq. 13), where $a_\\text{pred}$ is the answer extracted from response "
    "$y$ and $a_\\text{gold}$ is the ground-truth answer. EM is the unique "
    "training signal -- no intermediate or format-based rewards are used.",
    title="Exact-Match reward (Eq. 13)",
)

setup_grpo_training = setting(
    "RL training uses GRPO via Verl [@Sheng2025] on Qwen2.5 backbones "
    "with an E5 retriever over the 2018 Wikipedia dump. Fixed "
    "hyperparameters: 100 optimization steps, rollout batch size 256, "
    "gradient batch size 64, temperature 1.0, top-$p$ 1.0, learning rate "
    "$1\\times10^{-6}$ (LoRA variants scaled $10\\times$ per [@Schulman2025]), "
    "KL coefficient $\\beta=0.001$, clip ratio $\\epsilon=0.2$, action "
    "budget $B=4$, top-3 retrieved passages. 8x NVIDIA A800 GPUs. "
    "BF16 + FlashAttention-2 + gradient checkpointing + FSDP offload + "
    "vLLM rollouts.",
    title="GRPO training setup (Appendix B.1)",
)

__all__ = [
    "setup_trajectory",
    "setup_role_router",
    "setup_policy_gradient",
    "setup_masked_objective",
    "setup_token_partition",
    "setup_kl_regularizer",
    "setup_lora",
    "setup_em_reward",
    "setup_grpo_training",
]
