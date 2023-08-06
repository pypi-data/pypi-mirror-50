Factor Analysis
===============

Your data is factorized into latent variables and noise parameters all within the same sample. 

`m` denotes sample length, 
`n` denotes number of features for the data sample
`k` denotes number of latent features to be represented for the data sample

`λ` denotes the factor
`z` denotes the latent variable of size `m` x `k`
`ϵ` denotes the noise parameters of size `m` x ``n`
`ψ` denotes the covariance of `ϵ`

Factor Analysis equation
------------------------

                x = μ + λz + ϵ

We determine `λ` and `ψ` using posterior distribution ( z | x ) by expectation maximisation. The method is useful to predict the factor variables from a posterior distribution known to the user provided the data you are processing can be fit into the equation.

```python

import tensorflow as tf

f = factor_analysis.factors.Factor(data, factor_analysis.posterior.Posterior(covariance_prior, means))

noise = factor_analysis.noise.Noise(f, f.posterior)

with tf.Session() as sess:
    print(f.create_factor().eval())
    print(noise.create_noise(f.create_factor()).eval())
```

