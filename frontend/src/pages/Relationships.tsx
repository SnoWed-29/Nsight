import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

function Relationships() {
  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <Link
          to="/datasets/company-db"
          className="text-sm text-zinc-500 hover:text-zinc-900"
        >
          ← Company Database
        </Link>

        <h1 className="mt-4 text-2xl font-semibold">Relationships</h1>

        <p className="mt-1 text-sm text-zinc-500">
          Explore how tables are connected.
        </p>
      </div>

      <div className="min-h-[500px] rounded-xl border border-zinc-200 bg-white p-8">
        <div className="flex min-h-[420px] items-center justify-center">
          <div className="flex items-center gap-6">
            <TableCard
              name="users"
              columns={["id", "name", "email", "role_id"]}
            />

            <ArrowRight className="text-zinc-400" />

            <TableCard
              name="roles"
              columns={["id", "name", "permissions"]}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function TableCard({
  name,
  columns,
}: {
  name: string;
  columns: string[];
}) {
  return (
    <div className="w-64 overflow-hidden rounded-xl border border-zinc-200 bg-white shadow-sm">
      <div className="border-b border-zinc-200 bg-zinc-50 px-4 py-3">
        <p className="text-sm font-semibold">{name}</p>
      </div>

      <div className="divide-y divide-zinc-100">
        {columns.map((column) => (
          <div
            key={column}
            className="px-4 py-2.5 text-xs text-zinc-500"
          >
            {column}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Relationships;