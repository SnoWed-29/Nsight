import {
  ArrowUpRight,
  Database,
  FileSpreadsheet,
  MessageSquare,
  Rows3,
} from "lucide-react";
import { Link } from "react-router-dom";

import { datasets } from "../data/mockData";
import { formatNumber } from "../lib/utils";

function Dashboard() {
  const totalRows = datasets.reduce((sum, dataset) => sum + dataset.rows, 0);

  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <div>
        <p className="text-sm font-medium text-zinc-500">Overview</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight">
          Welcome to Nsight
        </h1>
        <p className="mt-2 max-w-2xl text-sm text-zinc-500">
          Import your data, explore its structure, and ask questions using
          natural language.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <StatCard
          label="Datasets"
          value={datasets.length.toString()}
          icon={<Database size={18} />}
        />

        <StatCard
          label="Total rows"
          value={formatNumber(totalRows)}
          icon={<Rows3 size={18} />}
        />

        <StatCard
          label="AI conversations"
          value="24"
          icon={<MessageSquare size={18} />}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <section className="rounded-xl border border-zinc-200 bg-white lg:col-span-2">
          <div className="flex items-center justify-between border-b border-zinc-200 px-5 py-4">
            <div>
              <h2 className="font-semibold">Recent datasets</h2>
              <p className="mt-1 text-xs text-zinc-500">
                Your recently imported data
              </p>
            </div>

            <Link
              to="/datasets"
              className="flex items-center gap-1 text-sm font-medium text-zinc-700 hover:text-zinc-950"
            >
              View all
              <ArrowUpRight size={15} />
            </Link>
          </div>

          <div className="divide-y divide-zinc-100">
            {datasets.map((dataset) => (
              <Link
                key={dataset.id}
                to={`/datasets/${dataset.id}`}
                className="flex items-center justify-between px-5 py-4 transition hover:bg-zinc-50"
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-zinc-100">
                    <FileSpreadsheet size={17} />
                  </div>

                  <div>
                    <p className="font-display text-sm font-medium">
                      {dataset.name}
                    </p>
                    <p className="mt-0.5 text-xs text-zinc-500">
                      {dataset.type} · {formatNumber(dataset.rows)} rows
                    </p>
                  </div>
                </div>

                <span className="text-xs text-zinc-400">
                  {dataset.updatedAt}
                </span>
              </Link>
            ))}
          </div>
        </section>

        <section className="rounded-xl border border-zinc-200 bg-zinc-950 p-6 text-white">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-white/10">
            <MessageSquare size={19} />
          </div>

          <h2 className="mt-6 text-lg font-semibold">Ask your data</h2>

          <p className="mt-2 text-sm leading-6 text-zinc-400">
            Ask questions in plain language. Nsight will analyze your data and
            explain the results.
          </p>

          <Link
            to="/ask"
            className="mt-6 inline-flex items-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-medium text-zinc-950 transition hover:bg-zinc-200"
          >
            Start asking
            <ArrowUpRight size={15} />
          </Link>
        </section>
      </div>
    </div>
  );
}

function StatCard({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon: React.ReactNode;
}) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white p-5">
      <div className="flex items-center justify-between">
        <span className="text-sm text-zinc-500">{label}</span>
        <span className="text-zinc-400">{icon}</span>
      </div>

      <p className="font-display mt-4 text-2xl font-semibold">{value}</p>
    </div>
  );
}

export default Dashboard;
