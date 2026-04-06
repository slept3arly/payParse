"use client";

import { useState } from "react";
import FileUpload from "@/components/FileUpload";
import TransactionTable from "@/components/TransactionTable";
import { Loader2, Play } from "lucide-react";

export default function Home() {
  const [data, setData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isUploaded, setIsUploaded] = useState(false);

  const fetchTransactions = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/transactions`);
      if (res.ok) {
        const json = await res.json();
        setData(json.data);
      }
    } catch (err) {
      console.error("Failed to fetch transactions:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleProcess = async () => {
    setIsProcessing(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/process`, {
        method: "POST",
      });
      if (res.ok) {
        await fetchTransactions();
      }
    } catch (err) {
      console.error("Processing failed:", err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 p-8 font-sans">
      <div className="mx-auto max-w-6xl space-y-8">
        <header className="flex items-center justify-between">
          <div className="space-y-1">
            <h1 className="text-3xl font-bold tracking-tight text-slate-900">payParse</h1>
            <p className="text-slate-500">Analyze your Google Pay transaction history securely.</p>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={handleProcess}
              disabled={!isUploaded || isProcessing}
              className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700 disabled:opacity-50"
            >
              {isProcessing ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Play className="h-4 w-4" />
              )}
              {isProcessing ? "Processing..." : "Process All"}
            </button>
          </div>
        </header>

        <section className="grid gap-6 md:grid-cols-4">
          <div className="md:col-span-1">
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="mb-4 text-lg font-semibold text-slate-800">1. Upload Activity</h2>
              <FileUpload onUploadSuccess={() => setIsUploaded(true)} />
            </div>
          </div>

          <div className="md:col-span-3">
            <div className="min-h-[500px] rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
              <div className="border-b border-slate-100 bg-slate-50/50 p-4 flex items-center justify-between">
                <h3 className="font-medium text-slate-700">Transaction History</h3>
                <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
                  {data.length} Transactions
                </span>
              </div>
              <div className="p-0">
                {isLoading ? (
                  <div className="flex h-64 items-center justify-center">
                    <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
                  </div>
                ) : data.length > 0 ? (
                  <TransactionTable transactions={data} />
                ) : (
                  <div className="flex h-64 flex-col items-center justify-center space-y-2 text-slate-400">
                    <p>No data found.</p>
                    <p className="text-sm">Upload your activity file and click "Process All".</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
