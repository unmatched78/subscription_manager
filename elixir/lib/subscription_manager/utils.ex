defmodule SubscriptionManager.Utils do
  @moduledoc """
  Generate a simple fingerprint from IP and headers.
  """
  def fingerprint(headers, ip) when is_map(headers) do
    :crypto.hash(:sha256, ip <> "::" <> Map.get(headers, "user-agent", ""))
    |> Base.encode16(case: :lower)
  end
end
