import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { uploadDocument } from "../../lib/api";

interface DocRow {
  name: string;
  chunks: number;
  lastIndexed: string;
}

export default function UploadPage() {
  const [progress, setProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [docs, setDocs] = useState<DocRow[]>([
    { name: "soc2-overview.pdf", chunks: 42, lastIndexed: "2026-05-28" },
  ]);

  const onDrop = useCallback(async (files: File[]) => {
    setUploading(true);
    for (const file of files) {
      await uploadDocument(file, setProgress);
      setDocs((d) => [
        ...d,
        { name: file.name, chunks: 0, lastIndexed: new Date().toISOString().slice(0, 10) },
      ]);
    }
    setUploading(false);
    setProgress(0);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"], "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
  });

  const removeDoc = (name: string) => setDocs((d) => d.filter((x) => x.name !== name));

  return (
    <div className="space-y-6 max-w-2xl">
      <h2 className="text-xl font-semibold">Knowledge Management</h2>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer ${
          isDragActive ? "border-emerald-500 bg-emerald-950/20" : "border-slate-700"
        }`}
      >
        <input {...getInputProps()} />
        <p>Drag & drop PDF or DOCX files</p>
      </div>
      {uploading && (
        <div className="w-full bg-slate-800 rounded h-2">
          <div className="bg-emerald-500 h-2 rounded transition-all" style={{ width: `${progress}%` }} />
        </div>
      )}
      <div>
        <h3 className="text-sm font-medium mb-2">Indexed documents</h3>
        <ul className="space-y-2">
          {docs.map((d) => (
            <li key={d.name} className="flex justify-between items-center bg-slate-900 p-3 rounded">
              <div>
                <span className="font-medium">{d.name}</span>
                <span className="text-xs text-slate-500 ml-2">{d.chunks} chunks · {d.lastIndexed}</span>
              </div>
              <button onClick={() => removeDoc(d.name)} className="text-red-400 text-sm">
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
