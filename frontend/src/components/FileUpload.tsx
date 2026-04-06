"use client";

import { useState } from "react";
import { Upload, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";

interface FileUploadProps {
  onUploadSuccess: () => void;
}

export default function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus("idle");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setStatus("uploading");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      setStatus("success");
      onUploadSuccess();
    } catch (err) {
      setStatus("error");
      setError(err instanceof Error ? err.message : "Something went wrong");
    }
  };

  return (
    <div className="space-y-4">
      <div className="relative group">
        <input
          type="file"
          accept=".html"
          onChange={handleFileChange}
          className="absolute inset-0 z-10 h-full w-full opacity-0 cursor-pointer"
        />
        <div className="flex h-32 flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-200 bg-slate-50 transition-colors group-hover:border-blue-400 group-hover:bg-blue-50/10">
          {file ? (
            <div className="flex flex-col items-center gap-1">
              <span className="text-sm font-medium text-slate-700 truncate max-w-[200px]">
                {file.name}
              </span>
              <span className="text-xs text-slate-400">{(file.size / 1024).toFixed(1)} KB</span>
            </div>
          ) : (
            <>
              <Upload className="mb-2 h-6 w-6 text-slate-400" />
              <span className="text-sm font-medium text-slate-600">Select Google Activity HTML</span>
              <span className="text-xs text-slate-400">"My Activity.html" only</span>
            </>
          )}
        </div>
      </div>

      <button
        onClick={handleUpload}
        disabled={!file || status === "uploading"}
        className="w-full rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition-all hover:bg-slate-800 disabled:bg-slate-200 disabled:text-slate-400"
      >
        {status === "uploading" ? (
          <div className="flex items-center justify-center gap-2">
            <Loader2 className="h-4 w-4 animate-spin" />
            Uploading...
          </div>
        ) : (
          "Upload HTML"
        )}
      </button>

      {status === "success" && (
        <div className="flex items-center gap-2 rounded-lg bg-green-50 p-3 text-sm font-medium text-green-700">
          <CheckCircle2 className="h-4 w-4" />
          Ready to process!
        </div>
      )}

      {status === "error" && (
        <div className="flex items-center gap-2 rounded-lg bg-red-50 p-3 text-sm font-medium text-red-700">
          <AlertCircle className="h-4 w-4" />
          {error}
        </div>
      )}
    </div>
  );
}
