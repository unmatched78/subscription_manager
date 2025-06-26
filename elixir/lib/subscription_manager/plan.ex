defmodule SubscriptionManager.Plan do
  @enforce_keys [:key, :name, :price_cents, :duration_days, :category]
  defstruct [:key, :name, :price_cents, :duration_days, :category]
end
