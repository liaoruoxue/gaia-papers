from gaia.lang import claim, setting, noisy_and

context = setting("Background context for this package.")
hypothesis = claim("A scientific hypothesis.")
evidence = claim("Supporting evidence.")
_strat = noisy_and([hypothesis], evidence, reason="Hypothesis supports evidence.")

__all__ = ["context", "hypothesis", "evidence"]
