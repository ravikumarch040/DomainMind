import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";
import ChatPage from "./features/chat/ChatPage";
import EvalDashboard from "./features/eval/EvalDashboard";
import UploadPage from "./features/upload/UploadPage";
import AdminPage from "./features/admin/AdminPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen">
        <nav className="w-56 bg-slate-900 border-r border-slate-800 p-4 flex flex-col gap-2">
          <h1 className="text-lg font-semibold text-emerald-400 mb-4">DomainMind</h1>
          <NavLink className="nav-link" to="/">Chat</NavLink>
          <NavLink className="nav-link" to="/eval">Eval</NavLink>
          <NavLink className="nav-link" to="/upload">Upload</NavLink>
          <NavLink className="nav-link" to="/admin">Admin</NavLink>
        </nav>
        <main className="flex-1 p-6 overflow-auto">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/eval" element={<EvalDashboard />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </main>
      </div>
      <style>{`.nav-link { @apply block px-3 py-2 rounded text-slate-300 hover:bg-slate-800; } .nav-link.active { @apply bg-slate-800 text-emerald-400; }`}</style>
    </BrowserRouter>
  );
}
