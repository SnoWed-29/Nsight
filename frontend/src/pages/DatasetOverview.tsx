import { ArrowRight, BarChart3, Database, Rows3 } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import type { ReactNode } from "react";

import { datasets, chartData } from "../data/mockData";
import { formatNumber } from "../lib/utils";

function DatasetOverview() {
  const { datasetId } = useParams();

  const dataset = datasets.find((item) => item.id === datasetId) ?? datasets[0];

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div>
        <Link
          to="/datasets"
          className="text-sm text-zinc-500 hover:text-zinc-900"
        >
          ← Datasets
        </Link>

        <div className="mt-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold">{dataset.name}</h1>
            <p className="mt-1 text-sm text-zinc-500">
              {dataset.type} · {dataset.size}
            </p>
          </div>

          <Link
            to={`/datasets/${dataset.id}/data`}
            className="flex items-center gap-2 rounded-lg bg-zinc-950 px-4 py-2.5 text-sm font-medium text-white"
          >
            Explore data
            <ArrowRight size={16} />
          </Link>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Metric label="Rows" value={formatNumber(dataset.rows)} icon={<Rows3 />} />
        <Metric label="Columns" value={dataset.columns.toString()} icon={<Database />} />
        <Metric label="File size" value={dataset.size} icon={<BarChart3 />} />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <section className="rounded-xl border border-zinc-200 bg-white p-5 lg:col-span-2">
          <h2 className="font-semibold">Data activity</h2>
          <p className="mt-1 text-sm text-zinc-500">
            Example visualization for the frontend.
          </p>

          <div className="mt-8 flex h-56 items-end gap-4">
            {chartData.map((item) => {
              const height = Math.max(15, (item.amount / 5500) * 100);

              return (
                <div
                  key={item.month}
                  className="flex flex-1 flex-col items-center gap-2"
                >
                  <div className="flex h-44 w-full items-end">
                    <div
                      className="w-full rounded-t-md bg-zinc-900"
                      style={{ height: `${height}%` }}
                    />
                  </div>

                  <span className="text-xs text-zinc-400">{item.month}</span>
                </div>
              );
            })}
          </div>
        </section>

        <section className="rounded-xl border border-zinc-200 bg-white p-5">
          <h2 className="font-semibold">Automatic insights</h2>

          <div className="mt-5 space-y-4">
            <Insight
              title="Dataset loaded successfully"
              description={`${formatNumber(dataset.rows)} rows are available for analysis.`}
            />

            <Insight
              title="Data quality"
              description="Most columns contain complete values."
            />

            <Insight
              title="AI ready"
              description="This dataset can be queried using natural language."
            />
          </div>
        </section>
      </div>
    </div>
  );
}

function Metric({
  label,
  value,
  icon,
}: {
  label: string;
  value: string;
  icon: ReactNode;
}) {
  return (
    <div className="rounded-xl border border-zinc-200 bg-white p-5">
      <div className="flex items-center gap-2 text-zinc-400">
        {icon}
        <span className="text-sm">{label}</span>
      </div>

      <p className="font-display mt-4 text-2xl font-semibold">{value}</p>
    </div>
  );
}

function Insight({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="border-l-2 border-zinc-900 pl-4">
      <p className="text-sm font-medium">{title}</p>
      <p className="mt-1 text-xs leading-5 text-zinc-500">{description}</p>
    </div>
  );
}

export default DatasetOverview;
