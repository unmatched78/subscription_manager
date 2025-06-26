defmodule SubscriptionManager.Client do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :binary_id, autogenerate: true}
  schema "clients" do
    field :email, :string
    field :phone, :string
    field :fingerprint, :string
    timestamps()
  end

  def changeset(client, attrs) do
    client
    |> cast(attrs, [:email, :phone, :fingerprint])
    |> validate_required([:email])
    |> unique_constraint(:email)
  end
end
