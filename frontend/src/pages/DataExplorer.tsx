import { Link } from "react-router-dom";

import { transactionRows } from "../data/mockData";
import { formatCurrency } from "../lib/utils";

function DataExplorer() {
  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <Link
          to="/datasets/transactions"
          className="text-sm text-zinc-500 hover:text-zinc-900"
        >
          ← Transactions
        </Link>

        <h1 className="mt-4 text-2xl font-semibold">Data Explorer</h1>

        <p className="mt-1 text-sm text-zinc-500">
          Browse the records in this dataset.
        </p>
      </div>

      <div className="overflow-hidden rounded-xl border border-zinc-200 bg-white">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-zinc-200 bg-zinc-50">
              <tr>
                <th className="px-5 py-3 font-medium text-zinc-500">Date</th>
                <th className="px-5 py-3 font-medium text-zinc-500">
                  Merchant
                </th>
                <th className="px-5 py-3 font-medium text-zinc-500">
                  Category
                </th>
                <th className="px-5 py-3 text-right font-medium text-zinc-500">
                  Amount
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-zinc-100">
              {transactionRows.map((row) => (
                <tr key={`${row.date}-${row.merchant}`}>
                  <td className="px-5 py-4">{row.date}</td>
                  <td className="px-5 py-4 font-medium">{row.merchant}</td>
                  <td className="px-5 py-4 text-zinc-500">{row.category}</td>
                  <td className="px-5 py-4 text-right">
                    {formatCurrency(row.amount, row.currency)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="border-t border-zinc-200 px-5 py-3 text-xs text-zinc-400">
          Showing 5 of 12,482 rows
        </div>
      </div>
    </div>
  );
}

export default DataExplorer;