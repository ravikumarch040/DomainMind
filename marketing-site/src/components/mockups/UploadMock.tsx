import AppShellMock from "./AppShellMock";
import BrowserFrame from "./BrowserFrame";

export default function UploadMock() {
  return (
    <BrowserFrame title="DomainMind — Upload">
      <AppShellMock active="Upload">
        <div className="max-w-md space-y-4">
          <h2 className="text-base font-semibold">Knowledge Management</h2>
          <div className="rounded-xl border-2 border-dashed border-slate-700 p-8 text-center text-xs text-slate-400">
            Drag & drop PDF or DOCX files
          </div>
          <div>
            <h3 className="mb-2 text-xs font-medium">Indexed documents</h3>
            <div className="flex items-center justify-between rounded bg-slate-900 p-2.5">
              <div>
                <span className="font-medium">soc2-overview.pdf</span>
                <span className="ml-2 text-[10px] text-slate-500">42 chunks · 2026-05-28</span>
              </div>
              <span className="text-[10px] text-red-400">Delete</span>
            </div>
          </div>
        </div>
      </AppShellMock>
    </BrowserFrame>
  );
}
