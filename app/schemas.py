from pydantic import BaseModel
from typing import List

# customer schema
class CustomerFeatures(BaseModel):

    recency_days: float
    frequency_180d: float
    monetary_180d: float
    return_rate_180d: float
    avg_discount_pct_180d: float
    avg_rating_180d: float
    category_diversity_180d: float

    ticket_count_90d: float
    negative_ticket_rate_90d: float
    avg_resolution_hours_90d: float

    days_since_signup: float

    sessions_30d: float
    product_views_30d: float
    cart_adds_30d: float
    wishlist_adds_30d: float
    abandoned_carts_30d: float

    email_opens_30d: float
    campaign_clicks_30d: float

    last_visit_days_ago: float

    city_tier: str
    age_group: str
    acquisition_channel: str
    loyalty_tier: str
    preferred_category: str
    marketing_consent: str

# Batch schema
class BatchRequest(BaseModel):

    customers: List[
        CustomerFeatures
    ]
