# Judge audit structural QA

This directory reports execution completeness, schema validity, response-identity
consistency across original and swapped orders, and confidence differences. It
does not display or code Judge justifications.

## Interpretation boundary

A flipped original-swapped pair is consistent with position sensitivity, but does not isolate position bias from stochastic run-to-run variability because each order is evaluated once.

The position table compares the selected underlying response identity rather
than raw A/B labels. Justification coding is a separate, subsequently blinded
manual stage.
