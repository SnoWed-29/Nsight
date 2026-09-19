import { Search, Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";

function Header() {
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-zinc-200 bg-white/95 px-6 backdrop-blur">
      <div className="flex items-center gap-2 text-sm text-zinc-500">
        <span>Workspace</span>
        <span>/</span>
        <span className="text-zinc-900">Nsight</span>
      </div>

      <div className="flex items-center gap-3">
        <button
          className="flex items-center gap-2 rounded-lg border border-zinc-200 px-3 py-2 text-sm text-zinc-600 transition hover:bg-zinc-50"
          onClick={() => navigate("/datasets")}
        >
          <Upload size={16} />
          Import data
        </button>

        <button className="flex h-9 w-9 items-center justify-center rounded-lg text-zinc-500 hover:bg-zinc-100">
          <Search size={18} />
        </button>

        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-zinc-900 text-xs font-semibold text-white">
          HD
        </div>
      </div>
    </header>
  );
}

export default Header;