defmodule SubscriptionManager.StorageInMemory do
  @behaviour SubscriptionManager.Storage

  alias SubscriptionManager.{Client, Subscription}

  defstruct clients: %{}, subs: %{}

  @impl true
  def get_client_by_email(email) do
    case Map.get(state().clients, email) do
      nil -> :error
      client -> {:ok, client}
    end
  end

  @impl true
  def add_client(attrs) do
    client = struct(Client, attrs)
    :persistent_term.put({__MODULE__, :clients, attrs.email}, client)
    {:ok, client}
  end

  @impl true
  def get_subscriptions(client_id) do
    Map.get(state().subs, client_id, [])
  end

  @impl true
  def add_subscription(attrs) do
    sub = struct(Subscription, attrs)
    subs = get_subscriptions(attrs.client_id) ++ [sub]
    :persistent_term.put({__MODULE__, :subs, attrs.client_id}, subs)
    {:ok, sub}
  end

  defp state do
    %{
      clients: :persistent_term.get({__MODULE__, :clients}, %{}),
      subs:    :persistent_term.get({__MODULE__, :subs}, %{})
    }
  end
end
