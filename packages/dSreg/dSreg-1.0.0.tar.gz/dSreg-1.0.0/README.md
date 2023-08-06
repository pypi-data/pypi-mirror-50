# dSreg

dSreg is a library to perform joint inference of differential splicing and regulatory mechanisms using RNA-seq data. It uses [Stan](http://mc-stan.org/) through pystan interface to efficiently fit a fully probabilistic model integrating both layers of information under a bayesian framework. dSreg assumes an additive model of regulatory effects of a number of regulatorys that act by binding to their target sequences in the alternative splicing events and modify their inclusion rates. dSreg also allows random variation from this linear combination to accommodate splicing changes that remain unexplained by the regulatory elements introduced in the S matrix. This way, dSreg pools information across the whole set of alternative splicing event to infer changes in the regulatory system without the need to detect significant splicing changes. 

![dSreg graphical summary](https://bitbucket.org/cmartiga/dsreg/raw/master/images/fig1.png)

## Installation

Create a python3 virtual environment and activate it

```bash
virtualenv -p python3 dSreg
source dSreg/bin/activate
```

Download the repository using git and cd into it

```bash
git clone git@bitbucket.org:cmartiga/dSreg.git
cd dSreg
```

Install using setuptools
```bash
python setup.py install
```

You may need to update setuptools
```bash
pip install -U setuptools
```

Check that installation was succesful and dSreg options

```bash
dSreg -h
```

You may need to recompile the [Stan](http://mc-stan.org/) models fort them to work. For that:
```bash
compile_models
```

## Running dSreg

The main aim of dSreg is the inference of changes in the activity of regulatory elements driving splicing changes between two biological conditions.
To perform this analysis, dSreg requires 4 CSV input files with the following information

-	Inclusion counts matrix. Rows represent events and columns represent samples

-	Total counts matrix. Rows represent events and columns represent samples

-	Binding sites matrix. Rows represent events and columns represent regulatory features i.e. an RBP binding to a particular region

-	Design matrix. Matrix containing a single column with value 1 for samples belonging to one condition and 0 for the other

Example files to run dSreg can be found in the dSreg/test/dsreg_pw directory. To run dSreg:

```bash
dSreg -I test/inclusion.csv -T test/total.csv -S test/binding_sites.csv -d test/design.csv -o test/output
```

Fitting the model to the data may require some time. For testing purposes, you can use the -K option to set a small number of splicing events to sample and reduce computational burden.

```bash
dSreg -I test/inclusion.csv -T test/total.csv -S test/binding_sites.csv -d test/design.csv -o test/output -K 200
```

## dSreg Output

dSreg will write a number of CSV files with the provided *prefix* and the *model* used for fitting the data (*dSreg-PW* by default)

*	*output_prefix*.csv contains the full posterior probabilities for model parameters i.e. changes in the activity of the regulatory features

*	*output_prefix*.summary.csv contains a summary of the parameters including the split R to check MCMC convergence and effective samples size (ESS)

*	*output_prefix*.sampler_params.csv contains information about the sampler for MCMC diagnostics as described by [Michael Betancourt](https://betanalpha.github.io/assets/case_studies/rstan_workflow.html). However, warnings will be raised by [Stan](http://mc-stan.org/) in case of abnormal fitting.

*	*output_prefix*.regulators.csv contains the summarized output for the inferred changes in the activity of the regulatory elements (dTheta)

|    | E[dTheta]           | dTheta_p2.5           | dTheta_p97.5       | P(asb(dTheta)>0) | 
|----|---------------------|-----------------------|--------------------|-----------------| 
| 41 | 1.948365833786224   | -0.004154537329472519 | 3.8087565867774904 | 0.96975         | 
| 35 | 0.3131432161555559  | -0.21365117436546677  | 2.201200749538354  | 0.69425         | 
| 13 | 0.2446195116215051  | -0.20375418818201496  | 1.5953932313630386 | 0.68525         | 
| 16 | 0.22229829118760894 | -0.122586963249107    | 1.0362600232652692 | 0.769           | 
| 47 | 0.16066027540033892 | -0.19140608227507724  | 1.0753606734100378 | 0.679           | 

dSreg by default only stores parameters related to the regulatory elements. However. it also allows obtaining estimations from the splicing changes derived from these regulatory mechanisms. To save this information use the -a option.

```bash
dSreg -I test/inclusion.csv -T test/total.csv -S test/binding_sites.csv -d test/design.csv -o test/output -a
```

It will add new columns to the posterior distribution file and a new file *output_prefix*.events.csv with the summary information for splicing changes (dPSI)

|      | E[PSI_1]            | E[PSI_2]            | E[dPSI]             | dPSI_p2.5             | dPSI_p97.5         | P(abs(dPSI)>0.05) | 
|------|---------------------|---------------------|---------------------|-----------------------|--------------------|------------------| 
| 394  | 0.35797020898668946 | 0.6592066346257464  | 0.3012364256390573  | -0.034060204957281466 | 0.6040006975395776 | 0.9275           | 
| 335  | 0.35426995762681573 | 0.6036697451873659  | 0.24939978756055092 | -0.09546364300220359  | 0.5794646276014399 | 0.87075          | 
| 245  | 0.20273459974014146 | 0.43693354214665786 | 0.23419894240651679 | -0.041823843780665074 | 0.5117504145643708 | 0.90875          | 
| 381  | 0.3418296643884672  | 0.5744287488967228  | 0.23259908450825809 | -0.09502987456288116  | 0.5490660180673584 | 0.8595           | 
| 1072 | 0.41830419341652747 | 0.6447436824470557  | 0.22643948903052916 | -0.09934419118412881  | 0.5358810889956022 | 0.852            | 

The output can be plotted for **visualization** purposes with dsreg_plot tool:

```bash
dsreg_plot output_prefix.csv -a -o output_prefix.model.png -r  output_prefix.model.rbp_names
```
![Results visualization](https://bitbucket.org/cmartiga/dsreg/raw/master/images/dsreg_output.png)

## Citation

dSreg: A bayesian model to integrate changes in splicing and RNA binding protein activity (2019). Carlos Martí-Gómez, Enrique Lara-Pezzi, Fátima Sánchez-Cabo. bioRxiv 595751; doi:[https://doi.org/10.1101/595751](https://doi.org/10.1101/595751) 

## Paper code

All the code to reproduce the analysis in the paper can be found at [dsreg_paper](https://bitbucket.org/cmartiga/dsreg_paper) repository.
