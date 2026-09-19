export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

export function formatCurrency(
  value: number,
  currency = "MAD",
): string {
  return new Intl.NumberFormat("en-MA", {
    style: "currency",
    currency,
  }).format(value);
}