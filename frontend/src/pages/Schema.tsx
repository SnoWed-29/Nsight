import { KeyRound } from "lucide-react";
import { Link } from "react-router-dom";

import { studentColumns } from "../data/mockData";

function Schema() {
  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <Link
          to="/datasets/students"
          className="text-sm text-zinc-500 hover:text-zinc-900"
        >
          ← Students
        </Link>

        <h1 className="mt-4 text-2xl font-semibold">Schema</h1>

        <p className="mt-1 text-sm text-zinc-500">
          Structure and metadata discovered from the dataset.
        </p>
      </div>

      <div className="rounded-xl border border-zinc-200 bg-white">
        <div className="border-b border-zinc-200 px-5 py-4">
          <h2 className="font-semibold">students</h2>
        </div>

        <table className="w-full text-left text-sm">
          <thead className="border-b border-zinc-200 bg-zinc-50">
            <tr>
              <th className="px-5 py-3 font-medium text-zinc-500">Column</th>
              <th className="px-5 py-3 font-medium text-zinc-500">Type</th>
              <th className="px-5 py-3 font-medium text-zinc-500">
                Nullable
              </th>
              <th className="px-5 py-3 font-medium text-zinc-500">Key</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-zinc-100">
            {studentColumns.map((column) => (
              <tr key={column.name}>
                <td className="px-5 py-4 font-medium">{column.name}</td>
                <td className="px-5 py-4 font-mono text-xs text-zinc-500">
                  {column.type}
                </td>
                <td className="px-5 py-4 text-zinc-500">
                  {column.nullable ? "Yes" : "No"}
                </td>
                <td className="px-5 py-4">
                  {column.key && (
                    <span className="inline-flex items-center gap-1 rounded-md bg-zinc-100 px-2 py-1 text-xs">
                      <KeyRound size={12} />
                      {column.key}
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Schema;