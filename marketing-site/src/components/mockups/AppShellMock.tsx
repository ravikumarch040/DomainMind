type NavItem = "Chat" | "Eval" | "Upload" | "Admin";

interface AppShellMockProps {
  active: NavItem;
  children: React.ReactNode;
}

const navItems: NavItem[] = ["Chat", "Eval", "Upload", "Admin"];

export default function AppShellMock({ active, children }: AppShellMockProps) {
  return (
    <div className="flex min-h-[420px] bg-slate-950 text-slate-100">
      <nav className="hidden w-44 shrink-0 flex-col gap-1 border-r border-slate-800 bg-slate-900 p-3 sm:flex">
        <h1 className="mb-3 text-sm font-semibold text-emerald-400">DomainMind</h1>
        {navItems.map((item) => (
          <span
            key={item}
            className={`rounded px-2.5 py-1.5 text-xs ${
              item === active ? "bg-slate-800 text-emerald-400" : "text-slate-300"
            }`}
          >
            {item}
          </span>
        ))}
      </nav>
      <main className="flex-1 overflow-hidden p-4 text-sm">{children}</main>
    </div>
  );
}
