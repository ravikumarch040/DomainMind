import { ReactNode } from "react";

interface BrowserFrameProps {
  children: ReactNode;
  title?: string;
}

export default function BrowserFrame({ children, title = "DomainMind — Chat" }: BrowserFrameProps) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-700 bg-slate-950 shadow-2xl shadow-marketing-dark/20">
      <div className="flex items-center gap-2 border-b border-slate-800 bg-slate-900 px-4 py-2.5">
        <div className="flex gap-1.5">
          <span className="h-3 w-3 rounded-full bg-red-500/80" />
          <span className="h-3 w-3 rounded-full bg-yellow-500/80" />
          <span className="h-3 w-3 rounded-full bg-green-500/80" />
        </div>
        <div className="mx-auto flex-1 rounded-md bg-slate-800 px-3 py-1 text-center text-xs text-slate-400">
          {title}
        </div>
      </div>
      <div className="overflow-hidden">{children}</div>
    </div>
  );
}
