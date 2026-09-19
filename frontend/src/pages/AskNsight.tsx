import { ArrowUp, Database, Sparkles } from "lucide-react";
import { useState } from "react";

function AskNsight() {
  const [question, setQuestion] = useState("");

  const suggestions = [
    "How many students have an average below 10?",
    "When did I spend the most money?",
    "Which tables are related to users?",
    "Give me a SQL query to find administrators.",
  ];

  return (
    <div className="mx-auto flex min-h-[calc(100vh-8rem)] max-w-5xl flex-col">
      <div className="text-center">
        <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-zinc-950 text-white">
          <Sparkles size={21} />
        </div>

        <h1 className="mt-5 text-2xl font-semibold">Ask Nsight</h1>

        <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-zinc-500">
          Ask questions about your datasets in natural language. Nsight will
          analyze the data and explain the answer.
        </p>
      </div>

      <div className="mt-10 grid gap-3 sm:grid-cols-2">
        {suggestions.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => setQuestion(suggestion)}
            className="rounded-xl border border-zinc-200 bg-white p-4 text-left text-sm text-zinc-600 transition hover:border-zinc-400 hover:text-zinc-950"
          >
            {suggestion}
          </button>
        ))}
      </div>

      <div className="mt-auto pt-10">
        <div className="rounded-xl border border-zinc-300 bg-white p-2 shadow-sm">
          <div className="flex items-center gap-3 px-3">
            <Database size={18} className="text-zinc-400" />

            <input
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask a question about your data..."
              className="flex-1 bg-transparent py-3 text-sm outline-none placeholder:text-zinc-400"
            />

            <button
              disabled={!question.trim()}
              className="flex h-9 w-9 items-center justify-center rounded-lg bg-zinc-950 text-white transition hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-30"
            >
              <ArrowUp size={17} />
            </button>
          </div>
        </div>

        <p className="mt-3 text-center text-xs text-zinc-400">
          Nsight can generate SQL, analyze results, and create visualizations.
        </p>
      </div>
    </div>
  );
}

export default AskNsight;