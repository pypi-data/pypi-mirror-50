import pandas as pd
from pychattr.channel_attribution import MarkovModel

data = {
    "path": [
        "A >>> B >>> A >>> B >>> B >>> A",
        "A >>> B >>> B >>> A >>> A",
        "A >>> A"
    ],
    "conversions": [1, 1, 1],
    "revenue": [1, 1, 1],
    "cost": [1, 1, 1]
}

df = pd.DataFrame(data)

path_feature="path"
conversion_feature="conversions"
null_feature=None
revenue_feature="revenue"
cost_feature="cost"
separator=">>>"
k_order=1
n_simulations=10000
max_steps=None
return_transition_probs=True
random_state=26

# instantiate the model
mm = MarkovModel(path_feature=path_feature,
                 conversion_feature=conversion_feature,
                 null_feature=null_feature,
                 revenue_feature=revenue_feature,
                 cost_feature=cost_feature,
                 separator=separator,
                 k_order=k_order,
                 n_simulations=n_simulations,
                 max_steps=max_steps,
                 return_transition_probs=return_transition_probs,
                 random_state=random_state)

# fit the model
mm.fit(df)

print(mm.attribution_model_)
print(mm.transition_matrix_)
print(mm.removal_effects_)