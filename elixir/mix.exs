defmodule SubscriptionManager.MixProject do
  use Mix.Project

  def project do
    [
      app: :subscription_manager,
      version: "0.1.0",
      elixir: "~> 1.12",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  # Run app under supervision to start Ecto Repo if used
  def application do
    [
      extra_applications: [:logger],
      mod: {SubscriptionManager.Application, []}
    ]
  end

  defp deps do
    [
      {:ecto_sql, "~> 3.8"},
      {:postgrex, ">= 0.0.0"}
    ]
  end
end
