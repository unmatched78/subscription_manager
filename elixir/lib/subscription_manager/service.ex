defmodule SubscriptionManager.Service do
  alias SubscriptionManager.{Storage, Plan, Subscription}
  import Ecto.Query, only: [from: 2]

  @type plan_map :: %{required(String.t()) => Plan.t()}
  @trial_key "free_trial"

  def start_link(opts), do: Agent.start_link(fn -> opts end, name: __MODULE__)

  @spec register_client(module(), String.t(), String.t() | nil, String.t() | nil) ::
          {:ok, any()} | {:error, any()}
  def register_client(storage, email, phone \\ nil, fingerprint \\ nil) do
    case storage.get_client_by_email(email) do
      {:ok, client} -> {:ok, client}
      :error ->
        storage.add_client(%{email: email, phone: phone, fingerprint: fingerprint})
    end
  end

  @spec start_subscription(module(), map(), String.t(), String.t()) ::
          {:ok, any()} | {:error, any()}
  def start_subscription(storage, plans, client_id, plan_key) do
    case Map.fetch(plans, plan_key) do
      :error -> {:error, :plan_not_found}
      {:ok, %Plan{} = plan} ->
        if plan_key == @trial_key and used_trial?(storage, client_id) do
          {:error, :trial_already_used}
        else
          now = DateTime.utc_now()
          attrs = %{
            client_id: client_id,
            plan_key: plan_key,
            start_date: now,
            end_date: DateTime.add(now, plan.duration_days * 86_400, :second),
            active: true
          }

          storage.add_subscription(attrs)
        end
    end
  end

  defp used_trial?(storage, client_id) do
    storage.get_subscriptions(client_id)
    |> Enum.any?(fn s -> s.plan_key == @trial_key end)
  end
end
