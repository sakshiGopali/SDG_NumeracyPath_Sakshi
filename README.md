# Numeracy Path

AI Final Project by Sakshi

AI Final Project prototype for [United Nations SDG 4](https://sdgs.un.org/goals/goal4).

## Run the demo

Open NumeracyPath.html in a modern web browser. The entire interface and model run
offline. The project uses HTML, CSS and JavaScript and requires no API key,
server or external dependency.

### How it works

The prototype covers three fraction skills with four authored questions per
skill. It starts each skill at 0.30 and applies Bayesian Knowledge Tracing.
For a correct answer the likelihoods are 0.88 if the skill is known and 0.25
otherwise. For an incorrect answer the likelihoods are 0.12 and 0.75. After
Bayes' rule, the learner transitions to the known state with probability 0.10.
The scheduler selects the lowest-estimated skill, using listed order for ties.
The probabilities are demonstration parameters chosen by the author.

### Try the key interaction

1. Answer “Equivalent to 1/2?” with “2/4”. The first skill rises from 30% to 64%.
2. Select **Next question**. The comparison skill is selected at 30%.
3. Select an incorrect answer and inspect the explanation and changed estimate.
4. Select **Reset session** to return all skills to 30%.

### Scope

Progress stays in memory for the current session. The estimates are practice
signals, and the fixed item bank is unsuitable for formal assessment.

## License

This source package includes an MIT license.

## Project files

- [Sakshi's GitHub repository](https://github.com/sakshiGopali/SDG_NumeracyPath_Sakshi)

- [Offline application and source](NumeracyPath.html)
- [Sakshi's assignment report](SDG_NumeracyPath_Sakshi.pdf)
- [Proof-of-work screenshots](screenshots/)
- [Standalone source archive](NumeracyPath-Source.zip)

## Update the repository link

Use Python on Windows with the dependencies in tools/requirements-report.txt.
Run tools/build_report.py with --repository-url followed by the confirmed
public HTTPS GitHub repository URL. The builder updates the named four-page
PDF and verifies that it contains the clickable link.
