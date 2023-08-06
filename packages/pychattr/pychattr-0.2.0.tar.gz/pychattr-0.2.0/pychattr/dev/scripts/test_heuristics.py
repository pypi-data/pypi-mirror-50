import pandas as pd
from pychattr.channel_attribution import HeuristicModel

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
first_touch=True
last_touch=True
linear_touch=True
ensemble_results=True

# instantiate the model
hm = HeuristicModel(path_feature=path_feature,
                    conversion_feature=conversion_feature,
                    null_feature=null_feature,
                    revenue_feature=revenue_feature,
                    cost_feature=cost_feature,
                    separator=separator,
                    first_touch=first_touch,
                    last_touch=last_touch,
                    linear_touch=linear_touch,
                    ensemble_results=ensemble_results)

# fit the model
hm.fit(df)


print(hm.attribution_model_)