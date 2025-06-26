defmodule SubscriptionManager.Application do
  use Application

  def start(_type, _args) do
    children =
      Application.get_env(:subscription_manager, :ecto_repos, [])
      |> Enum.map(& &1)

    opts = [strategy: :one_for_one, name: SubscriptionManager.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
