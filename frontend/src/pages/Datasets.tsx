import { Database, FileUp, Plus } from "lucide-react";
import { Link } from "react-router-dom";

import { datasets } from "../data/mockData";
import { formatNumber } from "../lib/utils";

function Datasets() {
  return (
    <div className="mx-auto max-w-7xl space-y-8">
      <div className="flex items-end justify-between">
        <div>
          <p className="text-sm font-medium text-zinc-500">Workspace</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight">
            Datasets
          </h1>
          <p className="mt-2 text-sm text-zinc-500">
            Import and explore the data you want Nsight to understand.
          </p>
        </div>

        <button className="flex items-center gap-2 rounded-lg bg-zinc-950 px-4 py-2.5 text-sm font-medium text-white hover:bg-zinc-800">
          <Plus size={17} />
          Import data
        </button>
      </div>

      <div className="rounded-xl border border-dashed border-zinc-300 bg-white p-10 text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-zinc-100">
          <FileUp size={22} className="text-zinc-600" />
        </div>

        <h2 className="mt-4 font-semibold">Import a dataset</h2>

        <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-zinc-500">
          Upload CSV, Excel, JSON or SQLite files. Nsight will inspect the
          structure and prepare the data for analysis.
        </p>

        <button className="mt-5 rounded-lg border border-zinc-200 px-4 py-2 text-sm font-medium hover:bg-zinc-50">
          Choose file
        </button>
      </div>

      <div className="rounded-xl border border-zinc-200 bg-white">
        <div className="border-b border-zinc-200 px-5 py-4">
          <h2 className="font-semibold">Your datasets</h2>
        </div>

        <div className="divide-y divide-zinc-100">
          {datasets.map((dataset) => (
            <Link
              key={dataset.id}
              to={`/datasets/${dataset.id}`}
              className="flex items-center justify-between px-5 py-4 hover:bg-zinc-50"
            >
              <div className="flex items-center gap-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-zinc-100">
                  <Database size={18} />
                </div>

                <div>
                  <p className="font-display text-sm font-medium">
                    {dataset.name}
                  </p>
                  <p className="mt-1 text-xs text-zinc-500">
                    {dataset.type} · {dataset.size}
                  </p>
                </div>
              </div>

              <div className="text-right">
                <p className="text-sm font-medium">
                  {formatNumber(dataset.rows)} rows
                </p>
                <p className="mt-1 text-xs text-zinc-400">
                  {dataset.columns} columns
                </p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Datasets;
