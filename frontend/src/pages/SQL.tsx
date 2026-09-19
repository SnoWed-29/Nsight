import { Copy, Play } from "lucide-react";

const sql = `SELECT
    role,
    COUNT(*) AS user_count
FROM users
GROUP BY role
ORDER BY user_count DESC;`;

function SQL() {
  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <p className="text-sm font-medium text-zinc-500">Developer tools</p>
        <h1 className="mt-1 text-2xl font-semibold">SQL</h1>
        <p className="mt-2 text-sm text-zinc-500">
          Inspect and execute generated SQL queries.
        </p>
      </div>

      <div className="overflow-hidden rounded-xl border border-zinc-200 bg-zinc-950">
        <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
          <span className="text-xs font-medium text-zinc-400">
            Generated SQL
          </span>

          <div className="flex gap-2">
            <button className="flex items-center gap-2 rounded-md bg-zinc-800 px-3 py-1.5 text-xs text-zinc-300 hover:bg-zinc-700">
              <Copy size={13} />
              Copy
            </button>

            <button className="flex items-center gap-2 rounded-md bg-white px-3 py-1.5 text-xs font-medium text-zinc-950">
              <Play size={13} />
              Run
            </button>
          </div>
        </div>

        <pre className="overflow-x-auto p-5 text-sm leading-7 text-zinc-300">
          <code>{sql}</code>
        </pre>
      </div>

      <div className="rounded-xl border border-zinc-200 bg-white p-5">
        <h2 className="font-semibold">Query result</h2>

        <div className="mt-5 rounded-lg border border-zinc-200 bg-zinc-50 p-8 text-center">
          <p className="text-sm text-zinc-500">
            Query results will appear here.
          </p>
        </div>
      </div>
    </div>
  );
}

export default SQL;