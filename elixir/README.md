# subscription_manager (Elixir)

An Elixir library for subscription & trial management, with both in-memory and Ecto storage.

## Setup

1. `mix deps.get`
2. Configure `config/config.exs` for your Postgres credentials.
3. `mix ecto.create && mix ecto.migrate` to create tables.
4. In your application supervisor, we already start the Repo.

## Usage

```elixir
alias SubscriptionManager.{StorageEcto, Service, Plan}

# Define plans
plans = %{
  "free_trial" => %Plan{key: "free_trial", name: "14-day Trial", price_cents: 0, duration_days: 14, category: "Trial"},
  "basic"      => %Plan{key: "basic",      name: "Basic",        price_cents: 999, duration_days: 30, category: "Paid"}
}

# Register client
{:ok, client} = Service.register_client(StorageEcto, "alice@example.com", "+2507800000", nil)

# Start subscription
{:ok, sub} = Service.start_subscription(StorageEcto, plans, client.id, "free_trial")
IO.puts("Expires at #{sub.end_date}")
