defmodule SubscriptionManager.Subscription do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :id, autogenerate: true}
  schema "subscriptions" do
    field :plan_key, :string
    field :start_date, :utc_datetime
    field :end_date, :utc_datetime
    field :active, :boolean, default: true

    belongs_to :client, SubscriptionManager.Client, type: :binary_id
    timestamps()
  end

  def changeset(sub, attrs) do
    sub
    |> cast(attrs, [:client_id, :plan_key, :start_date, :end_date, :active])
    |> validate_required([:client_id, :plan_key, :start_date, :end_date])
  end
end
