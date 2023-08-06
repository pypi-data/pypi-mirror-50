import pandas as pd
from pkg_resources import resource_filename

def get_data():
    sources = ["campaign_descriptions",
               "coupons",
               "promotions",
               "campaigns",
               "demographics",
               "transactions",
               "coupon_redemptions",
               "products"]

    return dict(
        map(lambda src: (src, pd.read_parquet(resource_filename("completejourney_py", f"data/{src}.parquet"))),
            sources))
