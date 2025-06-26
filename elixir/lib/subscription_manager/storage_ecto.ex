defmodule SubscriptionManager.Repo do
  use Ecto.Repo,
    otp_app: :subscription_manager,
    adapter: Ecto.Adapters.Postgres
end

defmodule SubscriptionManager.StorageEcto do
  @behaviour SubscriptionManager.Storage

  alias SubscriptionManager.{Repo, Client, Subscription}

  @impl true
  def get_client_by_email(email) do
    case Repo.get_by(Client, email: email) do
      nil -> :error
      client -> {:ok, client}
    end
  end

  @impl true
  def add_client(attrs) do
    %Client{} |> Client.changeset(attrs) |> Repo.insert()
  end

  @impl true
  def get_subscriptions(client_id) do
    Repo.all(from s in Subscription, where: s.client_id == ^client_id)
  end

  @impl true
  def add_subscription(attrs) do
    %Subscription{} |> Subscription.changeset(attrs) |> Repo.insert()
  end
end
