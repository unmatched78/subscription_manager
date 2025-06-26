defmodule SubscriptionManager.Storage do
  @moduledoc """
  Behaviour defining storage interface.
  """
  alias SubscriptionManager.{Client, Subscription}

  @callback get_client_by_email(String.t()) :: {:ok, Client.t()} | :error
  @callback add_client(map()) :: {:ok, Client.t()} | {:error, any()}
  @callback get_subscriptions(String.t()) :: [Subscription.t()]
  @callback add_subscription(map()) :: {:ok, Subscription.t()} | {:error, any()}
end
