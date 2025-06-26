import Config

config :subscription_manager, SubscriptionManager.Repo,
  database: "subs_manager_db",
  username: "postgres",
  password: "postgres",
  hostname: "localhost"

config :subscription_manager,
  ecto_repos: [SubscriptionManager.Repo]
