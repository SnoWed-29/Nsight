import {
  BarChart3,
  Database,
  MessageSquare,
  Settings,
  Sparkles,
} from "lucide-react";
import { NavLink } from "react-router-dom";

const navigation = [
  {
    label: "Dashboard",
    path: "/dashboard",
    icon: BarChart3,
  },
  {
    label: "Datasets",
    path: "/datasets",
    icon: Database,
  },
  {
    label: "Ask Nsight",
    path: "/ask",
    icon: MessageSquare,
  },
];

const secondaryNavigation = [
  {
    label: "Settings",
    path: "/settings",
    icon: Settings,
  },
];

function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-20 flex w-64 flex-col border-r border-zinc-200 bg-white">
      <div className="flex h-16 items-center gap-3 border-b border-zinc-200 px-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-zinc-950 text-white">
          <Sparkles size={16} />
        </div>

        <span className="font-display text-lg font-semibold tracking-tight">
          Nsight
        </span>
      </div>

      <div className="flex flex-1 flex-col px-3 py-5">
        <p className="mb-2 px-3 text-xs font-medium uppercase tracking-wider text-zinc-400">
          Workspace
        </p>

        <nav className="space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  [
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition",
                    isActive
                      ? "bg-zinc-100 text-zinc-950"
                      : "text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900",
                  ].join(" ")
                }
              >
                <Icon size={18} strokeWidth={1.8} />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <div className="mt-8">
          <p className="mb-2 px-3 text-xs font-medium uppercase tracking-wider text-zinc-400">
            System
          </p>

          <nav className="space-y-1">
            {secondaryNavigation.map((item) => {
              const Icon = item.icon;

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    [
                      "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition",
                      isActive
                        ? "bg-zinc-100 text-zinc-950"
                        : "text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900",
                    ].join(" ")
                  }
                >
                  <Icon size={18} strokeWidth={1.8} />
                  {item.label}
                </NavLink>
              );
            })}
          </nav>
        </div>
      </div>

      <div className="border-t border-zinc-200 p-4">
        <div className="rounded-lg bg-zinc-50 p-3">
          <p className="text-xs font-medium text-zinc-500">Local workspace</p>
          <p className="mt-1 text-xs text-zinc-400">
            Your data stays under your control.
          </p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
